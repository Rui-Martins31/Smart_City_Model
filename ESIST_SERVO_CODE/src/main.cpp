#include <Arduino.h>
#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Aguarda a conexão com a serial (opcional)

  Serial.println("Iniciando teste do servo...");

  // Conecta o servo ao GPIO 4
  myServo.attach(4);  // ⬅️ Aqui está o teu pino
}

void loop() {
  Serial.println("Posição: 0°");
  myServo.write(0);
  delay(2000);

  Serial.println("Posição: 90°");
  myServo.write(90);
  delay(2000);

  Serial.println("Posição: 180°");
  myServo.write(180);
  delay(2000);
}
