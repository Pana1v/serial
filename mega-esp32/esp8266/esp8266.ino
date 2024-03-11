#include <ArduinoJson.h>
#include <SoftwareSerial.h>

SoftwareSerial espSerial(4,5);  // RX, TX (change pins as needed)

void setup() {
  Serial.begin(115200);
  espSerial.begin(9600);  // Set the baud rate for SoftwareSerial
}

void loop() {
  if (espSerial.available() > 0) {
    // Read data from SoftwareSerial
    String receivedData = espSerial.readStringUntil('\n');

    // Parse JSON data
    DynamicJsonDocument doc(100);
    deserializeJson(doc, receivedData);

    // Extract x, y, cmd values
    int x_value = doc["x"];
    int y_value = doc["y"];
    String cmd_value = doc["cmd"].as<String>();

    // Display received data
    Serial.println("Received: x=" + String(x_value) + ", y=" + String(y_value) + ", cmd=" + cmd_value);
  }
}
