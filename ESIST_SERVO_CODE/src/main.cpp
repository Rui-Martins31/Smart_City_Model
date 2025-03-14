// Adapted from Paulo Costa's PCA9685 example for Raspberry Pi Pico
// Using Platform.IO with Arduino framework
// Controls servo to rotate 90 degrees

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// PCA9685 default I2C address
Adafruit_PWMServoDriver ServoDriver = Adafruit_PWMServoDriver(0x40);

#define SERVO_FREQ 50  // Analog servos typically run at 50Hz
#define SERVO_NUM 0    // Using servo channel 0

// Pulse width constants for servo (adjusted for typical 500-2500µs range)
#define SERVO_MIN 102  // ~500µs at 4096 resolution (0 degrees)
#define SERVO_MAX 512  // ~2500µs at 4096 resolution (180 degrees)
#define SERVO_90  307  // ~1500µs at 4096 resolution (90 degrees)

unsigned long interval = 2000;  // 2-second interval between movements
unsigned long last_cycle;

// Function to detect PCA9685 presence
int find_ServoDriver(int addr) {
    Wire.beginTransmission(addr);
    Wire.write(0x00);  // MODE1 register
    Wire.write(0x80);  // MODE1_RESTART
    return !Wire.endTransmission();
}

void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    while (!Serial) delay(10);  // Wait for serial to connect

    // Initialize I2C (using GPIO 8 for SDA, GPIO 9 for SCL, which is default for Wire on I2C0)
    Wire.begin();  // No need for setSDA/setSCL

    // Check for PCA9685 connection
    while (!find_ServoDriver(0x40)) {
        Serial.println("No PCA9685 found ... check your connections");
        delay(200);
    }

    Serial.println("Found PCA9685");

    // Initialize PCA9685
    ServoDriver.begin();
    
    // Set oscillator frequency (adjust if needed based on your chip)
    ServoDriver.setOscillatorFrequency(27000000);  // Typical value, may need calibration
    ServoDriver.setPWMFreq(SERVO_FREQ);  // Set to 50Hz
    delay(10);

    // Initial position (0 degrees)
    ServoDriver.setPWM(SERVO_NUM, 0, SERVO_MIN);
}

void loop() {
    unsigned long now = millis();
    
    if (now - last_cycle > interval) {
        last_cycle = now;

        // Move to 0 degrees
        Serial.println("Moving to 0 degrees");
        ServoDriver.setPWM(SERVO_NUM, 0, SERVO_MIN);
        delay(2000);  // Wait 2 seconds

        // Move to 90 degrees
        Serial.println("Moving to 90 degrees");
        ServoDriver.setPWM(SERVO_NUM, 0, SERVO_90);
        delay(2000);  // Wait 2 seconds
    }
}