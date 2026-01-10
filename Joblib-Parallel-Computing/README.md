# Joblib Parallel Computing Experiments

This project explores various techniques for optimizing Python code performance, focusing on parallel computing and memory management using `joblib`.

## Business Goals Achieved
- **Performance Optimization**: Demonstrated reduction in execution time for heavy computational tasks using parallel processing.
- **Scalability**: Implemented patterns that allow data processing pipelines to scale with available CPU cores.
- **Resource Efficiency**: Utilized memory caching to avoid redundant re-computation of expensive function calls, saving both time and compute resources.
- **Profiling & Monitoring**: Integrated memory profiling to identify bottlenecks and optimize memory usage.

## Files Description

- `parallel_loops.py`: Demonstrates how to distribute simple loops across multiple CPU cores using `joblib.Parallel`.
- `memory_caching.py`: Shows how to cache function results to disk to speed up subsequent calls with the same inputs using `joblib.Memory`.
- `ml_pipeline.py`: A basic example of constructing a Scikit-learn machine learning pipeline.
- `data_processing.py`: Contains generator-based data processing patterns for handling large files efficiently.
- `numpy_ops.py`: Basic Numpy array manipulations.
- `pandas_processing.py`: Efficient operations on Pandas Series.
- `profiling_example.py`: Demonstrates how to profile memory usage of a function using `memory_profiler`.

## How to Run
Ensure you have the necessary dependencies installed:
```bash
pip install joblib numpy pandas scikit-learn memory-profiler
```

Run individual scripts:
```bash
python parallel_loops.py
python memory_caching.py
```
