import time
import math
import argparse
from mqtt_setup import get_mqtt_client

# Define the topic
topic_esp_pump = "irrigation/pump"


def gardena_irrigation(
    total_time: int, cycle_duration: int, pause_duration: int
) -> None:
    pump_cycles = total_time * 60 / (cycle_duration + pause_duration)
    pump_cycles = math.ceil(pump_cycles)
    client = get_mqtt_client()
    for _ in range(pump_cycles):
        client.publish(topic_esp_pump, "pump_ON")
        time.sleep(cycle_duration)
        client.publish(topic_esp_pump, "pump_OFF")
        time.sleep(pause_duration)

    # eventually turn off everything
    client.publish(topic_esp_pump, "pump_OFF")
    client.disconnect()
    return pump_cycles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gardena Irrigation Script")
    parser.add_argument(
        "--total_time", type=int, required=True, help="Total time in minutes"
    )
    parser.add_argument(
        "--cycle_duration", type=int, required=True, help="Cycle duration in seconds"
    )
    parser.add_argument(
        "--pause_duration", type=int, required=True, help="Pause duration in seconds"
    )

    args = parser.parse_args()
    gardena_irrigation(args.total_time, args.cycle_duration, args.pause_duration)
