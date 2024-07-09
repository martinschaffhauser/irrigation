import subprocess
import os


script_path = os.path.join(os.getcwd(), "mqtt_scripts", "mqtt_test.py")


def run_script(script_path):
    venv_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "../../..",
        "venv",
        "bin",
        "activate",
    )
    command = f"source {venv_path} && python3 {script_path}"
    subprocess.run(command, shell=True, executable="/bin/bash")
