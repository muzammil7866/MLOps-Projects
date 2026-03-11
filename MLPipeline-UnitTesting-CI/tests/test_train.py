import pytest
import pandas as pd
from src.train import load_data, prepare_data, train_model

# Create a mock dataset for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame({'feature1': [1, 2, 3], 'label': [0, 1, 0]})

def test_data_loading():
    # Test if the specific file exists
    df = load_data('data/dataset.csv')
    assert not df.empty, "Dataset should not be empty"

def test_shape_validation(sample_data):
    # Test if X and y have matching lengths
    X, y = prepare_data(sample_data)
    assert len(X) == len(y), "Features and labels must have same number of rows"

def test_model_training(sample_data):
    # Test if model training returns an object
    X, y = prepare_data(sample_data)
    model = train_model(X, y)
    # Check if it has a predict method (standard for sklearn models)
    assert hasattr(model, "predict"), "Model should have a predict method"