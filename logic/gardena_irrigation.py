import time
import math
from mqtt_setup import get_mqtt_client

# Define the topic
topic_esp_pump = "irrigation/pump"


def gardena_irrigation(
    total_time: int, cycle_duration: int, pause_duration: int
) -> None:
    """_summary_

    Args:
        total_time (int): unit = minutes; how long should the pump be turned on
        cycle_duration (int): unit = seconds; how long should on ON-cycle last
        pause_duration (int): unit = seconds; how long should the pump be turned OFF for it to reset, so that no "leak" is detected falsely
    """
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
    gardena_irrigation(60, 60, 10)
