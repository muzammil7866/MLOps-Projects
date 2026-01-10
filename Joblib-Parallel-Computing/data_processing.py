def preprocess(line):
    # Placeholder for actual preprocessing logic
    return line.strip()

def data_preprocessor(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                yield preprocess(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")

if __name__ == "__main__":
    # Example usage
    file_path = "example_data.txt"
    # Create a dummy file for demonstration
    with open(file_path, "w") as f:
        f.write("line 1\nline 2\nline 3")
        
    for data in data_preprocessor(file_path):
        print(data)
