"""Simple Prefect-based ML pipeline."""

from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd
from prefect import flow, task
from sklearn.linear_model import LinearRegression


@task
def collect_data() -> pd.DataFrame:
    return pd.DataFrame({"x": range(100), "y": [value * 2 + 1 for value in range(100)]})


@task
def preprocess_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return frame[["x"]], frame["y"]


@task
def train_model(features: pd.DataFrame, targets: pd.Series) -> LinearRegression:
    model = LinearRegression()
    model.fit(features, targets)
    return model


@task
def save_model(model: LinearRegression, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        pickle.dump(model, handle)
    return output_path


@flow
def ai_pipeline(output_path: str | None = None) -> str:
    """Run the pipeline and save the model.

    By default the model is saved into this package folder as `model.pkl` so
    pipeline artifacts remain colocated.
    """
    data = collect_data()
    features, targets = preprocess_data(data)
    model = train_model(features, targets)

    if output_path is None:
        default_path = Path(__file__).resolve().parent / "model.pkl"
        saved = save_model(model, default_path)
    else:
        saved = save_model(model, Path(output_path))

    return str(saved)


def main() -> None:
    print(ai_pipeline())


if __name__ == "__main__":
    main()
