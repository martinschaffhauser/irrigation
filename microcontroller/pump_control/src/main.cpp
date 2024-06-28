#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <TelnetStream.h>
#include "globals.h"
#include "wifi_setup.h"
#include "mqtt_setup.h"
#include "ota_setup.h"

// Definitions
#define LED_BUILTIN 2
const int relay = 4; // D2 on board!

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
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW); // when esp powers on, the valve should be turned off - relay off
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

  // MAIN CODE
}

// Function that runs control logic upon MQTT messages
void controlLogic(const String &topic, const String &message)
{
  // TESTING MQTT
  if (topic == "test/topic" || topic == "test/topic2")
  {
    if (message == "TURN_ON")
    {
      digitalWrite(LED_BUILTIN, LOW); // turn on led
      digitalWrite(relay, HIGH);
      TelnetStream.println("recvd test");
    }
    else if (message == "TURN_OFF")
    {
      digitalWrite(LED_BUILTIN, HIGH); // turn off led
      digitalWrite(relay, LOW);
      TelnetStream.println("recvd test");
    }
  }

  // LOGIC TO TURN ON/OFF PUMP
  if (topic == "irrigation/pump")
  {
    if (message == "pump_ON")
    {
      digitalWrite(relay, LOW);       // LOW is ON actually - relay is connected that way
      digitalWrite(LED_BUILTIN, LOW); // CAVE for that LED its LOW/HIGH is the other way round
      TelnetStream.println("Irrigation - cycling pump ON/OFF -> ON");
      Serial.println("Irrigation - cycling pump ON/OFF -> ON");
    }
    else if (message == "pump_OFF")
    {
      digitalWrite(relay, HIGH);       // HIGH is OFF actually - relay is connected that way
      digitalWrite(LED_BUILTIN, HIGH); // CAVE for that LED its LOW/HIGH is the other way round
      TelnetStream.println("Irrigation - cycling pump ON/OFF -> OFF");
      Serial.println("Irrigation - cycling pump ON/OFF -> OFF");
    }
  }
}
