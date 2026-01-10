from celery_tasks import add, simulate_heavy_task
import time

def trigger_tasks():
    print("Triggering tasks...")
    
    # Trigger addition task
    result_add = add.delay(4, 6)
    print(f"Added task triggered. Task ID: {result_add.id}")
    
    # Trigger heavy task
    result_heavy = simulate_heavy_task.delay(5)
    print(f"Heavy task triggered. Task ID: {result_heavy.id}")
    
    print("\nWaiting for results...")
    
    # Wait for results (blocking)
    print(f"Addition Result: {result_add.get(timeout=10)}")
    
    # Check status of heavy task
    while not result_heavy.ready():
        print("Heavy task is still running...")
        time.sleep(1)
        
    print(f"Heavy Task Result: {result_heavy.get()}")

if __name__ == "__main__":
    trigger_tasks()
