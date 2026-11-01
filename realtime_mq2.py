import serial
import joblib
import time
import re

# --- Load trained model ---
model = joblib.load("mq2_model.pkl")
print("Model loaded successfully!")

# --- Connect to ESP32 / Arduino ---
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)
print("Connected to sensor device... Reading live data.\n")

while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        # Ignore any header or junk lines
        if "Voltage" not in line:
            continue

        # Extract voltage value using regex
        match = re.search(r"Voltage:\s*([\d.]+)", line)
        if match:
            voltage = float(match.group(1))

            # --- AI model prediction ---
            prediction = model.predict([[voltage]])[0]

            # --- Safety override ---
            if voltage > 1.40:
                prediction = "Wildfire"
            elif 0.9 < voltage <= 1.39:
                prediction = "Smoke"
            elif 0.45 <= voltage <= 0.9:
                prediction = "Normal air"
            else:
                prediction = "Very clean air"

            print(f"Voltage: {voltage:.2f} V → {prediction}")

        else:
            print("Could not extract voltage from:", line)

    except ValueError:
        print("Invalid data received:", line)
    except KeyboardInterrupt:
        print("\nStopped by user.")
        break

ser.close()
