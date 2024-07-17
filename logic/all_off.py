import time
import math
from mqtt_setup import get_mqtt_client

# Define the topics
topic_esp_thuja = "irrigation/thuja"
topic_esp_pump = "irrigation/pump"


def thuja_irrigation() -> None:
    """all off

    Args:
    """
    client = get_mqtt_client()
    client.publish(topic_esp_thuja, "thuja_irrigation_OFF")
    client.publish(topic_esp_pump, "pump_OFF")
    client.disconnect()


if __name__ == "__main__":
    thuja_irrigation()
