
# Prefect ML Pipeline

## Overview

This project demonstrates a small Prefect workflow that creates sample data, preprocesses it, trains a linear regression model, and saves the result to disk.

## Business Goal

The business goal is to show how a model training workflow can be orchestrated and repeated reliably. That is the basic pattern behind many MLOps pipelines for training, retraining, and artifact management.

## Structure

- `prefect_pipeline.py` - Prefect flow and tasks
- `requirements.txt` - runtime dependencies

## Setup

Install the dependencies listed in `requirements.txt`.

## Run

```bash
python prefect_pipeline.py
```

## Notes

By default the flow saves `model.pkl` in the current directory, but you can pass a custom output path through the flow entry point.
