#include <Arduino.h>
#include <Servo.h>

// ----- Sensores LDR -----
const int SENSOR_EAST_PIN = 27;
const int SENSOR_WEST_PIN = 26;

// ----- Servo 180° -----
const int SERVO_GPIO          = 4;
const int SERVO_NEUTRAL_ANGLE = 90;
const int SERVO_MAX           = 180;
const int SERVO_MIN           =   0;

// ----- Calibração LDR -----
const int kalibracao = 42;

// ----- Parâmetros PID -----
double Kp = 0.01;
double Ki = 0.000001;
double Kd = 0.005;

// Limiar para parar o controle PID (erro “próximo de zero”)
const int ERROR_STOP_THRESHOLD  = 5;
// Limiar para reiniciar o controle se o erro aumentar muito
const int ERROR_START_THRESHOLD = 10;

double error = 0, lastError = 0;
double integral = 0, derivative = 0;
double pidOutput = 0;

// Tempo de amostragem
unsigned long lastTime;
const unsigned long sampleTime = 100; // ms

Servo solarServo;
double servoPosition = SERVO_NEUTRAL_ANGLE;
bool inControl = true;  // flag: estamos ajustando via PID?

void setup() {
  Serial.begin(9600);
  solarServo.attach(SERVO_GPIO);
  solarServo.write(servoPosition);
  lastTime = millis();
}

void loop() {
  unsigned long now = millis();
  if (now - lastTime < sampleTime) return;
  double dt = (now - lastTime) / 1000.0;
  lastTime = now;

  // 1) lê os LDRs e aplica calibração
  int e = analogRead(SENSOR_EAST_PIN);
  int w = analogRead(SENSOR_WEST_PIN) + kalibracao;

  // 2) calcula erro (buscamos e - w == 0)
  error = double(e - w);

  // 3) lógica de parada / reinício (histérese)
  if (inControl) {
    if (abs(error) <= ERROR_STOP_THRESHOLD) {
      inControl = false;
      integral = 0;         // limpa integral
    }
  } else {
    if (abs(error) >= ERROR_START_THRESHOLD) {
      inControl = true;
      lastError = error;    // reinicia derivativo
    }
  }

  // 4) se ainda estiver no modo de controle, faz PID
  if (inControl) {
    integral   += error * dt;
    derivative  = (error - lastError) / dt;
    pidOutput   = Kp * error + Ki * integral + Kd * derivative;
    lastError   = error;

    // atualiza posição e limita
    servoPosition += pidOutput;
    servoPosition = constrain(servoPosition, SERVO_MIN, SERVO_MAX);

    // escreve no servo
    solarServo.write(servoPosition);
  }
  // else: estamos no ponto ótimo, não movemos o servo

  // 5) debug
  Serial.print("E="); Serial.print(e);
  Serial.print(" W="); Serial.print(w);
  Serial.print(" err="); Serial.print(error);
  Serial.print(" out="); Serial.print(pidOutput);
  Serial.print(" pos="); Serial.print(servoPosition);
  Serial.print(" mode=");
  Serial.println(inControl ? "PID" : "STOP");

}
