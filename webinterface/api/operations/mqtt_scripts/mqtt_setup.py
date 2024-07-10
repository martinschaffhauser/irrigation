# mqtt_setup.py
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt

# Load environment variables from .env file
load_dotenv("../cred.env")

# Get the username and password from environment variables
mqtt_username = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Define the MQTT broker details
broker = "localhost"
port = 1883


def get_mqtt_client():
    # Create a new MQTT client instance with the correct API version
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)

    # Connect to the MQTT broker
    client.connect(broker, port)

    return client
