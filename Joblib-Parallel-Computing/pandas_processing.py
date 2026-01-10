import pandas as pd
import numpy as np

def my_func(data):
    data2 = data + 3
    return data2

def process_pandas_series():
    data = range(10000)
    series = pd.Series(data)
    
    print("Original Series Head:")
    print(series.head())
    
    result = my_func(series)
    
    print("\nProcessed Series Head:")
    print(result.head())

if __name__ == "__main__":
    process_pandas_series()
