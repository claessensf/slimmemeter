import serial
import json
import paho.mqtt.client as mqtt

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

broker_ip = config["broker_ip"]
broker_port = config["broker_port"]
mqtt_topic = config["mqtt_topic"]

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.connect(broker_ip, broker_port)

# Serial setup
SERIAL_PORT = "/dev/ttyUSB0"  # Adjust based on your smart meter
BAUD_RATE = 115200

def read_smart_meter():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            try:
                line = ser.readline().decode("utf-8").strip()
                print(line)  # Debugging
                mqtt_client.publish(mqtt_topic, line)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    read_smart_meter()
