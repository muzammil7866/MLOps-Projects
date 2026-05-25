from __future__ import annotations

import datetime as dt
import logging
from pathlib import Path

import joblib

LOGGER = logging.getLogger("apscheduler_ml_job")
DEFAULT_SAMPLE_INPUT = [[1.0, 2.0, 3.0]]


def parse_sample_input(raw_sample_input: str | None) -> list[list[float]]:
    if not raw_sample_input:
        return DEFAULT_SAMPLE_INPUT

    try:
        values = [float(item.strip()) for item in raw_sample_input.split(",") if item.strip()]
    except ValueError as exc:
        raise ValueError("Sample input must be a comma-separated list of numbers.") from exc

    if not values:
        return DEFAULT_SAMPLE_INPUT

    return [values]


def run_model(model_path: Path, log_path: Path, sample_input: list[list[float]] | None = None) -> str:
    now = dt.datetime.now()
    sample = sample_input or DEFAULT_SAMPLE_INPUT

    if model_path.exists():
        model = joblib.load(model_path)
        prediction = model.predict(sample)
        message = f"Model ran at {now.isoformat()} with prediction {prediction}"
    else:
        message = f"Model ran at {now.isoformat()} but no model was found at {model_path}"

    LOGGER.info(message)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(message + "\n")

    return message
