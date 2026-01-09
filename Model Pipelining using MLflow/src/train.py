# src/train.py
import os
import argparse
import joblib
import matplotlib.pyplot as plt
import numpy as np
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def plot_confusion_matrix(cm, labels, out_path):
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest')
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, cm[i, j], ha="center", va="center")
    plt.title("Confusion Matrix")
    plt.colorbar(im)
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

def main(args):
    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Set MLflow tracking URI (if you have a remote server, pass it via --mlflow-uri)
    if args.mlflow_uri:
        mlflow.set_tracking_uri(args.mlflow_uri)

    experiment_name = args.experiment_name
    mlflow.set_experiment(experiment_name)

    # Load dataset (Iris example)
    data = load_iris()
    X, y = data.data, data.target
    labels = data.target_names

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )

    models = {
        "logistic": (Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(random_state=42, max_iter=500))]),
                     {"C":1.0, "penalty":"l2"}),
        "random_forest": (Pipeline([("clf", RandomForestClassifier(random_state=42, n_estimators=100))]),
                          {"n_estimators":100, "max_depth": None}),
        "svc": (Pipeline([("scaler", StandardScaler()), ("clf", SVC(probability=True, random_state=42))]),
                {"C":1.0, "kernel":"rbf"})
    }

    best_f1 = -1.0
    best_run_info = None

    for name, (pipeline, hyperparams) in models.items():
        with mlflow.start_run(run_name=name) as run:
            print(f"Training {name} ...")
            # fit
            pipeline.fit(X_train, y_train)

            # predict
            y_pred = pipeline.predict(X_test)

            # metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
            rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
            f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

            # Log params & metrics to MLflow
            mlflow.log_param("model_name", name)
            for k, v in hyperparams.items():
                mlflow.log_param(k, v)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision_macro", prec)
            mlflow.log_metric("recall_macro", rec)
            mlflow.log_metric("f1_macro", f1)

            # Save local model
            local_model_path = f"models/{name}_model.joblib"
            joblib.dump(pipeline, local_model_path)
            mlflow.log_artifact(local_model_path, artifact_path="models_local")

            # Confusion matrix artifact
            cm = confusion_matrix(y_test, y_pred)
            cm_path = f"results/confusion_matrix_{name}.png"
            plot_confusion_matrix(cm, labels, cm_path)
            mlflow.log_artifact(cm_path, artifact_path="confusion_matrices")

            # Log the model with mlflow.sklearn (this saves model as an artifact "model")
            mlflow.sklearn.log_model(pipeline, artifact_path="model")

            # Track best by f1
            if f1 > best_f1:
                best_f1 = f1
                best_run_info = {
                    "run_id": run.info.run_id,
                    "model_name": name,
                    "f1": f1
                }

            print(f"Run {name} metrics: acc={acc:.4f} f1={f1:.4f}")

    print("Best run:", best_run_info)

    # Optionally register best model
    if args.register and best_run_info:
        try:
            client = MlflowClient(tracking_uri=mlflow.get_tracking_uri())
            model_uri = f"runs:/{best_run_info['run_id']}/model"
            registered_model_name = args.registered_model_name or "mlops_assignment_best_model"
            print("Registering model:", model_uri, "as", registered_model_name)
            # This requires the MLflow server to support model registry
            mv = client.create_model_version(name=registered_model_name, source=model_uri, run_id=best_run_info["run_id"])
            print("Requested model version:", mv.version)
            # Optionally transition to Staging (uncomment if desired)
            # client.transition_model_version_stage(name=registered_model_name, version=mv.version, stage="Staging")
            print("Model registration requested. Check MLflow Model Registry UI.")
        except Exception as e:
            print("Model registration failed (server may not support registry):", e)
            print("You can register manually via the MLflow UI using the model URI:", model_uri)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-name", default="mlops-assignment-1", type=str)
    parser.add_argument("--test-size", default=0.2, type=float)
    parser.add_argument("--mlflow-uri", default=None, type=str, help="MLflow tracking URI (optional)")
    parser.add_argument("--register", action="store_true", help="Attempt to register best model in MLflow registry")
    parser.add_argument("--registered-model-name", default=None, help="Name for registered model")
    args = parser.parse_args()
    main(args)
