
# Ping Tracker - V1.0 - 08/01/2025

## Purpose
Ping Tracker is a lightweight tool for monitoring the status of network devices. It continuously pings a list of devices at specified intervals and provides a web-based interface to display their statuses, including:
- Whether the device is reachable or not.
- The ping time (in milliseconds) if reachable.
- The last time the device was reachable, if currently unreachable.

This tool is containerized for easy deployment using Docker, it uses Python, Flask, and ping.

It does nothing that fully fledged network monitors can do (and can do much better). For diagnosing a network mesh problem I needed to be able to run a very lightweight tool on multiple low-power devices like routers and Raspberry PI Ws, and installing a full network monitor or agent on each device would have been excessive.

---

## Features
- **Web Interface:** Displays real-time status updates for all configured devices.
- **Configurable:** Adjust the listening IP, port, ping interval, and device list via a `config.yaml` file.
- **Dockerized:** Simple setup and deployment with Docker.

---

## Configuration

### `config.yaml`
The application uses a `config.yaml` file for configuration. Below is an example configuration:

```yaml
listen_ip: "0.0.0.0"          # IP address the web server listens on
listen_port: 12345             # Port the web server listens on
ping_interval: 15              # Interval in seconds between ping cycles
devices:                       # List of devices to monitor
  - name: "Device 1"
    ip: "192.168.1.1"
  - name: "Device 2"
    ip: "192.168.1.2"
```

### Parameters
- `listen_ip`: The IP address the web server will listen on (default: `0.0.0.0` - ie all local interfaces/IPs).
- `listen_port`: The port the web server will listen on (default: `12345`).
- `ping_interval`: Time interval (in seconds) between consecutive pings (default: `10`).
- `devices`: A list of devices, each with a `name` and `ip`.

---

## How to Build and Run

### Prerequisites
- **Docker:** Ensure Docker is installed and running on your system.
- **Python (optional):** For local testing without Docker.

### Directory Structure
The project directory should have the following structure:

```
ping-tracker/
├── app.py               # The main Python application
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # HTML template for the web front-end
├── Dockerfile           # Dockerfile to containerize the app
```

### Steps to Build and Run Using Docker

1. **Navigate to the project directory**:
   ```bash
   cd ping-tracker
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t ping-tracker .
   ```

3. **Run the Docker container**:
   ```bash
   docker run -d -p 12345:12345 --name pingtracker ping-tracker
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:12345`.

### Running Locally (Without Docker)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   Open your browser and go to `http://localhost:12345`.

---

## Usage

- Open the web interface at the specified `listen_ip` and `listen_port`.
- Monitor the status of devices:
  - **Reachable:** Displays the ping time.
  - **Unreachable:** Shows the last time the device was reachable.
  - **Error:** Indicates a problem with pinging the device.

---

## Customization

To modify:
1. **Add or remove devices**: Update the `devices` section in `config.yaml`.
2. **Change ping interval**: Update the `ping_interval` in `config.yaml`.
3. **Change listening IP or port**: Update the `listen_ip` and `listen_port` in `config.yaml`.

After changes, restart the Docker container or the Python application.

If you have a spreadsheet of device names (Column 1) and IP addresses (Column 2) and save it as devices.csv then this command will turn it into yaml suitable for addition to config.yaml

   ```bash
tr -d '\r' < devices.csv | awk 'BEGIN { FS="," } { if ($1 != "") print "  - name: \"" $1 "\"\n    ip: \"" $2 "\"\n"; else print "" }' >temp.yaml
   ```

---

## License
This project is open-source and available under the MIT License.


