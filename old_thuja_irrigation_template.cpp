#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPUpdateServer.h>

const char *ssid = "wifi";
const char *password = "pass";
const char *wifi_hostname = "ESP_Thujen";
const char *mqtt_server = "192.168.28.2";
const char *mqttUser = "user";
const char *mqttPass = "pass";
const char *updateesphost = "esp-webupdate";

// webupdate stuff
ESP8266WebServer httpServer(80);
ESP8266HTTPUpdateServer httpUpdater;

// Initializes the espClient. You should change the espClient name if you have multiple ESPs running in your home automation system
WiFiClient espClient;
PubSubClient client(espClient);

// defining which pinout is going to control relay
const int relay = 4;                // is D2 on Wemos board, but 4 in Arduino IDE
const byte interruptPin = 5;        // is D1 on Wemos board, but 5 in Arduino IDE
volatile byte interruptCounter = 0; // all water flow measurement - Specifically, it directs the compiler to load the variable from RAM and not from a storage register, which is a temporary memory location where program variables are stored and manipulated. Under certain conditions, the value for a variable stored in registers can be inaccurate. A variable should be declared volatile whenever its value can be changed by something beyond the control of the code section in which it appears, such as a concurrently executing thread. In the Arduino, the only place that this is likely to occur is in sections of code associated with interrupts, called an interrupt service routine.
int numberOfInterrupts = 0;         // all water flow measurement
char desiredinterrupt[8];

// Don't change the function below. This functions connects your ESP8266 to your router
void setup_wifi()
{
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("WiFi connected - ESP IP address: ");
    Serial.println(WiFi.localIP());
}

// This functions is executed when some device publishes a message to a topic that your ESP8266 is subscribed to
// Change the function below to add logic to your program, so when a device publishes a message to a topic that
// your ESP8266 is subscribed you can actually do something
void callback(String topic, byte *message, unsigned int length)
{
    Serial.print("Message arrived on topic: ");
    Serial.print(topic);
    Serial.print(". Message: ");
    String messageTemp;

    for (int i = 0; i < length; i++)
    {
        Serial.print((char)message[i]);
        messageTemp += (char)message[i];
    }
    Serial.println();

    //************************************************************
    // Add logic here
    //************************************************************
    // If a message is received on the topic garden/thuja, you check if the message is either on or off. Turns the relay GPIO according to the message
    if (topic == "garden/thujarelay")
    {
        Serial.print("changing thuja irrigation to ");
        if (messageTemp == "on")
        {
            digitalWrite(relay, HIGH);
            Serial.print("On");
        }
        else if (messageTemp == "off")
        {
            digitalWrite(relay, LOW);
            Serial.print("Off");
        }
    }

    // ask for the value of the interruptCounter
    if (topic == "garden/waterflow")
    {
        if (messageTemp == "readinterrupts")
        {
            static char interruptcount[5];
            itoa(numberOfInterrupts, interruptcount, 10); // convert int interruptCounter to char for PubSubClient
            client.publish("garden/waterflowresponse", interruptcount);
        }
        if (messageTemp == "reset")
        {
            numberOfInterrupts = 0;
        }
    }

    // send desired interruptcount
    if (topic == "garden/wateramount")
    {
        messageTemp.toCharArray(desiredinterrupt, 8);
        client.publish("garden/wateramountvalue", desiredinterrupt);
    }
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266
void reconnect()
{
    // Loop until we're reconnected
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        /*
         YOU MIGHT NEED TO CHANGE THIS LINE, IF YOU'RE HAVING PROBLEMS WITH MQTT MULTIPLE CONNECTIONS
         To change the ESP device ID, you will have to give a new name to the ESP8266.
         Here's how it looks:
           if (client.connect("ESP8266Client")) {
         You can do it like this:
           if (client.connect("ESP1_Office")) {
         Then, for the other ESP:
           if (client.connect("ESP2_Garage")) {
          That should solve your MQTT multiple connections problem
        */
        if (client.connect("ESP_Irrigation", mqttUser, mqttPass))
        {
            Serial.println("connected");
            // Subscribe or resubscribe to a topic
            // You can subscribe to more topics (to control more LEDs in this example)
            client.subscribe("garden/thujarelay");
            client.subscribe("garden/waterflow");
            client.subscribe("garden/wateramount");
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

// The setup function sets your ESP GPIOs to Outputs, starts the serial communication at a baud rate of 115200
// Sets your mqtt broker and sets the callback function
// The callback function is what receives messages and actually controls the LEDs
void setup()
{
    pinMode(relay, OUTPUT);
    pinMode(interruptPin, INPUT_PULLUP); // https://techtutorialsx.com/2016/12/11/esp8266-external-interrupts/
    attachInterrupt(digitalPinToInterrupt(interruptPin), handleInterrupt, CHANGE);
    digitalWrite(relay, LOW); // when esp powers on, the valve should be turned off - relay off

    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    // webupdate stuff
    MDNS.begin(updateesphost);

    httpUpdater.setup(&httpServer);
    httpServer.begin();

    MDNS.addService("http", "tcp", 80);
    Serial.printf("HTTPUpdateServer ready! Open http://%s.local/update in your browser\n", updateesphost);
}

// For this project, you don't need to change anything in the loop function. Basically it ensures that you ESP is connected to your broker
void loop()
{

    if (!client.connected())
    {
        reconnect();
    }
    if (!client.loop())
        client.connect("ESP_test");

    // webupdate stuff
    httpServer.handleClient();

    // read out the volatile byte interruptCounter so it does not overflow - translate it into int numberOfInterrupts
    if (interruptCounter > 0)
    {
        interruptCounter--;
        numberOfInterrupts++;
    }

    // leave irrigation on until desiredinterrupt is reached
    if (numberOfInterrupts >= atoi(desiredinterrupt))
    {
        digitalWrite(relay, LOW);
        numberOfInterrupts = 0;
    }
}

// Interrupt function for waterflow measurement
void ICACHE_RAM_ATTR handleInterrupt()
{ // Your interrupt service routines need to be in ram, not flash. Make them all look like this: void ICACHE_RAM_ATTR pulseCounter_1() * https://github.com/esp8266/Arduino/issues/4468
    interruptCounter++;
}
