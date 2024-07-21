import logging
import telnetlib
import time
import threading
import os
from dotenv import load_dotenv

### LOAD ENV FILE ###
load_dotenv("../cred.env")

# Telnet server details
TELNET_PUMP_ESP = os.getenv("TELNET_PUMP_ESP_IP")
TELNET_THUJA_ESP = os.getenv("TELNET_THUJA_ESP_IP")
TELNET_PORT = 23

latest_output_pump_esp = {"timestamp": "", "output": ""}
latest_output_thuja_esp = {"timestamp": "", "output": ""}


def read_telnet_output(host, port, output_storage):
    try:
        # Connect to the telnet server
        tn = telnetlib.Telnet(host, port)

        while True:
            # Read the output
            output = tn.read_until(b"\n").decode("utf-8").strip()
            logging.info(
                f"Telnet output from {host}: {output}"
            )  # For debugging purposes

            # Update the latest output
            output_storage["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            output_storage["output"] = output

            # Sleep for a short interval before reading again
            time.sleep(1)
    except Exception as e:
        logging.info(f"Error from {host}: {e}")
        time.sleep(5)  # Retry after a delay in case of failure


# Start the telnet reading in separate threads
telnet_thread_pump_esp = threading.Thread(
    target=read_telnet_output,
    args=(TELNET_PUMP_ESP, TELNET_PORT, latest_output_pump_esp),
    daemon=True,
)
telnet_thread_thuja_esp = threading.Thread(
    target=read_telnet_output,
    args=(TELNET_THUJA_ESP, TELNET_PORT, latest_output_thuja_esp),
    daemon=True,
)
telnet_thread_pump_esp.start()
telnet_thread_thuja_esp.start()
