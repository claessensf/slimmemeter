# Slimmemeter - Smart Meter Reader Project

This project allows you to read data from a smart meter in Belgium and send the data to an MQTT broker for visualization in Grafana. The setup is designed to be as simple as possible, requiring minimal configuration.

---

## Features
- Automatically reads data from a DSMR-compliant smart meter.
- Publishes data to an MQTT broker.
- Can be visualized in Grafana.

---

## Quick Start

1. **Flash Raspberry Pi OS** to your SD card.
2. **Clone this repository** to your Raspberry Pi:
   ```bash
   git clone https://github.com/claessensf/slimmemeter.git
   cd slimmemeter
   ```
3. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
4. Configure your MQTT broker details in `config.json`.

---

## Documentation
- [Setup Guide](docs/setup-guide.md)
- [MQTT Configuration](docs/mqtt-config.md)
