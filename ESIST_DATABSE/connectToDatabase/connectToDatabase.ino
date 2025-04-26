#include <WiFi.h>
#include "config.h"

const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

void setup() {
  // ESP32 as station
  WiFi.mode(WIFI_STA);

  // Start serial
  Serial.begin(115200);

  Serial.println();
  Serial.println("******************************************************");
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  // put your main code here, to run repeatedly:

}
