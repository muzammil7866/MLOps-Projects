from airflow.decorators import dag, task
from datetime import datetime
import json

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

@dag(default_args=default_args, schedule=None, tags=['mlops'])
def training_pipeline():

    # Task 1: Load Data
    @task
    def load_data():
        # Simulating data loading
        data = {'feature1': [1, 2, 3], 'label': [0, 1, 0]}
        print("Data loaded successfully.")
        return data

    # Task 2: Train Model
    @task
    def train_model(data):
        # Simulating training (using mock logic to avoid import errors inside Airflow)
        # In a real scenario, you'd import sklearn here
        features = data['feature1']
        labels = data['label']
        print(f"Training on {len(features)} rows...")
        
        # Mock model artifact
        model = {"weights": [0.5, 0.2], "bias": 0.1}
        return model

    # Task 3: Save Model
    @task
    def save_model(model):
        import os
        import pickle
        
        # Save to a path that is mapped in docker-compose (usually /opt/airflow/)
        save_path = "/opt/airflow/logs/model.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model saved to {save_path}")
        return save_path

    # Task 4: Log Results
    @task
    def log_results(model_path):
        print(f"Pipeline finished. Model available at: {model_path}")

    # Define the dependency flow
    dataset = load_data()
    trained_model = train_model(dataset)
    path = save_model(trained_model)
    log_results(path)

# Instantiate the DAG
dag = training_pipeline()