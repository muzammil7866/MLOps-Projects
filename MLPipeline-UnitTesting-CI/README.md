# ML Pipeline - Unit Testing & CI/CD

Complete machine learning pipeline with comprehensive unit testing and GitHub Actions continuous integration/continuous deployment workflows.

## Overview

This project demonstrates testing best practices for ML projects:
- Unit tests for data processing and model training
- GitHub Actions CI/CD automation
- Test automation on push/pull request
- Code quality checks
- Coverage reporting

## Project Structure

```
MLPipeline-UnitTesting-CI/
├── src/
│   ├── train.py              # Model training pipeline
│   └── __pycache__/          # Cached bytecode
├── tests/
│   ├── test_train.py         # Unit tests for training
│   └── __pycache__/          # Test cache
├── requirements.txt          # Dependencies
├── .github/workflows/        # CI/CD workflows
└── README.md
```

## Training Pipeline (`src/train.py`)

Implements complete ML pipeline:
1. **Data Loading**: Load dataset from CSV
2. **Data Validation**: Check data shapes and types
3. **Train/Test Split**: 80/20 split with random state
4. **Feature Scaling**: StandardScaler normalization
5. **Model Training**: LogisticRegression classifier
6. **Model Evaluation**: Accuracy and other metrics
7. **Model Serialization**: Save to pickle file

### Key Functions

- `load_data()`: Load and validate dataset
- `preprocess_data()`: Normalization and transformation
- `train_model()`: Train LogisticRegression
- `evaluate_model()`: Compute metrics

## Unit Tests (`tests/test_train.py`)

Comprehensive test suite covering:

### Test Cases

1. **`test_data_loading`**: Verify data loads correctly
   - Checks data dimensions
   - Validates data types
   - Ensures non-empty dataset

2. **`test_data_shape`**: Validate expected data shape
   - Correct number of features
   - Correct number of samples
   - Proper label encoding

3. **`test_model_training`**: Test model training process
   - Model trains without errors
   - Generated model file exists
   - Model produces predictions
   - Predictions have correct shape

### Test Utilities

```python
import pytest
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Create test fixtures
@pytest.fixture
def sample_data():
    return load_iris(as_frame=True)
```

## Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_train.py

# Run with coverage
pytest --cov=src tests/

# Show coverage report
pytest --cov=src --cov-report=html tests/
```

## GitHub Actions Workflows

Automated CI/CD in `.github/workflows/`:

### Workflow Triggers
- **On Push**: Every push to any branch
- **On Pull Request**: Every PR against main branch
- **Scheduled**: Optional scheduled runs

### Workflow Steps

1. **Checkout Code**: Clone repository
2. **Setup Python**: Install Python environment
3. **Install Dependencies**: Run `pip install -r requirements.txt`
4. **Run Tests**: Execute `pytest`
5. **Generate Report**: Create coverage report
6. **Publish Results**: Report in Actions tab

### Sample Workflow

```yaml
name: ML Pipeline CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest --cov
      - uses: codecov/codecov-action@v2
```

## Requirements

```
scikit-learn>=0.24.0
pandas>=1.1.0
numpy>=1.19.0
pytest>=6.0.0
pytest-cov>=2.10.0
```

## Features

✓ Comprehensive unit test coverage  
✓ Automated test execution  
✓ Code coverage tracking  
✓ Cross-platform testing  
✓ Dependency management  
✓ Test result reporting  
✓ Failed build notifications  

## MLOps Best Practices

### Testing

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test full pipeline
- **Edge Cases**: Handle boundary conditions
- **Error Handling**: Verify error messages

### CI/CD

- **Automation**: Run tests automatically
- **Early Feedback**: Catch issues in PR
- **Prevent Merge**: Block merge on test failure
- **Metrics**: Track test coverage
- **Documentation**: Clear test names

## Continuous Integration Benefits

1. **Quality Assurance**: Catch bugs early
2. **Collaboration**: Safe code merges
3. **Documentation**: Tests document behavior
4. **Refactoring Confidence**: Tests verify changes
5. **Regression Prevention**: Catch broken changes

## Test Coverage

Aim for high test coverage:
- **Target**: 80-90% code coverage
- **Critical Path**: 100% coverage for core logic
- **Edge Cases**: Cover boundaries and error conditions

Check coverage:
```bash
pytest --cov=src --cov-report=html tests/
# Opens htmlcov/index.html
```

## Troubleshooting

**Issue**: Tests pass locally but fail in CI  
**Solution**: Ensure same Python version; check environment variables

**Issue**: Import errors in tests  
**Solution**: Verify PYTHONPATH and package installation

**Issue**: Flaky tests (fail intermittently)  
**Solution**: Remove time dependencies; use mocking

## Extending Tests

Add tests for:
1. New functions in pipeline
2. Edge cases and error conditions
3. Performance regression (benchmarks)
4. Data validation rules
5. Model evaluation metrics

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [ML Testing Pyramid](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
