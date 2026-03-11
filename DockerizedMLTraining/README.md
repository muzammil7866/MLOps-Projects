# Dockerized ML Training

Production-ready Docker containerization for machine learning model training pipelines, enabling reproducible and portable ML workflows.

## Overview

This project demonstrates containerization best practices for ML:
- Multi-stage Docker builds
- Lightweight images
- Dependency management
- Environment reproducibility
- Easy deployment and scaling

## Dockerfile Stages

### Base Stage
- **Image**: `python:3.9-slim` (minimal footprint)
- **Size**: ~150MB (much smaller than full python)
- **Purpose**: Efficient, production-ready base

### Build Stage
- Install build dependencies
- Install Python packages from requirements
- Set working directory

### Final Stage
- Minimal footprint with only essentials
- Copy pre-built wheels from build stage
- Copy training scripts
- Set entry point

## Features

- **Lightweight Containers**: Slim base images
- **Layer Caching**: Efficient rebuilds
- **Multi-Stage Builds**: Separate build and runtime
- **Volume Mounting**: Input/output data handling
- **Environment Configuration**: Parameterized training

## Dockerfile Structure

```dockerfile
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY train.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "train.py"]
```

## Building the Image

```bash
# Build image
docker build -t ml-training:latest .

# Build with build args
docker build --build-arg PYTHON_VERSION=3.10 -t ml-training:3.10 .

# Build and tag
docker build -t myregistry/ml-training:v1.0 .
```

## Running Containers

### Basic Execution

```bash
# Run training
docker run ml-training:latest

# With volume mount (input/output data)
docker run -v /local/data:/app/data ml-training:latest

# With environment variables
docker run -e EPOCHS=100 -e BATCH_SIZE=32 ml-training:latest

# Run and remove after exit
docker run --rm ml-training:latest
```

### Advanced Options

```bash
# Mount multiple volumes
docker run \
  -v /local/data:/app/data \
  -v /local/models:/app/models \
  ml-training:latest

# Set resource limits
docker run \
  --memory=4g \
  --cpus=2 \
  ml-training:latest

# Interactive mode
docker run -it ml-training:latest bash
```

## Best Practices

### Image Optimization

✓ Use specific Python version (not `latest`)  
✓ Use slim/alpine variants when possible  
✓ Multi-stage builds to reduce size  
✓ Clean up cache after install  
✓ Minimize layers (combine RUN commands)  

### Security

✓ Don't run as root (create user)  
✓ Use specific base image versions  
✓ Scan images for vulnerabilities  
✓ Keep dependencies updated  
✓ No sensitive data in images  

### Reproducibility

✓ Pin all dependency versions  
✓ Document build arguments  
✓ Use fixed base image tags  
✓ Include requirements.txt in git  

## Requirements File

```
scikit-learn==0.24.2
pandas==1.3.0
numpy==1.21.0
tensorflow==2.6.0
torch==1.9.0
```

## File Structure

```
DockerizedMLTraining/
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── train.py               # Training script
├── data/                  # Training data (optional)
│   └── dataset.csv
└── models/                # Output models (optional)
```

## Training Script

Environment-aware training configuration:

```python
import os
import sys

# Read parameters from environment
EPOCHS = int(os.getenv("EPOCHS", 50))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
DATA_PATH = os.getenv("DATA_PATH", "/app/data")
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models")

# Training logic
def train():
    # Load data
    # Build model
    # Train
    # Save model
    pass
```

## Docker Compose

Scale and manage multiple containers:

```yaml
version: '3.8'
services:
  training:
    build: .
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - EPOCHS=100
      - BATCH_SIZE=32
    mem_limit: 4g
```

```bash
# Run with compose
docker-compose up
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Build Docker image
  run: docker build -t ml-training:latest .

- name: Run tests in container
  run: docker run --rm ml-training:latest python -m pytest

- name: Push to registry
  run: docker push myregistry/ml-training:latest
```

## Registry Deployment

### Docker Hub

```bash
# Tag image
docker tag ml-training:latest myusername/ml-training:v1.0

# Login
docker login

# Push
docker push myusername/ml-training:v1.0
```

### Cloud Registries

```bash
# Google Container Registry
docker tag ml-training gcr.io/myproject/ml-training:v1.0
docker push gcr.io/myproject/ml-training:v1.0

# AWS ECR
docker tag ml-training 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-training:v1.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-training:v1.0
```

## Troubleshooting

**Issue**: Container exits immediately  
**Solution**: Check logs with `docker logs <container_id>`

**Issue**: Out of memory errors  
**Solution**: Increase memory limit in docker run or compose

**Issue**: Permission denied accessing volumes  
**Solution**: Ensure correct user in Dockerfile; use proper ownership

**Issue**: Dependency conflicts  
**Solution**: Pin exact versions in requirements.txt

## Image Information

```bash
# Check image size
docker images ml-training

# View build history
docker history ml-training:latest

# Inspect image details
docker inspect ml-training:latest
```

## Benefits

1. **Reproducibility**: Same environment everywhere
2. **Portability**: Run on any Docker host
3. **Scalability**: Easy to scale horizontally
4. **Isolation**: Dependencies won't conflict
5. **CI/CD**: Automated building/testing
6. **Deployment**: Push to any cloud

## Next Steps

1. Build image: `docker build -t ml-training .`
2. Test locally: `docker run --rm ml-training`
3. Push to registry: `docker push myregistry/ml-training`
4. Deploy to cloud: Use Kubernetes, Cloud Run, or ECS

## References

- [Docker Documentation](https://docs.docker.com/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Docker Images](https://hub.docker.com/_/python)
