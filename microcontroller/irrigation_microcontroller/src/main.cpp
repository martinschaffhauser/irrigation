#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <TelnetStream.h>
#include "globals.h"
#include "wifi_setup.h"
#include "mqtt_setup.h"
#include "ota_setup.h"

#define LED_BUILTIN 2

void setup()
{
  Serial.begin(115200);
  setup_wifi();

  // TelnetStream Setup
  TelnetStream.begin();

  // OTA setup
  setup_ota();

  // MQTT setup
  setup_mqtt(client);

  // Pin Setup
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // HIGH for builtin led is actually off!
}

void loop()
{
  // Start TelnetStream
  switch (TelnetStream.read())
  {
  case 'R':
    TelnetStream.stop();
    delay(100);
    ESP.reset();
    break;
  case 'C':
    TelnetStream.println("bye bye");
    TelnetStream.flush();
    TelnetStream.stop();
    break;
  }

  // Start OTA handler
  ArduinoOTA.handle();

  // MQTT handling
  if (!client.connected())
  {
    reconnect_mqtt(client);
  }
  client.loop();

  // Your main code here
  // TelnetStream.println("=== main code loop is running ===");
}

// Function to control the LED upon MQTT messages
void controlLED(const String &message)
{
  if (message == "TURN_ON")
  {
    digitalWrite(LED_BUILTIN, LOW); // Turn the LED on
  }
  else if (message == "TURN_OFF")
  {
    digitalWrite(LED_BUILTIN, HIGH); // Turn the LED off
  }
}