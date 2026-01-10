from joblib import Parallel, delayed

def my_func(i):
    return i + i

def run_parallel_loop():
    data = range(1000)
    # n_jobs=4 means using 4 cores
    results = Parallel(n_jobs=4)(delayed(my_func)(i) for i in data)
    print(f"First 10 results: {results[:10]}")
    print(f"Total results: {len(results)}")

if __name__ == "__main__":
    run_parallel_loop()
