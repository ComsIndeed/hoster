import firebase_admin
from firebase_admin import credentials, db
import time
import platform
import socket
import uuid

import subprocess

def get_connection_info():
    """Gets connection type and strength information."""
    try:
        output = subprocess.check_output(["iwconfig"], stderr=subprocess.DEVNULL, text=True)
    except subprocess.CalledProcessError:
        return None  # No wireless interface found

    lines = output.splitlines()
    connection_type = None
    ssid = None
    strength_percent = None
    signal_level_dBm = None

    for line in lines:
        if "ESSID:" in line:
            connection_type = "Wi-Fi"
            ssid = line.split(":")[1].strip().strip('"')
        elif "Link Quality=" in line:
            link_quality = line.split("=")[1].split("/")[0]
            strength_percent = int(link_quality) * 100 // 70  
        elif "Signal level=" in line:
            parts = line.split("=")
            if len(parts) > 1:  # Check if there's a value after the "="
                signal_level_dBm = parts[1].split(" ")[0]

    if connection_type:  # Only return results if a connection is found
        return {
            "type": connection_type,
            "ssid": ssid,
            "strength_percent": strength_percent,
            "signal_level_dBm": signal_level_dBm
        }
    else:
        return None

# ====================================================================================

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate("/home/coms/AAA_WORKSPACE/hoster/private_keys/project-academic-weapon-firebase-adminsdk-irvv8-de78853ef1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-academic-weapon-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Get a reference to the database
ref = db.reference()

connection_id = str(uuid.uuid4())

status = {
    "services": []
}

def newHeartbeat():
    connection_info = get_connection_info()

    payload = {
        "device": platform.system() + " " + platform.release(),
        "hostname": socket.gethostname(),
        "heartbeat": time.time(),
        "services": status["services"],
        "connection": {
            "type": connection_info["type"],
            "connectivity": connection_info["strength_percent"],
            "ssid": connection_info["ssid"]
            }
    }
    
    ref.child('devices').child(connection_id).set(payload)


while len(status["services"]) == 0:
    newHeartbeat()
    time.sleep(5)

while len(status["services"]) > 0:
    newHeartbeat()
    time.sleep(1)

