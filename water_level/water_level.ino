const int waterSensor = 34;
const int buzzer = 5;

void setup() {
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);
  digitalWrite(buzzer, LOW);
  Serial.println("🌊 Flood Detection System Initialized...");
}

void loop() {
  int sensorValue = analogRead(waterSensor);
  float voltage = sensorValue * (3.3 / 4095.0);

  Serial.print("Water Level: ");
  Serial.print(sensorValue);
  Serial.print(" | Voltage: ");
  Serial.println(voltage, 2);

  if (sensorValue > 1200) {
    Serial.println("⚠️ Flood Alert! High Water Level Detected!");
    digitalWrite(buzzer, HIGH);
  } else {
    digitalWrite(buzzer, LOW);
  }

  delay(1000);
}
