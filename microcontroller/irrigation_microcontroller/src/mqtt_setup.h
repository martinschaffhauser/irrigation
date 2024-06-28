#ifndef MQTT_SETUP_H
#define MQTT_SETUP_H

#include <PubSubClient.h>

extern const char *mqtt_server;
extern const char *mqtt_user;
extern const char *mqtt_password;
extern const char *mqtt_topic;
extern const int mqtt_port;

void setup_mqtt(PubSubClient &client);
void reconnect_mqtt(PubSubClient &client);
void callback(char *topic, byte *payload, unsigned int length);

#endif // MQTT_SETUP_H
