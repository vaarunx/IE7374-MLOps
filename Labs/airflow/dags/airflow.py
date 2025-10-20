from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_evaluate

default_args = {
    'owner': 'varun',
    'start_date': datetime(2025, 1, 15),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'Customer_Churn_Prediction_Pipeline',
    default_args=default_args,
    description='ML pipeline for predicting customer churn using Random Forest',
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='load_customer_data',
        python_callable=load_data,
    )

    data_preprocessing_task = PythonOperator(
        task_id='preprocess_and_feature_engineer',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    build_save_model_task = PythonOperator(
        task_id='train_random_forest_model',
        python_callable=build_save_model,
        op_args=[data_preprocessing_task.output, "churn_model.pkl"],
    )

    evaluate_model_task = PythonOperator(
        task_id='evaluate_model_performance',
        python_callable=load_model_evaluate,
        op_args=["churn_model.pkl", build_save_model_task.output, data_preprocessing_task.output],
    )

    load_data_task >> data_preprocessing_task >> build_save_model_task >> evaluate_model_task

if __name__ == "__main__":
    dag.test()