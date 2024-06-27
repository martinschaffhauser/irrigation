import paho.mqtt.client as mqtt

# Define the MQTT broker details
broker = "localhost"
port = 1883
topic = "test/topic"
client_id = "mqtt_subscriber"
username = "martin"
password = "sofi"


# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")


# Create a new MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

# Set the username and password for the MQTT client
client.username_pw_set(username, password)

# Assign the on_message callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port)

# Subscribe to the topic
client.subscribe(topic)

# Start the MQTT client loop to process messages
client.loop_forever()
