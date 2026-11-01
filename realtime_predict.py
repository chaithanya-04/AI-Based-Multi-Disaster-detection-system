import joblib
import serial
import time
import numpy as np

# Load trained model
model = joblib.load('earthquake_model.joblib')

# Connect to ESP32 (make sure COM port is correct)
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)
print(" Connected to ESP32. Monitoring...")

while True:
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode().strip()
            if line:
                accel = float(line)

                # Manual condition for Normal range
                if 1.03 <= accel <= 1.06:
                    print(f"Normal: {accel:.2f}")
                    ser.write(b'0')  # turn OFF buzzer/LED
                    continue

                # Otherwise, use AI prediction
                X = np.array([[accel]])
                prediction = model.predict(X)

                if prediction == 1:
                    print(f"EARTHQUAKE DETECTED! Accel: {accel:.2f}")
                    ser.write(b'1')  # turn ON buzzer/LED
                else:
                    print(f"Normal: {accel:.2f}")
                    ser.write(b'0')  # turn OFF buzzer/LED

            time.sleep(0.1)

        except Exception as e:
            print("Error:", e)
