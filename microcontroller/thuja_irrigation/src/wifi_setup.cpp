#include "wifi_setup.h"
#include "globals.h"
#include <Arduino.h>
#include <ESP8266WiFi.h>

const char *ssid = SSID_NAME;
const char *password = PASSWORD;

void setup_wifi()
{
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}
