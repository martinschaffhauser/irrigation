#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <TelnetStream.h>
#include "globals.h"
#include "wifi_setup.h"
#include "mqtt_setup.h"
#include "ota_setup.h"

// definitions
#define LED_BUILTIN 2
const int relay = 4;                // is D2 on Wemos board, but 4 in Arduino IDE
const byte interruptPin = 5;        // is D1 on Wemos board, but 5 in Arduino IDE
volatile byte interruptCounter = 0; // all water flow measurement - Specifically, it directs the compiler to load the variable from RAM and not fr    om a storage register, which is a temporary memory location where program variables are stored and manipulated. Under certain conditions, the valu    e for a variable stored in registers can be inaccurate. A variable should be declared volatile whenever its value can be changed by something beyo    nd the control of the code section in which it appears, such as a concurrently executing thread. In the Arduino, the only place that this is likel    y to occur is in sections of code associated with interrupts, called an interrupt service routine.
int numberOfInterrupts = 0;         // all water flow measurement
char desiredinterrupt[8];

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

// Function that runs control logic upon MQTT messages
void controlLogic(const String &topic, const String &message)
{
  if (topic == "irrigation/thuja")
  {
    if (message == "thuja_irrigation_ON")
    {
      digitalWrite(relay, HIGH);
      TelnetStream.println("Turned Thuja Relay ON");
      Serial.println("Turned Thuja Relay ON");
    }
    else if (message == "thuja_irrigation_OFF")
    {
      digitalWrite(relay, LOW);
      TelnetStream.println("Turned Thuja Relay OFF");
      Serial.println("Turned Thuja Relay OFF");
    }
  }

  else if (topic == "test/topic")
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
}