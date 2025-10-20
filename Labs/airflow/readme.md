# Customer Churn Prediction Pipeline

## Overview
End-to-end ML pipeline using Apache Airflow to predict customer churn with Random Forest classification.

## Project Structure
```
.
├── dags/
│   └── airflow.py                 # DAG definition
├── src/
│   └── lab.py                     # ML functions
├── data/
│   ├── file.csv                   # Training data
│   └── test.csv                   # Test data
└── model/
    └── churn_model.pkl           # Trained model
```

## Pipeline Tasks

1. **load_customer_data** - Load and serialize customer data
2. **preprocess_and_feature_engineer** - Clean data, engineer features, split train/test
3. **train_random_forest_model** - Train Random Forest with hyperparameter tuning
4. **evaluate_model_performance** - Evaluate model and generate metrics

## Features

**Engineered Features:**
- Balance to Credit Ratio
- Purchases per Transaction

**Model Training:**
- Hyperparameter tuning (n_estimators: 50/100/200, max_depth: 5/10/15)
- Best model selection based on training accuracy

**Evaluation Metrics:**
- Test Accuracy, ROC AUC Score
- Confusion Matrix, Feature Importance
- Classification Report

## Setup
```bash
pip install apache-airflow pandas scikit-learn numpy pickle5 kneed
export AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
```

## Run
```bash
airflow standalone
```

Access UI at `http://localhost:8080` and trigger `Customer_Churn_Prediction_Pipeline`

## Configuration

- Schedule: 1 day, 0:00:00
- Start Date: 2025-10-20
- Catchup: False

## Sample Output
```
Test Accuracy: 0.8542
ROC AUC Score: 0.9123

Feature Importance:
  BALANCE_TO_CREDIT_RATIO: 0.3421
  PURCHASES: 0.2876
  CREDIT_LIMIT: 0.1987
```