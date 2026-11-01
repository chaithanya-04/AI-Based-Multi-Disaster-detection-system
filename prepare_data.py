# prepare_data.py
import pandas as pd

# Load the two files
normal = pd.read_csv("normal_data.csv", header=None, names=["accel"])
earthquake = pd.read_csv("earthquake_data.csv", header=None, names=["accel"])

# Label them
normal["label"] = 0  # Normal
earthquake["label"] = 1  # Earthquake

# Combine both datasets
data = pd.concat([normal, earthquake], ignore_index=True)

# Shuffle the rows randomly
data = data.sample(frac=1).reset_index(drop=True)

# Save final combined dataset
data.to_csv("earthquake_training_data.csv", index=False)

print("✅ Combined dataset saved as earthquake_training_data.csv")
print(data.head())
