#include <Arduino.h>
#include <Servo.h>

Servo myServo;
#define SERVO_PIN 0  // GPIO 0

unsigned long interval = 40;
unsigned long last_cycle = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Attach with explicit pulse range
  myServo.attach(SERVO_PIN, 500, 2500); // 500-2500µs
  Serial.println("Servo attached");
}

void loop() {
  unsigned long now = millis();
  if (now - last_cycle > interval) {
    // Check if data is available in the Serial Monitor
    if (Serial.available() > 0) {
      Serial.read(); // Clear the input buffer

      // Move servo to 0 degrees
      Serial.println("Moving to 0 degrees");
      myServo.write(0);
      delay(2000); // Wait 2 seconds

      // Move servo to 90 degrees
      Serial.println("Moving to 90 degrees");
      myServo.write(90);
      //delay(2000); 
    }


  }
}