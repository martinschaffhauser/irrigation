from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import time

# Load environment variables from .env file
load_dotenv()

# Get the username and password from environment variables
mqtt_username = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Define the MQTT broker details
broker = "localhost"
port = 1883
topic = "test/topic"
client_id = "mqtt_publisher"
username = mqtt_username
password = mqtt_password

# Create a new MQTT client instance with the correct API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set the username and password for the MQTT client
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker, port)

# Publish messages to the topic
for i in range(5):
    message = f"Message {i+1}: now the logic that depends on this messag needs to start"
    result = client.publish(topic, message)
    status = result.rc
    if status == 0:
        print(f"Published: {message}")
    else:
        print(f"Failed to send message to topic {topic}")
    time.sleep(1)  # Delay between messages

# LED TEST
time.sleep(1)
client.publish(topic, "TURN_ON")
time.sleep(1)
client.publish(topic, "TURN_OFF")
time.sleep(1)
client.publish(topic, "TURN_ON")
time.sleep(1)
client.publish(topic, "TURN_OFF")
time.sleep(1)
client.publish(topic, "TURN_ON")
time.sleep(1)
client.publish(topic, "TURN_OFF")
time.sleep(1)
client.publish(topic, "TURN_ON")
time.sleep(1)
client.publish(topic, "TURN_OFF")

# Disconnect from the broker
client.disconnect()
