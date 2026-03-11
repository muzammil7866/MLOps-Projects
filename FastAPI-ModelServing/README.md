# FastAPI - Model Serving

Production-ready REST API for machine learning model deployment built with FastAPI, featuring automatic validation, documentation, and high-performance serving.

## Overview

FastAPI is a modern, fast web framework for:
- Building production-ready APIs
- Serving ML models with low latency
- Automatic request/response validation
- Interactive API documentation
- Deployment on Uvicorn/Gunicorn

## Project Structure

```
FastAPI-ModelServing/
├── api/
│   ├── main.py               # FastAPI application
│   └── __pycache__/
├── models/                   # Trained models
│   └── model.pkl            # Serialized model
├── requirements.txt         # Dependencies
└── test.py                  # API tests
```

## FastAPI Application (`api/main.py`)

### Basic Structure

```python
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI(
    title="ML Model API",
    description="API for ML model inference",
    version="1.0.0"
)

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/predict")
def predict(inputs):
    """Make predictions"""
    predictions = model.predict(inputs)
    return {"predictions": predictions.tolist()}
```

## Request/Response Models

Use Pydantic for validation:

```python
from pydantic import BaseModel, Field
from typing import List

class PredictionInput(BaseModel):
    """Input features for prediction"""
    features: List[float] = Field(
        ..., 
        description="Input feature vector",
        example=[1.0, 2.0, 3.0]
    )

class PredictionOutput(BaseModel):
    """Prediction result"""
    prediction: float
    confidence: float
    model_version: str
```

## Endpoints

### Health Check
```python
@app.get("/health")
def health():
    """
    Health check endpoint
    
    Returns:
        status: Service health status
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }
```

### Predictions
```python
@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Make single prediction
    
    Args:
        input_data: Features for prediction
        
    Returns:
        Prediction with confidence score
    """
    features = [input_data.features]
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0].max()
    
    return PredictionOutput(
        prediction=float(prediction),
        confidence=float(confidence),
        model_version="1.0.0"
    )
```

### Batch Predictions
```python
@app.post("/batch_predict")
def batch_predict(batch_inputs: List[PredictionInput]):
    """
    Make batch predictions
    
    Args:
        batch_inputs: List of feature vectors
        
    Returns:
        List of predictions
    """
    features = [inp.features for inp in batch_inputs]
    predictions = model.predict(features)
    
    return {
        "predictions": predictions.tolist(),
        "count": len(predictions)
    }
```

## Error Handling

```python
from fastapi import HTTPException

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        # Validation happens automatically via Pydantic
        features = [input_data.features]
        
        # Custom validation
        if len(features[0]) != expected_features:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {expected_features} features, got {len(features[0])}"
            )
        
        prediction = model.predict(features)[0]
        return {"prediction": float(prediction)}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Running the API

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn api.main:app --reload

# Access API at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Production

```bash
# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app

# Production settings
gunicorn -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    api.main:app
```

## Interactive Documentation

FastAPI auto-generates documentation:

### Swagger UI
Access at `http://localhost:8000/docs`
- Interactive endpoint testing
- Request/response schemas
- Try-it-out functionality

### ReDoc
Access at `http://localhost:8000/redoc`
- Alternative documentation interface
- Better for complex APIs

## Testing API

### Using httpx (async)

```python
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_prediction():
    response = client.post("/predict", json={
        "features": [1.0, 2.0, 3.0]
    })
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [1.0, 2.0, 3.0]}'

# Batch prediction
curl -X POST http://localhost:8000/batch_predict \
    -H "Content-Type: application/json" \
    -d '[{"features": [1.0, 2.0]}, {"features": [3.0, 4.0]}]'
```

## Deployment

### Docker (see DockerizedMLTraining)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

### Cloud Platforms

#### Google Cloud Run
```bash
gcloud run deploy ml-api \
    --source . \
    --platform managed \
    --region us-central1
```

#### AWS Lambda
Use API Gateway + Lambda for serverless deployment

#### Azure
Use Azure App Service or Container Instances

## Performance Features

### Automatic Validation
- Request validation via Pydantic
- Type checking
- Error messages automatically generated

### Async Support
```python
@app.post("/async_predict")
async def async_predict(input_data: PredictionInput):
    # Non-blocking I/O operations
    # Run ML inference
    return {"prediction": ...}
```

### Dependency Injection
```python
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict")
def predict(input: Input, db: Database = Depends(get_db)):
    return model.predict(input.features)
```

## Advanced Features

### CORS (Cross-Origin Resource Sharing)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/predict")
def predict(
    input: PredictionInput,
    credentials: HTTPAuthCredentials = Depends(security)
):
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401)
    return model.predict([input.features])
```

### Middleware
```python
@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    # Add custom headers
    return response
```

## Monitoring & Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict")
def predict(input_data: PredictionInput):
    logger.info(f"Received prediction request with features: {input_data.features}")
    prediction = model.predict([input_data.features])
    logger.info(f"Prediction: {prediction}")
    return {"prediction": float(prediction)}
```

## Requirements

```
fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.0.0
scikit-learn==1.3.0
numpy==1.24.0
requests==2.31.0
pytest==7.4.0
httpx==0.25.0
```

## Best Practices

✓ Validate all inputs with Pydantic models  
✓ Clear error messages  
✓ Health endpoints for monitoring  
✓ Comprehensive documentation  
✓ Logging and metrics  
✓ Rate limiting  
✓ Authentication when needed  
✓ Model versioning  
✓ Graceful error handling  

## Features Summary

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Auto validation | ✓ | ✗ | ✗ |
| Auto docs | ✓ | ✗ | ✗ |
| Async | ✓ | ✓ | ✗ |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Learning curve | Easy | Easy | Steep |

## Troubleshooting

**Issue**: CORS errors  
**Solution**: Add CORSMiddleware to app

**Issue**: Model loading slow  
**Solution**: Load model at startup, cache in memory

**Issue**: Out of memory  
**Solution**: Load smaller model or use model quantization

**Issue**: Slow predictions  
**Solution**: Use batch processing, consider GPU

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [API Best Practices](https://restfulapi.net/)
