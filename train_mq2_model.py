import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Load the cleaned data
df = pd.read_csv("mq2_cleaned.csv")

# Features and labels
X = df[["Voltage"]]
y = df["Label"]

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
with open("mq2_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("\n✅ Model saved as mq2_model.pkl")

# Example test
test_voltage = 1.40
prediction = model.predict([[test_voltage]])[0]
print(f"\nTest Voltage: {test_voltage:.2f} V → Prediction: {prediction}")
