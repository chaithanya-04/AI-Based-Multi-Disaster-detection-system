import pandas as pd

# Read your raw data 
df = pd.read_csv("mq2_raw.csv", header=None, names=["Voltage"])

def label_voltage(v):
    if v <= 0.70:
        return "Normal air"
    elif v <= 1.40:
        return "Smoke"
    else:
        return "Wildfire"

df["Label"] = df["Voltage"].apply(label_voltage)

df.to_csv("mq2_cleaned.csv", index=False)
print("Cleaned data saved to mq2_cleaned.csv")
print(df.head())
