# Create this as a temporary script or run in python shell
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

os.makedirs('models', exist_ok=True)
# Dummy training data
df = pd.DataFrame({'feature1': [1, 10, 20], 'label': [0, 1, 1]})
model = LogisticRegression()
model.fit(df[['feature1']], df['label'])

with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved to models/model.pkl")