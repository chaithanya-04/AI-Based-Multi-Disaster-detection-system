# AI-Based Multi-Disaster detection system

A low-cost IoT + machine learning prototype that detects **earthquakes**, **wildfires** and **floods** in real time. An ESP32 reads sensor data and streams it over serial to a Python script, where a trained ML model classifies the readings and raises an alert (and triggers a buzzer where applicable).

> **⚠️ Disclaimer:** This is a **demonstration / prototype model** built for academic purposes. It uses small datasets collected in a lab setup (a hobby-grade accelerometer, a gas sensor and a water level sensor) and simulated events such as shaking the sensor, burning paper or filling a container with water. It is **not** a certified or reliable disaster warning system and must **not** be used for real safety decisions.

## Features

| Disaster   | Sensor                  | ML Model                                  | Output                                                   |
| ---------- | ----------------------- | ----------------------------------------- | -------------------------------------------------------- |
| Earthquake | MPU6050 (accelerometer) | Random Forest (`earthquake_model.joblib`) | "EARTHQUAKE DETECTED" + buzzer ON/OFF sent back to ESP32 |
| Wildfire   | MQ-2 gas/smoke sensor   | Random Forest (`mq2_model.pkl`)           | Normal air / Smoke / Wildfire                            |
| Flood      | Water level sensor      | Logistic Regression (`flood_model.pkl`)   | Safe / Flood Alert                                       |

## Hardware Required

- ESP32 development board
- MPU6050 accelerometer/gyro module
- MQ-2 gas/smoke sensor
- Analog water level sensor
- Buzzer (or LED)
- Jumper wires, breadboard, USB cable

### Pin Connections

| Component          | ESP32 Pin                       |
| ------------------ | ------------------------------- |
| Buzzer / LED       | GPIO 5                          |
| MQ-2 (AO)          | GPIO 34                         |
| Water level sensor | GPIO 34                         |
| MPU6050 (SDA/SCL)  | Default I2C (GPIO 21 / GPIO 22) |

> MQ-2 and the water sensor share GPIO 34 because each sensor is flashed and run as a separate setup.

## Software Required

- Arduino IDE with ESP32 board support
- Arduino library: `MPU6050_light`
- Python 3.8+
- Python packages: see `requirements.txt`

```bash
pip install -r requirements.txt
```

## Project Structure

```
major/
├── buzzer/buzzer.ino            # ESP32 sketch: earthquake sensor (MPU6050 + buzzer)
├── mq2test/mq2test.ino          # ESP32 sketch: wildfire sensor (MQ-2)
├── water_level/water_level.ino  # ESP32 sketch: flood sensor
│
├── prepare_data.py              # Earthquake: combine normal + earthquake CSVs
├── train_model.py               # Earthquake: train Random Forest
├── realtime_predict.py          # Earthquake: live prediction + buzzer control
│
├── clean_data.py                # Wildfire: label raw voltage readings
├── train_mq2_model.py           # Wildfire: train Random Forest
├── realtime_mq2.py              # Wildfire: live prediction
│
├── flood_ai_train.py            # Flood: parse data + train Logistic Regression
├── flood_ai_realtime.py         # Flood: live prediction
│
├── *.csv                        # Datasets
└── *.pkl / *.joblib             # Trained models
```

## How It Works

1. The ESP32 reads its sensor and prints values over serial at 115200 baud.
2. A Python script reads the serial stream (default port `COM4`).
3. The trained model classifies each reading.
4. The result is printed to the console. For the earthquake system, Python also writes `1` or `0` back to the ESP32 to switch the buzzer on or off.

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd major
```

### 2. (Optional) Retrain the models

Pre-trained models are included, so you can skip this step.

```bash
# Earthquake
python prepare_data.py
python train_model.py

# Wildfire
python train_mq2_model.py

# Flood
python flood_ai_train.py
```

### 3. Run the system

For every system the first steps are the same:

1. Open the Arduino IDE and load the sketch for the sensor you want to use.
2. Select the ESP32 board and the correct COM port, then upload. Press the **BOOT** button on the ESP32 if the upload does not start.
3. Wait for the ESP32 to reset, then **close the Arduino IDE / Serial Monitor** (it would otherwise hold the COM port).
4. Open a terminal and go to the project folder.
5. Run the matching Python script:

| System     | Sketch                        | Command                       | How to test                                                                                             |
| ---------- | ----------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------- |
| Earthquake | `buzzer/buzzer.ino`           | `python realtime_predict.py`  | Tilt or shake the MPU6050; a warning is printed and the buzzer sounds                                   |
| Wildfire   | `mq2test/mq2test.ino`         | `python realtime_mq2.py`      | Bring a lit paper or incense stick near the MQ-2; output changes between normal air, smoke and wildfire |
| Flood      | `water_level/water_level.ino` | `python flood_ai_realtime.py` | Slowly fill a container with water around the sensor; a flood alert appears past the threshold          |

> **Note:** The scripts use `COM4` (Windows). On Linux/macOS change it to something like `/dev/ttyUSB0`, or on Windows to whichever COM port your ESP32 uses (Arduino IDE → Tools → Port).

## Thresholds Used

- **Wildfire (MQ-2 voltage):** below 0.8 V normal, 0.8–1.40 V smoke, above 1.40 V wildfire
- **Flood (ADC value):** alert above ~1200–1300 (tune to your sensor and container)
- **Earthquake:** accelerometer readings between 1.03 and 1.06 are treated as normal; others go to the model

Tune these values for your own sensors and environment.

## From Demo to Real Life

This prototype shows the core idea. A real deployment would need the following.

### Earthquake

- Use proper seismic sensors (MEMS seismometers or geophones) instead of a hobby MPU6050.
- Train on real seismic data (e.g. public datasets from USGS or IRIS) rather than shake tests.
- Detect the **P-wave** (the fast, weaker wave that arrives first) with algorithms such as STA/LTA, so a warning goes out seconds before the damaging S-waves arrive.
- Use many sensors in a network, so a single bump or passing truck is not mistaken for an earthquake.

### Wildfire

- Combine several sensors: smoke/particulate (PM2.5), CO, temperature, humidity, and optionally thermal or camera-based detection.
- Add satellite data (e.g. NASA FIRMS) and weather data (wind, humidity).
- Calibrate the MQ-2 and account for its warm-up time, drift and sensitivity to humidity.
- Power nodes with solar and a battery, and connect them over LoRa for remote forest areas.

### Flood

- Use waterproof ultrasonic, radar or pressure-based water level sensors installed on rivers, drains or dams.
- Add rainfall gauges and flow sensors, and train models on historical river and rainfall data to **forecast** floods, not only detect them.
- Account for terrain, drainage and seasonal patterns.

### System-level

- **Connectivity:** replace USB serial with Wi-Fi, LoRaWAN, GSM or NB-IoT, sending data via MQTT to a cloud server.
- **Edge + cloud:** run lightweight models on the device (TinyML) and heavier models in the cloud.
- **Alerts:** send SMS, mobile push notifications, sirens and dashboards, and integrate with disaster management authorities.
- **Reliability:** weatherproof enclosures, battery backup, self-diagnostics, and redundancy so one failed sensor does not break the system.
- **Validation:** test with large, real-world datasets and measure false alarm and missed detection rates before deployment.

## Future Improvements

- Add a web/mobile dashboard and SMS or push notifications
- Replace hard-coded COM port with auto-detection or a config file
- Collect larger datasets for more robust models
- Run inference directly on the ESP32 (TinyML) or send data over Wi-Fi/MQTT
