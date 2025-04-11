import paho.mqtt.client as mqtt
import json
import re
from datetime import datetime

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

USERNAME = config["username"]
MQTT_BROKER = config["mqtt_broker"]
MQTT_PORT = config["mqtt_port"]

# MQTT Topics
MQTT_TOPICS = {
    "electricity": f"{USERNAME}/smartmeter/electricity",
    "voltage_current": f"{USERNAME}/smartmeter/voltage_current",
    "gas": f"{USERNAME}/smartmeter/gas",
}

# Parse Fluvius data
def parse_fluvius_data(raw_data):
    lines = raw_data.split("\n")
    data = {
        "electricity": {},
        "voltage_current": {},
        "gas": {}
    }

    for line in lines:
        match = re.match(r"1-0:1\.8\.1\(([\d.]+)\*kWh\)", line)
        if match:
            data["electricity"]["consumption_tariff1"] = float(match.group(1))

        match = re.match(r"1-0:1\.8\.2\(([\d.]+)\*kWh\)", line)
        if match:
            data["electricity"]["consumption_tariff2"] = float(match.group(1))

        match = re.match(r"1-0:2\.8\.1\(([\d.]+)\*kWh\)", line)
        if match:
            data["electricity"]["delivery_tariff1"] = float(match.group(1))

        match = re.match(r"1-0:2\.8\.2\(([\d.]+)\*kWh\)", line)
        if match:
            data["electricity"]["delivery_tariff2"] = float(match.group(1))

        match = re.match(r"1-0:1\.7\.0\(([\d.]+)\*kW\)", line)
        if match:
            data["electricity"]["current_consumption"] = float(match.group(1))

        match = re.match(r"1-0:2\.7\.0\(([\d.]+)\*kW\)", line)
        if match:
            data["electricity"]["current_delivery"] = float(match.group(1))

        match = re.match(r"1-0:32\.7\.0\(([\d.]+)\*V\)", line)
        if match:
            data["voltage_current"]["voltage_phase1"] = float(match.group(1))

        match = re.match(r"1-0:52\.7\.0\(([\d.]+)\*V\)", line)
        if match:
            data["voltage_current"]["voltage_phase2"] = float(match.group(1))

        match = re.match(r"1-0:72\.7\.0\(([\d.]+)\*V\)", line)
        if match:
            data["voltage_current"]["voltage_phase3"] = float(match.group(1))

        match = re.match(r"1-0:24\.2\.3\(.+?\)\(([\d.]+)\*m3\)", line)
        if match:
            data["gas"]["gas_meter"] = float(match.group(1))

        match = re.match(r"1-0:1\.6\.0\((.+?)\)\(([\d.]+)\*kW\)", line)
        if match:
            timestamp = match.group(1)
            data["electricity"]["peak_capacity"] = {
                "value": float(match.group(2)),
                "timestamp": timestamp
            }
    
    # Add a common timestamp
    data["electricity"]["timestamp"] = datetime.now().isoformat()
    data["voltage_current"]["timestamp"] = datetime.now().isoformat()
    data["gas"]["timestamp"] = datetime.now().isoformat()

    return data

# Publish data to MQTT
def publish_to_mqtt(data):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)

    for category, topic in MQTT_TOPICS.items():
        if category in data:
            payload = json.dumps(data[category])
            client.publish(topic, payload)

    client.disconnect()

# Example raw data from Fluvius meter
raw_data = """
0-0:96.1.4(50217)
0-0:96.1.1(3153414733313030313537383232)
0-0:1.0.0(250411211226S)
1-0:1.8.1(001938.304*kWh)
1-0:1.8.2(003429.673*kWh)
1-0:2.8.1(006776.513*kWh)
1-0:2.8.2(002805.521*kWh)
1-0:96.14.0(0002)
1-0:1.4.0(00.012*kW)
1-0:1.6.0(250402071500S)(00.930*kW)
1-0:1.7.0(00.043*kW)
1-0:2.7.0(00.000*kW)
1-0:32.7.0(233.0*V)
1-0:52.7.0(230.3*V)
1-0:72.7.0(232.9*V)
0-1:24.2.3(250411210957S)(04188.420*m3)
"""

# Parse and publish the data
parsed_data = parse_fluvius_data(raw_data)
publish_to_mqtt(parsed_data)
