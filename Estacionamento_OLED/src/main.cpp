#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WebServer.h>

#include <VL53L0X.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "config.h"

// ======= CONFIGURAÇÃO DO OLED =======
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define OLED_ADDRESS  0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Ícone 16×16 para estacionamento
const unsigned char parkingIcon[] PROGMEM = {
  0x00,0x00, 0x00,0x00, 0x07,0xE0, 0x0C,0x30,
  0x18,0x18, 0x30,0x0C, 0x7F,0xFC, 0xC0,0x03,
  0xC0,0x03, 0xC0,0x03, 0x7F,0xFC, 0x30,0x0C,
  0x18,0x18, 0x0C,0x30, 0x07,0xE0, 0x00,0x00
};

// ======= CONFIGURAÇÃO DOS SENSORES =======
#define NUM_SENSORS 6
const uint8_t XSHUT_PINS[NUM_SENSORS] = {2, 3, 4, 5, 6, 7};
const uint8_t ADDRESSES[NUM_SENSORS]  = {0x30, 0x31, 0x32, 0x33, 0x34, 0x35};
VL53L0X sensors[NUM_SENSORS];

// ======= CONFIGURAÇÃO DO WEBSERVER =======
#define SERVER_PORT 80
WebServer server(SERVER_PORT);

// Quantas vagas estão livres
int vagasLivres = 0;

// Página HTML com placeholder
const char* htmlPage = R"rawliteral(
<!DOCTYPE html>
<html lang="pt">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Status Estacionamento</title>
<meta http-equiv="refresh" content="5">
<style>
  body { font-family: Arial, sans-serif; background:#f4f4f4;
         display:flex;justify-content:center;align-items:center;
         height:100vh;margin:0; }
  .box { text-align:center; background:#fff; padding:20px;
         border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1);}
  h1 { color:#333; }
  .slots { font-size:24px; color:#007BFF; margin:20px 0; }
  .foot { font-size:14px; color:#666; }
</style>
</head>
<body>
  <div class="box">
    <h1>Status Estacionamento</h1>
    <div class="slots">%SLOTS% vagas livres</div>
    <div class="foot">Atualiza a cada 5 s</div>
  </div>
</body>
</html>
)rawliteral";

void display_vagas(int v) {
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
  display.println(v);
  display.display();
}

void handleRoot() {
  String page = htmlPage;
  page.replace("%SLOTS%", String(vagasLivres));
  server.send(200, "text/html", page);
}

void setup() {
  Serial.begin(115200);
  delay(100);  // deixa o Serial estabilizar, mas não espera por monitor

  // 1) I2C + reset XSHUT
  Wire.setSDA(8);
  Wire.setSCL(9);
  Wire.begin();
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    pinMode(XSHUT_PINS[i], OUTPUT);
    digitalWrite(XSHUT_PINS[i], LOW);
  }
  delay(10);

  // 2) OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("ERRO: OLED não iniciou");
    // não bloqueia, apenas segue sem display
  } else {
    display.clearDisplay();
    display.display();
  }

  // 3) Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando Wi-Fi");
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 10000) {
    delay(300);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi OK, IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\nFalha Wi-Fi");
  }

  // 4) Sensores
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    digitalWrite(XSHUT_PINS[i], HIGH);
    delay(10);
    sensors[i].setTimeout(500);
    if (!sensors[i].init()) {
      Serial.printf("Erro init sensor %u\n", i);
    } else {
      sensors[i].setAddress(ADDRESSES[i]);
      sensors[i].startReadRangeMillimeters();
      Serial.printf("Sensor %u @0x%02X pronto\n", i, ADDRESSES[i]);
    }
  }

  // 5) WebServer
  server.on("/", handleRoot);
  server.onNotFound([](){ server.send(404, "text/plain", "Not Found"); });
  server.begin();
  Serial.println("WebServer iniciado na porta 80");
}

unsigned long lastMicros = micros();
const unsigned long interval = 40UL * 1000UL;  // 40 ms

void loop() {
  server.handleClient();

  unsigned long now = micros();
  if (now - lastMicros < interval) return;
  lastMicros = now;

  // lê sensores e conta livres
  int cnt = 0;
  for (uint8_t i = 0; i < NUM_SENSORS; i++) {
    if (sensors[i].readRangeAvailable()) {
      float d = sensors[i].readRangeMillimeters() * 1e-3;
      sensors[i].startReadRangeMillimeters();
      if (d > 0.05) cnt++;
    }
  }
  vagasLivres = cnt;

  // debug no Serial e display
  Serial.printf("Vagas livres: %d\n", vagasLivres);
  display_vagas(vagasLivres);
}
