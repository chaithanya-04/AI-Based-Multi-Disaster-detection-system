// --- ESP32 MQ2 Sensor for Fire Detection ---
// MQ2 AO → GPIO34
// MQ2 VCC → 5V
// MQ2 GND → GND
// Optional buzzer or LED → GPIO5

const int mq2Pin = 34;   // Analog input pin for MQ2 AO
const int buzzer = 5;    // Optional buzzer/LED pin

float voltage = 0.0;

// --- Thresholds ---
// Tune these based on your readings:
float smokeThreshold = 0.8;    // Mild smoke level
float fireThreshold  = 1.40;    // Strong fire/wildfire level

void setup() {
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);
  delay(1000);
  Serial.println("ADC Value, Voltage (V), Status");
}

void loop() {
  int adcValue = analogRead(mq2Pin);
  voltage = (adcValue / 4095.0) * 3.3;  // Convert ADC reading to voltage

  Serial.print(adcValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2);
  Serial.print("V → ");

  // --- Condition check ---
  if (voltage < smokeThreshold) {
    Serial.println("Normal air 🌿");
    digitalWrite(buzzer, LOW);
  }
  else if (voltage >= smokeThreshold && voltage < fireThreshold) {
    Serial.println("Smoke detected 💨");
    tone(buzzer, 1000, 200);   // short beep for smoke
  }
  else {
    Serial.println("🔥 Wildfire detected! 🔥");
    tone(buzzer, 2000, 800);   // long alert for wildfire
  }

  delay(1000);
}
