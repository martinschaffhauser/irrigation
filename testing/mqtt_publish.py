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
# topic = "test/topic"
topic = "test/topic2"
# topic = "irrigation/thuja"
# client_id = "mqtt_publisher"
username = mqtt_username
password = mqtt_password

# Create a new MQTT client instance with the correct API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set the username and password for the MQTT client
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.connect(broker, port)

# Publish messages to the topic
for i in range(2):
    message = f"Message {i+1}: now the logic that depends on this messag needs to start"
    result = client.publish(topic, message)
    status = result.rc
    if status == 0:
        print(f"Published: {message}")
    else:
        print(f"Failed to send message to topic {topic}")
    time.sleep(1)  # Delay between messages

# LED TEST
if topic == "irrigation/thuja":
    sleep_time = 0.2
    message = "thuja_irrigation"
elif topic == "test/topic":
    sleep_time = 2
    message = "TURN"
elif topic == "test/topic2":
    sleep_time = 0.5
    message = "TURN"

time.sleep(sleep_time)
client.publish(topic, f"{message}_ON")
print("turning on")
time.sleep(sleep_time)
client.publish(topic, f"{message}_OFF")
print("turning off")
time.sleep(sleep_time)
client.publish(topic, f"{message}_ON")
print("turning on")
time.sleep(sleep_time)
client.publish(topic, f"{message}_OFF")
print("turning off")
time.sleep(sleep_time)
client.publish(topic, f"{message}_ON")
print("turning on")
time.sleep(sleep_time)
client.publish(topic, f"{message}_OFF")
print("turning off")
time.sleep(sleep_time)
client.publish(topic, f"{message}_ON")
print("turning on")
time.sleep(sleep_time)
client.publish(topic, f"{message}_OFF")
print("turning off")

# Disconnect from the broker
client.disconnect()
