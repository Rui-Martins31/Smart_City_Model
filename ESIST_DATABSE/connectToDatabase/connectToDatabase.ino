#include <WiFi.h>
#include <WebServer.h>
#include "config.h"

#define SERVER_PORT 80

const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

int filledSlots = 0;

WebServer server(SERVER_PORT);

void handleRoot() {
  String response = "Parking slots: " + String(filledSlots) + "/6";
  server.send(200, "text/plain", response);
}

void setup() {
  // ESP32 as station
  WiFi.mode(WIFI_STA);

  // Start serial
  Serial.begin(115200);
  while (!Serial) {;} // Wait for serial port to connect

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


  // Initialize API - Specify endpoint
  server.on("/", handleRoot);

  // Handle 404 (Not Found)
  server.onNotFound([]() {
    server.send(404, "text/plain", "Not Found");
  });

  server.begin();

}

void loop() {
  server.handleClient(); // Handle incoming client requests
  filledSlots = random(0, 6+1);
  delay(2000);

}
