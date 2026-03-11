# src/train.py
import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression

# 1. Load dataset
data_path = 'data/dataset.csv'
df = pd.read_csv(data_path)
X = df[['feature1']]
y = df['label']

# 2. Train a small model
model = LogisticRegression()
model.fit(X, y)

# 3. Save model to models/model.pkl
os.makedirs('models', exist_ok=True)
output_path = 'models/model.pkl'
with open(output_path, 'wb') as f:
    pickle.dump(model, f)

print(f"Model trained and saved to {output_path}")