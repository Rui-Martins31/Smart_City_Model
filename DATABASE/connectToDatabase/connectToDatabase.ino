#include <WiFi.h>
#include <WebServer.h>
#include "config.h"

#define SERVER_PORT 80

const char *ssid = WIFI_SSID;
const char *password = WIFI_PASSWORD;

int filledSlots = 0;

WebServer server(SERVER_PORT);

// HTML + CSS content
const char* htmlPage = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parking Slots</title>
  <meta http-equiv="refresh" content="5"> <!-- Auto-refresh every 5 seconds -->
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      text-align: center;
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1 {
      color: #333;
    }
    .slots {
      font-size: 24px;
      color: #007BFF;
      margin: 20px 0;
    }
    .footer {
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Parking Lot Status</h1>
    <div class="slots">Parking slots: %SLOTS%/6</div>
    <div class="footer">Updated every 5 seconds</div>
  </div>
</body>
</html>
)rawliteral";

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
  server.on("/", []() {
    //String response = "Parking slots: " + String(filledSlots) + "/6";
    //server.send(200, "text/plain", response);
    String response = htmlPage;
    response.replace("%SLOTS%", String(filledSlots));
    server.send(200, "text/html", response);
  });

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
