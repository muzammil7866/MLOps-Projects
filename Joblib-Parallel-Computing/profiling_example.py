# Note: memory_profiler needs to be installed via `pip install memory-profiler`
# And typically run with `python -m memory_profiler profiling_example.py` 
# or by decorating with @profile and running normally if the module is imported.

try:
    from memory_profiler import profile
except ImportError:
    print("memory_profiler module not found. Please install it using `pip install memory-profiler`")
    # Dummy decorator to prevent crash if not installed
    def profile(func):
        return func

@profile
def test_function():
    # Create a large list to consume memory
    data = [i for i in range(100000)]
    del data
    return "Done"

if __name__ == "__main__":
    test_function()
