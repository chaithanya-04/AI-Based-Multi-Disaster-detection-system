import serial
import joblib
import re

# Load trained model
model = joblib.load("flood_model.pkl")
print("AI Flood Detection Model Loaded")


ser = serial.Serial("COM4", 115200)
print("Connected to ESP32. Reading live data...\n")

while True:
    try:
        line = ser.readline().decode().strip()
        match = re.findall(r"Water Level:\s*(\d+)\s*\|\s*Voltage:\s*([\d.]+)", line)
        if match:
            level, volt = match[0]
            level = float(level)
            volt = float(volt)

            # Predict flood status
            pred = model.predict([[level, volt]])[0]
            if pred == 1:
                print(f"Flood Alert! Level={level:.0f}, Voltage={volt:.2f}")
            else:
                print(f"Safe | Level={level:.0f}, Voltage={volt:.2f}")
    except Exception as e:
        print("Error:", e)
