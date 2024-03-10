// Arduino Uno
// Transmits and receives strings to/from PC 
// Rahul.S

// (c) www.xanthium.in 2021
// Tutorial - https://www.xanthium.in/Cross-Platform-serial-communication-using-Python-and-PySerial

#define ledPin 13  // LED connected to digital pin 13

void setup()
{
  Serial.begin(230400); // opens serial port, sets data rate to 230400 bps 8N1
  pinMode(ledPin, OUTPUT);  // initialize the digital pin as an output.
}

void loop()
{
  char TextToSend[] = " Hello From Arduino Uno";
  Serial.println(TextToSend); // sends a \n with text
  delay(5);

  // Read incoming data with a timeout
  String receivedText = readSerialString(1000); // Set your timeout in milliseconds

  // Print the received text
  if (receivedText.length() > 0) {
    Serial.print("Received: ");
    Serial.println(receivedText);

    // Check if the received text is "hi"
    if (receivedText.equals("hi")) {
      // Toggle the LED on pin 13
      digitalWrite(ledPin, !digitalRead(ledPin));
    }
  }
}

String readSerialString(int timeout)
{
  String inputString = "";
  unsigned long startTime = millis();

  while (millis() - startTime < timeout) {
    while (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {
        return inputString;
      } else {
        inputString += c;
      }
    }
  }

  return "";
}
