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
topic_esp_thuja = "irrigation/thuja"
topic_esp_pump = "irrigation/pump"
client_id = "mqtt_publisher_python_irrigation_script"
username = mqtt_username
password = mqtt_password

# Create a new MQTT client instance with the correct API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set the username and password for the MQTT client
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker, port)


# LOGIC
def thuja_irrigation(switch: str, cycles: int) -> None:
    if switch == "ON":
        client.publish(topic_esp_thuja, "thuja_irrigation_ON")
        pump_cycles = cycles  # 30 * (60sec_on + 5sec_off) = 32,5 min
        for _ in range(pump_cycles):
            client.publish(topic_esp_pump, "pump_ON")
            time.sleep(60)
            client.publish(topic_esp_pump, "pump_OFF")
            time.sleep(5)

        # eventually turn off everything
        client.publish(topic_esp_thuja, "thuja_irrigation_OFF")
        client.publish(topic_esp_pump, "pump_OFF")


thuja_irrigation("ON", 30)

# Disconnect from the broker
client.disconnect()
