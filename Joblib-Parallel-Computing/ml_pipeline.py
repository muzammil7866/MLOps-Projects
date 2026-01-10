from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def create_pipeline():
    # Define a pipeline with a scaler and a classifier
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression())
    ])
    print("Pipeline created successfully:")
    print(pipeline)

if __name__ == "__main__":
    create_pipeline()
