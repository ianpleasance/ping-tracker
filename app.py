#
# Version 1.0.0 - 08/01/2025
#
from flask import Flask, jsonify, render_template
import subprocess
import threading
import time
from datetime import datetime
import yaml
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Global dictionary to store device information
devices = {}
device_statuses = {}
config = {
    "listen_ip": "0.0.0.0",
    "listen_port": 12345,
    "ping_interval": 10,
}

# Read configuration from config.yaml file
def load_config(file_path="config.yaml"):
    global config
    with open(file_path, "r") as f:
        user_config = yaml.safe_load(f)
        config["listen_ip"] = user_config.get("listen_ip", config["listen_ip"])
        config["listen_port"] = user_config.get("listen_port", config["listen_port"])
        config["ping_interval"] = user_config.get("ping_interval", config["ping_interval"])

# Read devices from config.yaml file
def load_devices(file_path="config.yaml"):
    with open(file_path, "r") as f:
        user_config = yaml.safe_load(f)
        for device in user_config.get("devices", []):
            name = device["name"]
            ip = device["ip"]
            devices[name] = ip
            device_statuses[name] = {
                "status": "Unknown", 
                "ping_time": None, 
                "last_pingable": None
            }

# Function to ping a single device
def ping_device(name, ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", ip],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            # Parse ping time
            ping_time = float(result.stdout.split("time=")[1].split(" ms")[0])
            device_statuses[name] = {
                "status": "Reachable", 
                "ping_time": ping_time, 
                "last_pingable": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            if device_statuses[name]["status"] == "Reachable":
                device_statuses[name]["last_pingable"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            device_statuses[name]["status"] = "Unreachable"
            device_statuses[name]["ping_time"] = None
    except Exception as e:
        if device_statuses[name]["status"] == "Reachable":
            device_statuses[name]["last_pingable"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        device_statuses[name] = {
            "status": "Error", 
            "ping_time": None, 
            "last_pingable": device_statuses[name].get("last_pingable")
        }

# Function to ping devices in parallel
def ping_devices():
    while True:
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(ping_device, name, ip) for name, ip in devices.items()]
            for future in futures:
                future.result()
        time.sleep(config["ping_interval"])

# Route to serve the device status JSON
@app.route("/status")
def status():
    return jsonify(device_statuses)

# Route to serve the web interface
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Load configuration and devices
    load_config()
    load_devices()
    # Start pinging in a separate thread
    threading.Thread(target=ping_devices, daemon=True).start()
    app.run(host=config["listen_ip"], port=config["listen_port"])

