import subprocess
import os
import json


def run_scheduled_script(script_path, mqtt_args):
    if isinstance(mqtt_args, str):
        mqtt_args = json.loads(
            mqtt_args
        )  # Convert JSON string to dictionary if necessary

    total_time = mqtt_args["total_time"]
    cycle_duration = mqtt_args["cycle_duration"]
    pause_duration = mqtt_args["pause_duration"]

    venv_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "../../..",
        "venv",
        "bin",
        "activate",
    )
    command = f"source {venv_path} && python3 {script_path} --total_time {total_time} --cycle_duration {cycle_duration} --pause_duration {pause_duration}"
    subprocess.run(command, shell=True, executable="/bin/bash")


def run_script(script_path, mqtt_args):
    if isinstance(mqtt_args, str):
        mqtt_args = json.loads(
            mqtt_args
        )  # Convert JSON string to dictionary if necessary

    total_time = mqtt_args["total_time"]
    total_time = total_time * 1
    #     total_time * 60
    # )  # the time selected on html and js is ment to be in minutes

    venv_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "../../..",
        "venv",
        "bin",
        "activate",
    )
    command = f"source {venv_path} && python3 {script_path} --total_time {total_time}"
    subprocess.run(command, shell=True, executable="/bin/bash")
