#include <Arduino.h>
#include <NeoPixelConnect.h>

#define MAXIMUM_NUM_NEOPIXELS 5  // Número de LEDs; basta mudar aqui
#define SENSOR_PIN1 15          // Pino único do sensor Grove (trigger e echo)
#define SENSOR_PIN2 14
#define LED_PIN 6

// Inicializa a biblioteca NeoPixel (conforme o exemplo original)
NeoPixelConnect strip(LED_PIN, MAXIMUM_NUM_NEOPIXELS, pio0, 0);

// Parâmetros para a animação dos LEDs
const int fadeSteps = 100;
const int fadeDelay = 10;

// Parâmetros de distância (em centímetros)
const int minDistance = 5;
const int maxDistance = 9;

// Timeout para controle (a ajustar conforme necessário)
const unsigned long timeoutDuration = 15000; // tempo de timeout (não utilizado diretamente neste exemplo)
unsigned long lastDetectionTime = 0;

bool animating = false;
unsigned long animationStartTime = 0;

// Constante da velocidade do som (cm/µs)
const float SOUND_SPEED = 0.0343;

void setup() {
  // Configuração inicial do sensor e comunicação serial
  Serial.begin(115200);
  strip.neoPixelClear();
  strip.neoPixelShow();
}

/**
 * Função que verifica se um objeto é detectado dentro do intervalo de distância especificado.
 * Utiliza o sensor Grove ultrassônico, que opera com um único pino.
 */
bool isObjectDetected_1(int min, int thresholdDistance) {
  // Configura o pino como saída para enviar o pulso trigger
  pinMode(SENSOR_PIN1, OUTPUT);
  digitalWrite(SENSOR_PIN1, LOW);
  delayMicroseconds(2);
  digitalWrite(SENSOR_PIN1, HIGH);
  delayMicroseconds(10);  // Pulso de 10 µs
  digitalWrite(SENSOR_PIN1, LOW);

  // Muda o pino para entrada e mede a duração do pulso HIGH (echo)
  pinMode(SENSOR_PIN1, INPUT);
  unsigned long pulseDuration = pulseIn(SENSOR_PIN1, HIGH, 30000); // Timeout de 30 ms

  // Se não houver eco (timeout), retorna false
  if (pulseDuration == 0) {
    return false;
  }

  // Calcula a distância: (duração do pulso * velocidade do som) / 2
  int distance = pulseDuration * SOUND_SPEED / 2;

  // Para debug: imprime a distância medida no Serial Monitor
  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Retorna verdadeiro se a distância estiver dentro do intervalo (maior que min e menor ou igual a thresholdDistance)
  return (distance > min && distance <= thresholdDistance);
}
bool isObjectDetected_2(int min, int thresholdDistance) {
  // Configura o pino como saída para enviar o pulso trigger
  pinMode(SENSOR_PIN2, OUTPUT);
  digitalWrite(SENSOR_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(SENSOR_PIN2, HIGH);
  delayMicroseconds(10);  // Pulso de 10 µs
  digitalWrite(SENSOR_PIN2, LOW);

  // Muda o pino para entrada e mede a duração do pulso HIGH (echo)
  pinMode(SENSOR_PIN2, INPUT);
  unsigned long pulseDuration = pulseIn(SENSOR_PIN2, HIGH, 30000); // Timeout de 30 ms

  // Se não houver eco (timeout), retorna false
  if (pulseDuration == 0) {
    return false;
  }

  // Calcula a distância: (duração do pulso * velocidade do som) / 2
  int distance = pulseDuration * SOUND_SPEED / 2;

  // Para debug: imprime a distância medida no Serial Monitor
  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Retorna verdadeiro se a distância estiver dentro do intervalo (maior que min e menor ou igual a thresholdDistance)
  return (distance > min && distance <= thresholdDistance);
}
/**
 * Função que acende os LEDs sequencialmente com um efeito de fade-in.
 */
void fadeInAllLEDsSequentially() {
  for (int pos = 0; pos < MAXIMUM_NUM_NEOPIXELS; pos++) {
    for (int step = 0; step <= fadeSteps; step++) {
      int brightness = map(step, 0, fadeSteps, 0, 255);
      // Define a mesma intensidade para os três canais (branco)
      strip.neoPixelSetValue(pos, brightness, brightness, brightness);
      strip.neoPixelShow();
      delay(fadeDelay);
    }
  }
}

/**
 * Função para resetar os LEDs e finalizar a animação.
 */
void resetLEDs() {
  strip.neoPixelClear();
  strip.neoPixelShow();
  animating = false;
  Serial.println("Timed out - LEDs reset.");
}

void loop() {
  // Se não estiver em animação e um objeto for detectado no intervalo definido
  if (!animating && isObjectDetected_1(minDistance, maxDistance)) {
    animating = true;
    fadeInAllLEDsSequentially();
  }

  // Caso esteja em animação e um objeto seja detectado num intervalo diferente (exemplo: outro sensor ou condição),
  // o que no exemplo original está definido para usar um intervalo de 15 a 20 cm:
  if (animating && isObjectDetected_2(15, 20)) {
    resetLEDs();
  }
}
