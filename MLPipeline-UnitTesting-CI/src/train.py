import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression

# Function 1: Load Data
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)

# Function 2: Prepare Data
def prepare_data(df):
    X = df[['feature1']]
    y = df['label']
    return X, y

# Function 3: Train Model
def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    return model

# Main Execution
if __name__ == "__main__":
    df = load_data('data/dataset.csv')
    X, y = prepare_data(df)
    model = train_model(X, y)
    
    # Save Model
    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Training pipeline executed successfully.")