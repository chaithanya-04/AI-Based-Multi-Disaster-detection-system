import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

#Read and clean the raw CSV
# Adjust filename if needed
raw = pd.read_csv("flood_data.csv", header=None, names=["Raw"])

# Extract numeric values from lines like "Water Level: 1210 | Voltage: 1.02"
def extract_values(text):
    match = re.findall(r"Water Level:\s*(\d+)\s*\|\s*Voltage:\s*([\d.]+)", text)
    if match:
        level, volt = match[0]
        return float(level), float(volt)
    return None, None

cleaned = raw["Raw"].apply(lambda x: pd.Series(extract_values(str(x)), index=["Water Level", "Voltage"]))
data = cleaned.dropna()

print("Cleaned Data Preview:")
print(data.head())

#Label data (Flood if >1210) 
THRESHOLD = 1300
data["Label"] = data["Water Level"].apply(lambda x: 1 if x > THRESHOLD else 0)

print("\nLabel distribution:")
print(data["Label"].value_counts())

# --- Step 3: Train simple AI model ---
X = data[["Water Level", "Voltage"]]
y = data["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the trained model ---
joblib.dump(model, "flood_model.pkl")
print("Model saved as flood_model.pkl")
