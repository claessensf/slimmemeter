#!/bin/bash
# This script sets up the Raspberry Pi for the smart meter reader project

echo "Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git

echo "Installing Python libraries..."
pip3 install paho-mqtt pyserial

echo "Setting up MQTT configuration..."
# Replace these values with your MQTT broker details
BROKER_IP="192.168.1.100"
BROKER_PORT="1883"
MQTT_TOPIC="smart-meter/data"

cat <<EOF > config.json
{
  "broker_ip": "$BROKER_IP",
  "broker_port": $BROKER_PORT,
  "mqtt_topic": "$MQTT_TOPIC"
}
EOF

echo "Setting up smart meter reader service..."
sudo cp systemd/smart_meter_reader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable smart_meter_reader
sudo systemctl start smart_meter_reader

echo "Setup complete! Your smart meter should now be connected."
