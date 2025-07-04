# Raspberry Pi Environmental Monitoring System

A comprehensive environmental monitoring system that collects sensor data from multiple sensors and uploads it to Google Sheets for analysis and historical tracking.

## Features

- **Multi-sensor data collection**: Temperature, humidity, pressure, CO2 levels, and light intensity
- **Real-time display**: LCD screen shows current readings with timestamp
- **Cloud storage**: Automatic data upload to Google Sheets
- **Stable operation**: Robust error handling and retry mechanisms
- **No sudo required**: Secure operation without elevated privileges

## Sensors Supported

- **BME280**: Temperature, humidity, and atmospheric pressure
- **MH-Z19**: CO2 concentration measurement
- **MCP3208**: 8-channel ADC for analog sensors (light sensor)
- **AMQ1602XA**: 16x2 LCD display for real-time data

## Hardware Requirements

### Raspberry Pi Configuration
- Raspberry Pi with GPIO access
- I2C enabled for BME280 and LCD
- SPI enabled for MCP3208 ADC
- UART configured for MH-Z19 CO2 sensor

### Wiring
- **BME280**: I2C address 0x76
- **LCD**: I2C address 0x3e  
- **MCP3208**: SPI pins (CLK=11, MOSI=10, MISO=9, CS=8)
- **MH-Z19**: Serial port /dev/ttyAMA0

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/masa21kik/raspi-env-monitor.git
cd raspi-env-monitor
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. System Configuration

**Enable I2C and SPI:**
```bash
sudo raspi-config
# Interface Options → I2C → Enable
# Interface Options → SPI → Enable
```

**Configure UART for MH-Z19:**

Edit `/boot/config.txt`:
```
enable_uart=1
dtoverlay=disable-bt
```

Edit `/boot/cmdline.txt` (remove `console=serial0,115200`):
```
console=tty1 ...
```

Disable conflicting services:
```bash
sudo systemctl stop serial-getty@serial0.service
sudo systemctl disable serial-getty@serial0.service
sudo systemctl mask serial-getty@serial0.service
sudo systemctl disable hciuart.service
```

Set up permissions:
```bash
sudo usermod -a -G dialout $USER
echo 'SUBSYSTEM=="tty", KERNEL=="ttyAMA0", GROUP="dialout", MODE="0664"' | sudo tee /etc/udev/rules.d/10-serial.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Reboot the system:**
```bash
sudo reboot
```

## Google Sheets Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account and download JSON key file
4. Share your Google Sheet with the service account email
5. Create a worksheet named "Data" in your spreadsheet

## Usage

### Run the Environmental Monitor
```bash
python3 env_monitor.py <google_keyfile.json> <spreadsheet_id>
```

### Test Individual Sensors
```bash
python3 bme280.py          # Test BME280 sensor
python3 mh_z19.py          # Test CO2 sensor  
python3 mcp3208.py         # Test ADC/light sensor
python3 amq1602xa.py       # Test LCD display
```

## Data Format

Data is stored in Google Sheets with the following columns:
- Timestamp
- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- CO2 (ppm)
- Light Level (ADC value)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.