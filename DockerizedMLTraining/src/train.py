import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression

# Load Data
# Note: In Docker, we will copy files to /app, so paths remain relative
if not os.path.exists('data/dataset.csv'):
    raise FileNotFoundError("Dataset not found!")

df = pd.read_csv('data/dataset.csv')
X = df[['feature1']]
y = df['label']

# Train Model
model = LogisticRegression()
model.fit(X, y)
print("Model trained successfully.")

# Save Model
os.makedirs('models', exist_ok=True)
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Training pipeline executed successfully.")