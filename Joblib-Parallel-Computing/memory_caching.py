import joblib
import time
import os

# Create a cache directory
cache_dir = './cachedir'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

memory = joblib.Memory(cache_dir, verbose=0)

@memory.cache
def load_and_clean(x):
    print(f"Executing expensive operation for {x}...")
    time.sleep(1) # Simulate expensive work
    return x * x

def run_caching_example():
    start = time.time()
    print(f"Result 1: {load_and_clean(10)}")
    print(f"Time taken (1st run): {time.time() - start:.2f}s")
    
    start = time.time()
    print(f"Result 2: {load_and_clean(10)}")
    print(f"Time taken (2nd run - cached): {time.time() - start:.2f}s")

if __name__ == "__main__":
    run_caching_example()
    # Cleanup cache for demo purposes
    # joblib.memory.Memory.clear(memory)
