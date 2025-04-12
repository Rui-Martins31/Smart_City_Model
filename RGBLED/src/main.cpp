#include <Arduino.h>

#define MAXIMUM_NUM_NEOPIXELS 5 // numero de leds, basta mudar aqui 
#include <NeoPixelConnect.h>

#define TRIG_PIN 11
#define ECHO_PIN 10
#define LED_PIN 6

NeoPixelConnect strip(LED_PIN, MAXIMUM_NUM_NEOPIXELS, pio0, 0);


const int fadeSteps = 100;
const int fadeDelay = 10;

// Distance thresholds para os ultrasonicos
const int minDistance = 5;
const int maxDistance = 9;

// Timeout 
const unsigned long timeoutDuration = 15000; // ajustar consoante o que formos utilizar 
unsigned long lastDetectionTime = 0;

bool animating = false;
unsigned long animationStartTime = 0;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(115200);
  strip.neoPixelClear();
  strip.neoPixelShow();
}

int isObjectDetected(int min, int thresholdDistance) {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  int distance = duration * 0.034 / 2;

  return (distance > min && distance <= thresholdDistance);
}

void fadeInAllLEDsSequentially() {
  for (int pos = 0; pos < MAXIMUM_NUM_NEOPIXELS; pos++) {
    for (int step = 0; step <= fadeSteps; step++) {
      int brightness = map(step, 0, fadeSteps, 0, 255);
      strip.neoPixelSetValue(pos, brightness, brightness, brightness);
      strip.neoPixelShow();
      delay(fadeDelay);
    }
  }
}

void resetLEDs() {
  strip.neoPixelClear();
  strip.neoPixelShow();
  animating = false;
  Serial.println("Timed out - LEDs reset.");
}

void loop() {
 

  // se n estiver em animaçao e um objeto for detectado
  if (!animating && isObjectDetected(minDistance, maxDistance)) {
    animating = true;
    fadeInAllLEDsSequentially();
  }

  // se estiver ainda a animar e detectar objeto no sensor oposto
  if (animating && isObjectDetected(15,20)) {
    resetLEDs();
  }
}
