#!/bin/bash

echo "Updating system and installing git..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git nano net-tools

# Clone and run the setup script from GitHub
git clone https://github.com/claessensf/slimmemeter.git ./smart-meter-reader
cd smart-meter-reader
chmod +x setup.sh
./setup.sh
