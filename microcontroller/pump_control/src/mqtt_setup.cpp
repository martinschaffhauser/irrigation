#include "mqtt_setup.h"
#include "globals.h"
#include <Arduino.h>
#include <PubSubClient.h>
#include <TelnetStream.h>

const char *mqtt_server = MQTT_BROKER_IP;
const char *mqtt_user = MQTT_USER;
const char *mqtt_password = MQTT_PASSWORD;
const char *mqtt_topic1 = MQTT_TOPIC_1;
const char *mqtt_topic2 = MQTT_TOPIC_2;
const int mqtt_port = 1883;

void setup_mqtt(PubSubClient &client)
{
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
}

void reconnect_mqtt(PubSubClient &client)
{
    // Loop until we're reconnected
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("pump_esp_client", mqtt_user, mqtt_password))
        {
            Serial.println("connected");
            // Once connected, subscribe to the topic
            client.subscribe(mqtt_topic1);
            client.subscribe(mqtt_topic2);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

// Declare the external function that runs in main.cpp
extern void controlLogic(const String &topic, const String &message);

void callback(char *topic, byte *payload, unsigned int length)
{
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    String message;
    for (unsigned int i = 0; i < length; i++)
    {
        message += (char)payload[i];
    }
    Serial.println(message);
    TelnetStream.print("MQTT Message: ");
    TelnetStream.println(message);

    // call the controlLogic function to execute what should happen upon certain message
    controlLogic(topic, message);
}
