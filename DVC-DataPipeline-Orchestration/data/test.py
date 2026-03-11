# Run this once to generate data
import pandas as pd
df = pd.DataFrame({'feature1': [1, 2, 3], 'label': [0, 1, 0]})
df.to_csv('data/dataset.csv', index=False)