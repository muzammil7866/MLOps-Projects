# Airflow - Pipeline Orchestration

Enterprise-grade workflow orchestration using Apache Airflow, demonstrating modern DAG-based pipeline management with task dependencies, scheduling, and monitoring.

## Overview

Apache Airflow is a powerful platform for:
- Defining complex ML pipelines as DAGs (Directed Acyclic Graphs)
- Scheduling and monitoring workflows
- Handling task dependencies and failure recovery
- Implementing data pipelines at scale
- Central management and UI

## Airflow Concepts

### DAG (Directed Acyclic Graph)
- **Nodes**: Individual tasks to execute
- **Edges**: Dependencies between tasks
- **Direction**: Tasks flow in defined order
- **No Cycles**: No task depends on itself

### Tasks
- Individual units of work
- Can be Python operators, Bash commands, etc.
- Have dependencies on other tasks
- Generate outputs (XCom)

### Operators
- **PythonOperator**: Execute Python functions
- **BashOperator**: Execute shell commands
- **EmailOperator**: Send notifications
- **SensorOperator**: Wait for external conditions

## Project Structure

```
Airflow-PipelineOrchestration/
├── docker-compose.yaml           # Airflow environment
├── config/
│   └── airflow.cfg              # Configuration
├── dags/
│   ├── train_pipeline.py        # DAG definition
│   └── __pycache__/
├── logs/                        # Execution logs
│   └── dag_id=training_pipeline/
└── plugins/                     # Custom operators/hooks
```

## DAG Definition (`train_pipeline.py`)

Modern Airflow DAG using Python decorators:

```python
from airflow.decorators import dag, task
from airflow import DAG
from datetime import datetime

@dag(
    dag_id="training_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["ml", "training"]
)
def training_pipeline():
    """ML training and evaluation pipeline"""
    
    @task
    def load_data():
        """Load and validate data"""
        # Implementation
        return data_path
    
    @task
    def train_model(data_path):
        """Train ML model"""
        # Implementation
        return model_path
    
    @task
    def evaluate_model(model_path):
        """Evaluate model performance"""
        # Implementation
        return metrics
    
    # Define dependencies
    data = load_data()
    model = train_model(data)
    evaluate_model(model)

# Instantiate DAG
training_dag = training_pipeline()
```

## Task Dependencies

Three ways to define dependencies:

### 1. Decorator-based (Modern)
```python
@task
def task1():
    pass

@task
def task2(result_from_task1):
    pass

task1() >> task2()
```

### 2. Operator-based
```python
task1 = PythonOperator(python_callable=func1)
task2 = PythonOperator(python_callable=func2)
task1 >> task2
```

### 3. Set operators
```python
task1 >> [task2, task3]  # task1 then task2 and task3 in parallel
[task2, task3] >> task4  # both complete, then task4
```

## Scheduling

### Schedule Intervals

```python
# Cron expression
schedule_interval="0 0 * * *"  # Daily at midnight

# Predefined frequencies
schedule_interval="@hourly"    # Every hour
schedule_interval="@daily"     # Every day
schedule_interval="@weekly"    # Every week
schedule_interval="@monthly"   # Every month

# Custom timedelta
from datetime import timedelta
schedule_interval=timedelta(hours=6)  # Every 6 hours
```

## Setup & Installation

### Using Docker Compose

```bash
# Start Airflow
docker-compose up

# Access UI at http://localhost:8080
# Default: admin / airflow
```

### Manual Installation

```bash
# Install Airflow
pip install apache-airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start scheduler
airflow scheduler

# Start webserver (separate terminal)
airflow webserver
```

## Airflow UI

### Key Features

- **DAG View**: Visualize pipeline structure
- **Graph View**: See task dependencies
- **Tree View**: Timeline of executions
- **Gantt Chart**: Task duration and parallelism
- **Logs**: View task execution logs
- **Admin Panel**: Configure connections, variables, pools

### DAG Controls

- **Pause/Unpause**: Enable/disable scheduling
- **Trigger**: Manually trigger DAG run
- **Clear**: Reset task status
- **Refresh**: Reload DAG definition

## Data Exchange Between Tasks (XCom)

Share data between tasks:

```python
@task
def task1():
    return {"key": "value"}

@task
def task2(data):  # Automatically receives XCom from task1
    print(data)

task1() >> task2()
```

Manual XCom:
```python
context["task_instance"].xcom_push(key="result", value=123)
result = context["task_instance"].xcom_pull(task_ids="previous_task")
```

## Error Handling & Retries

```python
@dag(
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
    }
)
def my_dag():
    @task(
        on_failure_callback=send_alert,
        on_success_callback=log_success
    )
    def my_task():
        pass
```

## Monitoring

### Logs Access

```bash
# View logs for specific task
airflow logs -d training_pipeline -t load_data

# Stream logs
airflow logs -d training_pipeline -t load_data --follow
```

### Metrics & Health

- Task duration metrics
- Success/failure rates
- Execution frequency analysis
- Resource utilization

## Configuration

### airflow.cfg

```ini
[core]
dags_folder = /workspace/dags
max_active_runs_per_dag = 2
parallel_task_instances = 4

[database]
sql_alchemy_conn = sqlite:////workspace/airflow.db

[webserver]
base_log_folder = /workspace/logs
```

### Environment Variables

```bash
AIRFLOW_HOME=/workspace
AIRFLOW__CORE__DAGS_FOLDER=/workspace/dags
AIRFLOW__CORE__LOAD_EXAMPLES=False
```

## Features

✓ Declarative pipeline definition (DAG)  
✓ Rich UI for monitoring  
✓ Scalable task execution  
✓ Flexible scheduling  
✓ Error handling & retries  
✓ Data exchange between tasks  
✓ Rich operator ecosystem  
✓ Extensible with custom operators  

## Best Practices

1. **Idempotency**: Tasks should be re-runnable
2. **Modularity**: Small, reusable tasks
3. **Monitoring**: Add alerting for failures
4. **Testing**: Unit test DAGs
5. **Documentation**: Document task purposes
6. **Variable Management**: Use Airflow Variables
7. **Resource Limits**: Set CPU/memory limits

## DAG Validation

```bash
# Check DAG syntax
airflow dags list

# Dry run a DAG
airflow dags test training_pipeline

# Validate specific task
airflow tasks test training_pipeline load_data
```

## Triggering & Manual Runs

```bash
# Trigger DAG run
airflow dags trigger training_pipeline

# Trigger with configuration
airflow dags trigger training_pipeline --exec-date 2024-01-15

# List recent runs
airflow dags list-runs -d training_pipeline
```

## Integration Examples

### With Model Training
```python
@task
def train_model():
    # Model training logic
    return "model_path"

@task
def register_model(model_path):
    # Register in model registry (MLflow, etc)
    pass
```

### With Data Processing
```python
@task
def load_data():
    # Load from database/S3
    return data

@task
def preprocess(data):
    # Data cleaning and feature engineering
    return processed_data
```

### With Notifications
```python
from airflow.providers.email.operators.email import EmailOperator

notify = EmailOperator(
    task_id="notify_completion",
    to_emails=["ml-team@company.com"],
    subject="Training pipeline completed",
    html_content="Model training completed successfully"
)
```

## Troubleshooting

**Issue**: DAG not appearing in UI  
**Solution**: Place .py file in dags/ folder; restart scheduler

**Issue**: Tasks not executing**  
**Solution**: Check scheduler is running; verify dependencies

**Issue**: Memory issues  
**Solution**: Reduce parallel_task_instances; use pools

**Issue**: Scheduler not picking up DAG changes  
**Solution**: Restart scheduler; check dag_file_processor_interval

## Advanced Topics

- Custom Operators and Hooks
- Dynamic DAGs
- Branching and conditional logic
- SLA monitoring
- Pool management
- Kubernetes executor

## Monitoring Tools Integration

- Prometheus metrics export
- Datadog integration
- CloudWatch/GCP Cloud Monitoring
- Custom metrics via sensors

## References

- [Airflow Documentation](https://airflow.apache.org/)
- [Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Operators Reference](https://airflow.apache.org/docs/apache-airflow/stable/_api/)
