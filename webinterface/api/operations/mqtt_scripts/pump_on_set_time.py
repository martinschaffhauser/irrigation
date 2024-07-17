import time
import argparse
from mqtt_setup import get_mqtt_client

# Define the topic
topic_esp_pump = "irrigation/pump"


def pump_on_set_time(total_time: int) -> None:
    client = get_mqtt_client()
    client.publish(topic_esp_pump, "pump_ON")
    time.sleep(total_time)
    client.publish(topic_esp_pump, "pump_OFF")
    client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn Pump on for set time Script")
    parser.add_argument(
        "--total_time", type=int, required=True, help="Total time in minutes"
    )

    args = parser.parse_args()
    pump_on_set_time(args.total_time)
