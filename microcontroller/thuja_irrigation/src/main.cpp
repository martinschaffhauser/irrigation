#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <TelnetStream.h>
#include "globals.h"
#include "wifi_setup.h"
#include "mqtt_setup.h"
#include "ota_setup.h"

// Definitions
#define LED_BUILTIN 2
const int relay = 4; // CAVE: D4 == D4
// const byte interruptPin = 5;        // is D1 on Wemos board, but 5 in Arduino IDE
// volatile byte interruptCounter = 0; // all water flow measurement - Specifically, it directs the compiler to load the variable from RAM and not fr    om a storage register, which is a temporary memory location where program variables are stored and manipulated. Under certain conditions, the valu    e for a variable stored in registers can be inaccurate. A variable should be declared volatile whenever its value can be changed by something beyo    nd the control of the code section in which it appears, such as a concurrently executing thread. In the Arduino, the only place that this is likel    y to occur is in sections of code associated with interrupts, called an interrupt service routine.
// int numberOfInterrupts = 0;         // all water flow measurement
// char desiredinterrupt[8];

// Interrupt function for waterflow measurement
// void ICACHE_RAM_ATTR handleInterrupt()
// void IRAM_ATTR handleInterrupt() // since ICACHE_RAM_ATTR is deprecated
// {                                // Your interrupt service routines need to be in ram, not flash. Make them all look like this: void ICACHE_RAM_ATTR pulseCounter_1() * https://github.com/esp8266/Arduino/issues/4468
//   interruptCounter++;
// }

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
  // pinMode(interruptPin, INPUT_PULLUP); // https://techtutorialsx.com/2016/12/11/esp8266-external-interrupts/
  // attachInterrupt(digitalPinToInterrupt(interruptPin), handleInterrupt, CHANGE);
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
  // read out the volatile byte interruptCounter so it does not overflow - translate it into int numberOfInterrupts
  // if (interruptCounter > 0)
  // {
  //   interruptCounter--;
  //   numberOfInterrupts++;
  // }

  // // leave irrigation on until desiredinterrupt is reached
  // if (numberOfInterrupts >= atoi(desiredinterrupt))
  // {
  //   digitalWrite(relay, LOW);
  //   numberOfInterrupts = 0;
  // }
}

// Function that runs control logic upon MQTT messages
void controlLogic(const String &topic, const String &message)
{
  // MQTT testing
  // todo

  // thuja irrigation relay control
  if (topic == "irrigation/thuja")
  {
    if (message == "thuja_irrigation_ON")
    {
      digitalWrite(relay, LOW);        // pulling relay LOW is actually ON
      digitalWrite(LED_BUILTIN, HIGH); // CAVE for that LED its LOW/HIGH is the other way round
      TelnetStream.println("Turned Thuja Relay ON");
      Serial.println("Turned Thuja Relay ON");
    }
    else if (message == "thuja_irrigation_OFF")
    {
      digitalWrite(relay, HIGH);      // pulling relay HIGH is actually OFF
      digitalWrite(LED_BUILTIN, LOW); // CAVE for that LED its LOW/HIGH is the other way round
      TelnetStream.println("Turned Thuja Relay OFF");
      Serial.println("Turned Thuja Relay OFF");
    }
  }

  // ask for the value of the interruptCounter
  // if (topic == "irrigatioin/waterflow")
  // {
  //   if (message == "readinterrupts")
  //   {
  //     static char interruptcount[5];
  //     itoa(numberOfInterrupts, interruptcount, 10); // convert int interruptCounter to char for PubSubClient
  //     client.publish("irrigation/waterflowresponse", interruptcount);
  //   }
  //   if (message == "reset")
  //   {
  //     numberOfInterrupts = 0;
  //   }
  // }

  // send desired interruptcount
  // if (topic == "irrigation/wateramount")
  // {
  //   message.toCharArray(desiredinterrupt, 8);
  //   client.publish("irrigation/wateramountvalue", desiredinterrupt);
  // }
}
