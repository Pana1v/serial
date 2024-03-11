#include <ArduinoJson.h>

const int MAX_JSON_SIZE = 100;
char json_buffer[MAX_JSON_SIZE];

int accumulated_x = 0; // Variable to accumulate x values

void setup() {
  Serial.begin(921600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read data into a fixed-size buffer
    Serial.readBytesUntil('\n', json_buffer, MAX_JSON_SIZE);

    // Parse JSON data
    DynamicJsonDocument doc(MAX_JSON_SIZE);
    deserializeJson(doc, json_buffer);

    int x_value = doc["x"];
    int y_value = doc["y"];
    String cmd_value = doc["cmd"].as<String>();

    // Accumulate x values
    accumulated_x += x_value;

    // Create response JSON data with accumulated x value
    JsonObject response = doc.to<JsonObject>();
    response["x"] = accumulated_x;
    response["y"] = y_value;
    response["cmd"] = cmd_value;

    // Convert response JSON data to string
    serializeJson(response, json_buffer, MAX_JSON_SIZE);

    // Send response back to PC
    Serial.print(json_buffer);
    Serial.print('\n');

    // Print received data and accumulated x value
    Serial.printf("Received: x=%d, y=%d, cmd=%s, Accumulated x=%d\n", x_value, y_value, cmd_value.c_str(), accumulated_x);
  }
}
