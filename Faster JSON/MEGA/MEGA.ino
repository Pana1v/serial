#include <ArduinoJson.h>

StaticJsonDocument<900> incoming;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  while (!Serial1);
}

void loop() {
  // Wait for incoming JSON data
  if (Serial1.available() == 0) return;

  // Deserialize and process incoming JSON data
  DeserializationError error = deserializeJson(incoming, Serial1);

  if (error) {
    // Handle deserialization error
    Serial1.println("Arduino Mega Error: " + String(error.c_str()));
    Serial.println("Arduino Mega Error: " + String(error.c_str()));
  }
   else {
    // Print received JSON data to the Serial Monitor
    serializeJsonPretty(incoming, Serial1);
    Serial1.print('\n');
    serializeJsonPretty(incoming, Serial);
    Serial.print('\n');
  }
}
