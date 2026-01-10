import numpy as np

def numpy_operations():
    # Create an array
    array1 = np.array([1, 2, 3, 4, 5])
    print("Original Array:", array1)

    # Add scalar
    array1 = array1 + 10
    print("Array + 10:", array1)

if __name__ == "__main__":
    numpy_operations()
