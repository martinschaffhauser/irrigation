from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import time

# Load environment variables from .env file
load_dotenv("../cred.env")

# Get the username and password from environment variables
mqtt_username = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Define the MQTT broker details
broker = "localhost"
port = 1883
topic = "irrigation/thuja"
client_id = "mqtt_publisher"
username = mqtt_username
password = mqtt_password

# Create a new MQTT client instance with the correct API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set the username and password for the MQTT client
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker, port)

# LOGIC
# irrigation_on
client.publish(topic, "thuja_irrigation_ON")
# irrigation_off
# client.publish(topic, "thuja_irrigation_OFF")

# Disconnect from the broker
client.disconnect()
