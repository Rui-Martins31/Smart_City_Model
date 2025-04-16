#include <Arduino.h>
#include <WiFi.h>                    // Se necessário para o Pico W
#include "pico/cyw43_arch.h"

#include <Wire.h>
#include <VL53L0X.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Definições do display OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define OLED_ADDRESS  0x3C

// Prototipação
void display_vagas(int vagas);

// Instância do sensor TOF (VL53L0X)
VL53L0X tof;
float distance = 0;

// Controle de tempo para atualizações
unsigned long interval;
unsigned long currentMicros, previousMicros;

// Instância do display OLED via I²C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Bitmap de 16x16 pixels para o ícone de estacionamento (exemplo)
const unsigned char parkingIcon[] PROGMEM = {
  0x00, 0x00,  // linha 0
  0x00, 0x00,  // linha 1
  0x07, 0xE0,  // linha 2
  0x0C, 0x30,  // linha 3
  0x18, 0x18,  // linha 4
  0x30, 0x0C,  // linha 5
  0x7F, 0xFC,  // linha 6
  0xC0, 0x03,  // linha 7
  0xC0, 0x03,  // linha 8
  0xC0, 0x03,  // linha 9
  0x7F, 0xFC,  // linha 10
  0x30, 0x0C,  // linha 11
  0x18, 0x18,  // linha 12
  0x0C, 0x30,  // linha 13
  0x07, 0xE0,  // linha 14
  0x00, 0x00   // linha 15
};

void setup() 
{
  // Inicializa o monitor serial para debug
  Serial.begin(115200);
  Serial.println("Inicializando...");

  // Configuração dos pinos I²C: defina os pinos que você usa para o seu display e sensor
  Wire.setSDA(8);
  Wire.setSCL(9);
  Wire.begin();

  // Inicializa o display OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("Falha ao inicializar o display OLED!");
    while (1);
  }
  display.clearDisplay();
  display.display();

  // Inicializa o sensor VL53L0X
  tof.setTimeout(500);
  while (!tof.init()) {
    Serial.println(F("Falha ao detectar/inicializar o VL53L0X!"));
    delay(100);
  }  
  // Inicia a primeira medição
  tof.startReadRangeMillimeters();  

  // Configura os pinos de LED para diagnóstico
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(0, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(0, LOW);

  // Intervalo de medição: 40 milissegundos (em microssegundos)
  interval = 40 * 1000;
  previousMicros = micros();
}

void loop() 
{
  currentMicros = micros();

  // Atualiza a leitura a cada "interval" microsegundos
  if (currentMicros - previousMicros >= interval) {
    previousMicros = currentMicros;

    if (tof.readRangeAvailable()) {
      distance = tof.readRangeMillimeters() * 1e-3; // converte mm para metros
    }
 
    // Inicia uma nova medição
    tof.startReadRangeMillimeters(); 

    Serial.print("Distância: ");
    Serial.print(distance, 3);
    Serial.println(" m");

    int vagas;
    // Se objeto detectado (distância <= 0.05 m), vagas = 0; senão, vagas = 1.
    if (distance <= 0.05) {
      digitalWrite(LED_BUILTIN, HIGH);
      digitalWrite(0, HIGH);
      vagas = 0;
    } else {
      digitalWrite(LED_BUILTIN, LOW);
      digitalWrite(0, LOW);
      vagas = 1;
    }
    
    // Atualiza o display exibindo o número de vagas livres
    display_vagas(vagas);
  }
}

void display_vagas(int vagas)
{
  display.clearDisplay();

  // Desenha o ícone de estacionamento
  display.drawBitmap(0, 0, parkingIcon, 16, 16, SSD1306_WHITE);

  // Exibe o título ao lado do ícone
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(20, 0);
  display.println("Estacionamento");

  // Exibe o subtítulo "Vagas Livres:"
  display.setCursor(0, 20);
  display.println("Vagas Livres:");

  // Exibe o número de vagas livres de forma dinâmica
  display.setTextSize(3);
  display.setCursor(0, 40);
  display.println(vagas);

  // Atualiza o display para mostrar o conteúdo desenhado
  display.display();
}
