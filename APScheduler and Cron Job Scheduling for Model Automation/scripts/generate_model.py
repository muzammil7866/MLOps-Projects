from __future__ import annotations

from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model.pkl"


def build_and_save_model(path: Path = MODEL_PATH) -> None:
    X = np.array([
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 4.0, 5.0],
        [4.0, 5.0, 6.0],
    ])
    y = np.array([1.0, 2.0, 3.0, 4.0])
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, path)
    print(f"Saved demo model to {path}")


if __name__ == "__main__":
    build_and_save_model()
