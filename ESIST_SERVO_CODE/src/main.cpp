#include <Arduino.h>
#include <NeoPixelConnect.h>
#include <Servo.h>

#define MAXIMUM_NUM_NEOPIXELS 5
#define LED_PIN 6

// Define cores RGB para o semáforo
#define COLOR_RED    255, 0, 0
#define COLOR_YELLOW 255, 100, 0 // Amarelo forte e brilhante
#define COLOR_GREEN  0, 255, 0
#define COLOR_OFF    0, 0, 0

NeoPixelConnect strip(LED_PIN, MAXIMUM_NUM_NEOPIXELS, pio0, 0);

Servo myServo[4];
#define SERVO_PIN 0
#define SERVO_NUM 4

// Máquina de estados do semáforo
typedef struct {
  int state;
  unsigned long tes, tis;
} fsm_t;

fsm_t semaforo;

// Estados do semáforo
enum {
  SEM_GREEN,
  SEM_YELLOW,
  SEM_RED
};

const unsigned long green_time = 5000;
const unsigned long yellow_time = 2000;
const unsigned long red_time = 5000;

void set_state(fsm_t &fsm, int new_state) {
  if (fsm.state != new_state) {
    fsm.state = new_state;
    fsm.tes = millis();
    fsm.tis = 0;
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Attach servos with explicit pulse range
  Serial.print("Attaching servos...\n");
  for (int i = 0; i < SERVO_NUM; i++)
  {
    myServo[i].attach(SERVO_PIN + i, 500, 2500); // 500-2500µs
    Serial.print(".");
  }
  /*
  for (int i = 0; i < SERVO_NUM; i++) {
    myServo[i].attach(SERVO_PIN + i, 500, 2500);
    myServo[i].write(0);
    Serial.print(".");
    delay(100);
  }*/

  Serial.println("\nServos attached!");

  strip.neoPixelClear();
  strip.neoPixelShow();

  set_state(semaforo, SEM_GREEN);
}

void rotateServo(int servo_index){
  // Move servo to 0 degrees
  Serial.println("Moving to 0 degrees");
  myServo[servo_index].write(0);
  delay(2000); // Wait 2 seconds

  // Move servo to 90 degrees
  Serial.println("Moving to 90 degrees");
  myServo[servo_index].write(90);
  //delay(2000); 
}

void loop() {
  unsigned long now = millis();
  semaforo.tis = now - semaforo.tes;

  switch (semaforo.state) {

    case SEM_GREEN:
      strip.neoPixelSetValue(2, COLOR_GREEN);
      strip.neoPixelSetValue(3, COLOR_OFF);
      strip.neoPixelSetValue(4, COLOR_OFF);
      strip.neoPixelShow();

      myServo[0].write(0);

      if (semaforo.tis >= green_time)
        set_state(semaforo, SEM_YELLOW);
      break;

    case SEM_YELLOW:
      strip.neoPixelSetValue(2, COLOR_OFF);
      strip.neoPixelSetValue(3, COLOR_YELLOW);
      strip.neoPixelSetValue(4, COLOR_OFF);
      strip.neoPixelShow();

      if (semaforo.tis >= yellow_time)
        set_state(semaforo, SEM_RED);
      break;

    case SEM_RED:
      strip.neoPixelSetValue(2, COLOR_OFF);
      strip.neoPixelSetValue(3, COLOR_OFF);
      strip.neoPixelSetValue(4, COLOR_RED);
      strip.neoPixelShow();

      myServo[0].write(90);

      if (semaforo.tis >= red_time)
        set_state(semaforo, SEM_GREEN);
      break;
  }

  delay(50);  // Pequeno delay para evitar atualizações excessivas
}