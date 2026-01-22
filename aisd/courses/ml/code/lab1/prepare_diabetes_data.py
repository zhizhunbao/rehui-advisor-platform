"""
Prepare Diabetes Dataset for Lab 1
This script downloads and prepares the diabetes dataset from sklearn
and formats it with meaningful column names similar to Weka's version.
"""

import pandas as pd
from sklearn.datasets import load_diabetes
import numpy as np

print("Preparing diabetes dataset...")
print("-" * 80)

# Load diabetes dataset from sklearn
diabetes = load_diabetes()

# Create DataFrame with features
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)

# The sklearn diabetes dataset is for regression (predicting disease progression)
# We need to convert it to classification for the lab
# Create binary classes based on target median
target_median = np.median(diabetes.target)
df['class'] = (diabetes.target > target_median).astype(int)

# Display dataset info
print(f"Dataset shape: {df.shape}")
print(f"\nColumn names:")
print(df.columns.tolist())
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nClass distribution:")
print(df['class'].value_counts())
print(f"\nDataset statistics:")
print(df.describe())

# Save to CSV
output_file = 'diabetes.csv'
df.to_csv(output_file, index=False)
print(f"\n✓ Dataset saved to '{output_file}'")
print("-" * 80)

# Verify the saved file
df_verify = pd.read_csv(output_file)
print(f"\nVerification:")
print(f"  File: {output_file}")
print(f"  Shape: {df_verify.shape}")
print(f"  Columns: {len(df_verify.columns)}")
print(f"  Instances: {len(df_verify)}")
print("\n✓ Dataset ready for Lab 1!")
