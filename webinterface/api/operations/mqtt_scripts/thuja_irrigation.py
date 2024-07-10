import time
import math
import argparse
from mqtt_setup import get_mqtt_client

# Define the topics
topic_esp_thuja = "irrigation/thuja"
topic_esp_pump = "irrigation/pump"


def thuja_irrigation(total_time: int, cycle_duration: int, pause_duration: int) -> None:
    """_summary_

    Args:
        total_time (int): unit = minutes; how long should the pump be turned on
        cycle_duration (int): unit = seconds; how long should on ON-cycle last
        pause_duration (int): unit = seconds; how long should the pump be turned OFF for it to reset, so that no "leak" is detected falsely
    """
    pump_cycles = total_time * 60 / (cycle_duration + pause_duration)
    pump_cycles = math.ceil(pump_cycles)
    client = get_mqtt_client()
    client.publish(topic_esp_thuja, "thuja_irrigation_ON")
    for _ in range(pump_cycles):
        client.publish(topic_esp_pump, "pump_ON")
        time.sleep(cycle_duration)
        client.publish(topic_esp_pump, "pump_OFF")
        time.sleep(pause_duration)

    # eventually turn off everything
    client.publish(topic_esp_thuja, "thuja_irrigation_OFF")
    client.publish(topic_esp_pump, "pump_OFF")
    client.disconnect()


# if __name__ == "__main__":
# thuja_irrigation(60, 60, 5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Thuja Irrigation Script")
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
    thuja_irrigation(args.total_time, args.cycle_duration, args.pause_duration)
