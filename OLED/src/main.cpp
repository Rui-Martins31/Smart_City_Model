#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Definições do display OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

// Instância do display OLED via I²C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Bitmap de 16x16 pixels para o símbolo de estacionamento (exemplo)
// Esse desenho é apenas ilustrativo e pode ser alterado conforme necessário.
// Cada byte representa 8 pixels; utilize ferramentas on-line ou editores de bitmap para criar o seu.
const unsigned char parkingIcon[] PROGMEM = {
  0x00, 0x00,  // linha 0
  0x00, 0x00,  // linha 1
  0x07, 0xE0,  // linha 2: 0000 0111 1110 0000
  0x0C, 0x30,  // linha 3: 0000 1100 0011 0000
  0x18, 0x18,  // linha 4: 0001 1000 0001 1000
  0x30, 0x0C,  // linha 5: 0011 0000 0000 1100
  0x7F, 0xFC,  // linha 6: 0111 1111 1111 1100
  0xC0, 0x03,  // linha 7: 1100 0000 0000 0011
  0xC0, 0x03,  // linha 8
  0xC0, 0x03,  // linha 9
  0x7F, 0xFC,  // linha 10
  0x30, 0x0C,  // linha 11
  0x18, 0x18,  // linha 12
  0x0C, 0x30,  // linha 13
  0x07, 0xE0,  // linha 14
  0x00, 0x00   // linha 15
};

void setup() {
  Serial.begin(115200);
  

  // Inicializa o barramento I²C (os pinos padrão para o Arduino Mbed Core na Pico são GP4 - SDA e GP5 - SCL)
  Wire.begin();

  // Inicializa o display OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("Falha ao inicializar o display OLED!");
    while (1); // Caso não consiga inicializar, trava aqui.
  }
  
  display.clearDisplay();

  // Desenha o ícone de estacionamento
  // Parâmetros: x, y, ponteiro para o bitmap, largura, altura, cor
  display.drawBitmap(0, 0, parkingIcon, 16, 16, SSD1306_WHITE);

  // Exibe um título ou legenda
  display.setTextSize(1);              // Texto menor para o título
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(20, 0);            // Posiciona o texto ao lado do ícone
  display.println("Estacionamento");

  // Exibe um subtítulo, por exemplo, "Vagas Livres:"
  display.setTextSize(1);
  display.setCursor(0, 20);
  display.println("Vagas Livres:");

  // Exibe o número de vagas livres – ajuste o valor conforme a sua aplicação
  display.setTextSize(2);
  display.setCursor(0, 40);
  display.println("1");  // Exemplo: 12 vagas livres

  // Atualiza o display para mostrar o conteúdo desenhado
  display.display();
}

void loop() {
  // O loop não precisa executar nada para este exemplo.
}
