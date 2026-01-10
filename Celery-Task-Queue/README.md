# Celery Task Queue Experiments

This project demonstrates how to set up and use Celery for asynchronous task processing with a Redis broker.

## Business Goals Achieved
- **Asynchronous Processing**: Decoupled heavy computational tasks from the main application flow to improve responsiveness.
- **Distributed Computing**: set up the foundation for checking scale-out architecture where workers can process tasks on different machines.
- **Fault Tolerance**: Utilized a persistent message broker (Redis) to ensure tasks are not lost if the worker is temporarily unavailable.

## Files Description

- `celery_app.py`: Defines the Celery application instance and configuration.
- `celery_tasks.py`: Contains the definitions of tasks (functions decorated with `@celery_app.task`) that will be executed by the workers.
- `trigger_tasks.py`: A client script that enqueues tasks and retrieves their results.

## How to Run

### Prerequisites
1.  **Redis**: Ensure you have a Redis server running locally on port 6379.
    -   If using Docker: `docker run -d -p 6379:6379 redis`
    ```bash
    pip install celery[redis]
    ```

### Troubleshooting
**Error: `docker: error during connect... The system cannot find the file specified`**
This means **Docker Desktop is not running**.
1.  Search for **Docker Desktop** in your Windows Start Menu and launch it.
2.  Wait for the engine to start (the whale icon in the taskbar will stop animating).
3.  Run the `docker run` command again.

### Running the Worker
Open a terminal and navigate to this directory. Start the Celery worker:
*Note: On Windows, use the `pool=solo` option if you encounter concurrency issues.*

```bash
celery -A celery_tasks worker --loglevel=info --pool=solo
```

### Triggering Tasks
Open a second terminal and run the trigger script:

```bash
python trigger_tasks.py
```

You should see the tasks being executed in the worker terminal and the results being printed in the trigger terminal.
