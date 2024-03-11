#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600);  // Set the baud rate for Serial1
}

void loop() {
  // Create a JSON document
  StaticJsonDocument<100> doc;
  
  // Add x, y, and cmd to the document
  doc["x"] = 42;
  doc["y"] = 21;
  doc["cmd"] = "example";

  // Serialize the JSON document to a string
  String jsonData;
  serializeJson(doc, jsonData);

  // Send data over Serial1
  Serial1.println(jsonData);

  delay(1000); // Adjust delay as needed
}
