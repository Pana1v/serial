#include <ArduinoJson.h>

int accumulated_x = 0; // Variable to accumulate x values

void setup() {
  Serial.begin(921600);
}

void loop() {
  if (Serial.available() > 0) {
    String json_data = Serial.readStringUntil('\n');

    // Parse JSON data
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, json_data);

    int x_value = doc["x"];
    int y_value = doc["y"];
    String cmd_value = doc["cmd"].as<String>();

    // Accumulate x values
    accumulated_x += x_value;

    // Create response JSON data with accumulated x value
    JsonObject response = doc.to<JsonObject>();
    response["accumulated_x"] = accumulated_x;

    // Convert response JSON data to string
    String response_data;
    serializeJson(response, response_data);

    // Send response back to PC
    Serial.print(response_data);
    Serial.print('\n');

    // Print received data and accumulated x value
    Serial.printf("Received: x=%d, y=%d, cmd=%s, Accumulated x=%d\n", x_value, y_value, cmd_value.c_str(), accumulated_x);
  }
}
