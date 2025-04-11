#!/bin/bash

echo "Updating system and installing git..."
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install -y git nano net-tools

# Clone and run the setup script from GitHub
rm ./slimmemeter -Rf
git clone https://github.com/claessensf/slimmemeter.git ./slimmemeter
cd slimmemeter
chmod +x setup.sh
./setup.sh
