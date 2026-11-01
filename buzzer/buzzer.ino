#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
const int buzzer = 5;   // or LED pin
float accelValue = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(buzzer, OUTPUT);

  byte status = mpu.begin();
  while (status != 0) {
    Serial.println("MPU6050 not connected...");
    delay(1000);
  }

  Serial.println("MPU6050 ready!");
}

void loop() {
  mpu.update();
  accelValue = mpu.getAccZ(); // choose axis as needed
  Serial.println(accelValue);
  delay(500);

  if (Serial.available()) {
    char signal = Serial.read();
    if (signal == '1') {
      digitalWrite(buzzer, HIGH); // quake detected
    } else if (signal == '0') {
      digitalWrite(buzzer, LOW);  // normal
    }
  }
}
