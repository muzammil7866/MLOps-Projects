from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI()

# Load the model once when the app starts
model_path = "models/model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    model = None

# Define the input data format
class PredictionRequest(BaseModel):
    feature1: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict(request: PredictionRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not found")
    
    # Convert input to dataframe for the model
    data = pd.DataFrame([{"feature1": request.feature1}])
    prediction = model.predict(data)[0]
    
    return {"prediction": int(prediction)}