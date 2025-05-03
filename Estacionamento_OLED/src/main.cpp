#include <Arduino.h>
#include <Wire.h>
#include <VL53L0X.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- Configurações do OLED ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define OLED_ADDRESS  0x3C

// --- Parâmetros dos sensores VL53L0X ---
#define NUM_SENSORS 6
// GPIOs usados para XSHUT de cada sensor
const uint8_t XSHUT_PINS[NUM_SENSORS] = {2, 3, 4, 5, 6, 7};
// Endereços I²C únicos atribuídos após init
const uint8_t ADDRESSES[NUM_SENSORS]  = {0x30, 0x31, 0x32, 0x33, 0x34, 0x35};

// Instâncias dos sensores
VL53L0X sensors[NUM_SENSORS];

// Controle de timing
unsigned long interval;
unsigned long previousMicros;

// OLED via I²C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Bitmap 16×16 para o ícone de estacionamento
const unsigned char parkingIcon[] PROGMEM = {
  0x00,0x00, 0x00,0x00, 0x07,0xE0, 0x0C,0x30,
  0x18,0x18, 0x30,0x0C, 0x7F,0xFC, 0xC0,0x03,
  0xC0,0x03, 0xC0,0x03, 0x7F,0xFC, 0x30,0x0C,
  0x18,0x18, 0x0C,0x30, 0x07,0xE0, 0x00,0x00
};

// Função para desenhar número de vagas no OLED
void display_vagas(int vagas) {
  display.clearDisplay();
  display.drawBitmap(0, 0, parkingIcon, 16, 16, SSD1306_WHITE);
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(20, 0);
  display.println("Estacionamento");
  display.setCursor(0, 20);
  display.println("Vagas Livres:");
  display.setTextSize(3);
  display.setCursor(0, 40);
  display.println(vagas);
  display.display();
}

void setup() {
  Serial.begin(115200);
  Serial.println("Inicializando 6 sensores VL53L0X...");

  // --- Configura I2C e mantém todos sensores em reset (XSHUT LOW) ---
  Wire.setSDA(8);
  Wire.setSCL(9);
  Wire.begin();
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    pinMode(XSHUT_PINS[i], OUTPUT);
    digitalWrite(XSHUT_PINS[i], LOW);
  }
  delay(10);

  // --- Inicializa OLED ---
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("Falha ao inicializar OLED");
    while (1);
  }
  display.clearDisplay();
  display.display();

  // --- Sequência de boot e atribuição de endereços em cada sensor ---
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    // Tira o sensor i do reset
    digitalWrite(XSHUT_PINS[i], HIGH);
    delay(10);

    sensors[i].setTimeout(500);
    // Aguarda até inicializar
    while (!sensors[i].init()) {
      Serial.print("Erro init sensor "); Serial.println(i);
      delay(100);
    }
    // Atribui endereço único e inicia leitura
    sensors[i].setAddress(ADDRESSES[i]);
    sensors[i].startReadRangeMillimeters();
    Serial.print("Sensor "); Serial.print(i);
    Serial.print(" iniciado em 0x"); Serial.println(ADDRESSES[i], HEX);
  }

  // --- LEDs de diagnóstico (como antes) ---
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(0, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(0, LOW);

  // --- Intervalo de leitura: 40 ms ---
  interval = 40UL * 1000UL;
  previousMicros = micros();
}

void loop() {
  unsigned long now = micros();
  if (now - previousMicros < interval) return;
  previousMicros = now;

  int vagasLivres = 0;
  // Para cada sensor, se distancia > 5 cm, conta como vaga livre
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    if (sensors[i].readRangeAvailable()) {
      float dist = sensors[i].readRangeMillimeters() * 1e-3;
      sensors[i].startReadRangeMillimeters();
      if (dist > 0.05) vagasLivres++;
    }
  }

  Serial.print("Vagas livres: ");
  Serial.println(vagasLivres);

  // Acende LED se todas as vagas estiverem ocupadas
  bool todasOcupadas = (vagasLivres == 0);
  digitalWrite(LED_BUILTIN, todasOcupadas);
  digitalWrite(0, todasOcupadas);

  // Atualiza o display
  display_vagas(vagasLivres);
}
