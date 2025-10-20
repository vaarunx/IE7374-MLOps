import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import pickle
import os
import base64

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("Loading customer data...")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    
    # Simulate a churn column if it doesn't exist (for demo purposes)
    if 'CHURN' not in df.columns:
        np.random.seed(42)
        # Higher balance and purchases = lower churn probability
        churn_prob = 1 / (1 + np.exp(df['BALANCE'].fillna(0) / 5000))
        df['CHURN'] = (np.random.random(len(df)) < churn_prob).astype(int)
    
    serialized_data = pickle.dumps(df)
    return base64.b64encode(serialized_data).decode("ascii")

def data_preprocessing(data_b64: str):
    """
    Deserializes data, performs preprocessing, creates features,
    and returns base64-encoded pickled train/test data.
    """
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    
    # Create some feature engineering
    df['BALANCE_TO_CREDIT_RATIO'] = df['BALANCE'] / (df['CREDIT_LIMIT'] + 1)
    df['PURCHASES_PER_TRANSACTION'] = df['PURCHASES'] / (df.get('PURCHASES_TRX', 1) + 1)
    
    feature_columns = ["BALANCE", "PURCHASES", "CREDIT_LIMIT", 
                       "BALANCE_TO_CREDIT_RATIO", "PURCHASES_PER_TRANSACTION"]
    X = df[feature_columns]
    y = df['CHURN']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Package everything together
    preprocessed_data = {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_train': y_train.values,
        'y_test': y_test.values,
        'scaler': scaler,
        'feature_names': feature_columns
    }

    serialized_data = pickle.dumps(preprocessed_data)
    return base64.b64encode(serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a Random Forest model on the preprocessed data and saves it.
    Returns training metrics (JSON-serializable).
    """
    data_bytes = base64.b64decode(data_b64)
    data_dict = pickle.loads(data_bytes)

    X_train = data_dict['X_train']
    y_train = data_dict['y_train']

    # Train Random Forest with different hyperparameters to find best
    results = []
    best_score = 0
    best_model = None
    
    for n_estimators in [50, 100, 200]:
        for max_depth in [5, 10, 15]:
            rf = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                n_jobs=-1
            )
            rf.fit(X_train, y_train)
            score = rf.score(X_train, y_train)
            results.append({
                'n_estimators': n_estimators,
                'max_depth': max_depth,
                'train_accuracy': float(score)
            })
            
            if score > best_score:
                best_score = score
                best_model = rf

    print(f"Best training accuracy: {best_score:.4f}")

    # Save the best model
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    model_package = {
        'model': best_model,
        'scaler': data_dict['scaler'],
        'feature_names': data_dict['feature_names']
    }
    
    with open(output_path, "wb") as f:
        pickle.dump(model_package, f)

    return results


def load_model_evaluate(filename: str, training_results: list, data_b64: str):
    """
    Loads the saved model and evaluates it on test data.
    Returns evaluation metrics as a dictionary.
    """
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    model_package = pickle.load(open(output_path, "rb"))
    
    model = model_package['model']
    feature_names = model_package['feature_names']

    # Get test data
    data_bytes = base64.b64decode(data_b64)
    data_dict = pickle.loads(data_bytes)
    X_test = data_dict['X_test']
    y_test = data_dict['y_test']

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    test_accuracy = float(model.score(X_test, y_test))
    roc_auc = float(roc_auc_score(y_test, y_pred_proba))
    
    # Get feature importance
    feature_importance = {
        name: float(importance) 
        for name, importance in zip(feature_names, model.feature_importances_)
    }

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    print(f"ROC AUC Score: {roc_auc:.4f}")
    print(f"\nFeature Importance:")
    for name, imp in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {imp:.4f}")
    
    print(f"\nConfusion Matrix:\n{cm}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

    return {
        'test_accuracy': test_accuracy,
        'roc_auc': roc_auc,
        'feature_importance': feature_importance,
        'confusion_matrix': cm.tolist(),
        'training_results': training_results
    }