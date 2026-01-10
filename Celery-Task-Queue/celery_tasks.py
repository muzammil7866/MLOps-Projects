import time
from celery_app import celery_app

@celery_app.task
def add(x, y):
    """Simple task to add two numbers."""
    return x + y

@celery_app.task
def simulate_heavy_task(duration):
    """Simulates a CPU-heavy or I/O-heavy task."""
    print(f"Starting heavy task for {duration} seconds...")
    time.sleep(duration)
    print("Heavy task completed.")
    return f"Task completed in {duration} seconds"
