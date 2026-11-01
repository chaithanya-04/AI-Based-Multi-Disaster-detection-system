import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load training data
data = pd.read_csv("earthquake_training_data.csv")

X = data[["accel"]]
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred) * 100

print(f"Model trained successfully! Accuracy: {accuracy:.2f}%")

# Save model safely using joblib
joblib.dump(model, "earthquake_model.joblib")
print("Model saved as earthquake_model.joblib")
