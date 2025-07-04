# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Raspberry Pi environmental monitoring system that collects sensor data and uploads it to Google Sheets. The system reads temperature, humidity, pressure, CO2 levels, and light levels from various sensors and displays data on an LCD screen.

## Architecture

The system consists of sensor driver modules and a main uploader script:

- **Sensor Drivers**: Each sensor has its own Python module with device-specific I2C/SPI communication
- **Data Collection**: `uploader.py` orchestrates reading from all sensors and uploading to Google Sheets
- **Display**: Real-time sensor data is shown on an LCD display
- **Data Storage**: All readings are timestamped and stored in Google Sheets for historical analysis

## Key Components

- `uploader.py`: Main script that coordinates sensor reading, data upload, and display
- `bme280.py`: BME280 sensor driver for temperature, humidity, and pressure
- `mh_z19.py`: MH-Z19 CO2 sensor driver with serial communication
- `mcp3208.py`: MCP3208 ADC driver for analog sensors (light sensor)
- `amq1602xa.py`: AMQ1602XA LCD display driver
- `spreadsheet.py`: Google Sheets API wrapper for data upload

## Hardware Dependencies

This code is designed to run on Raspberry Pi with:
- I2C enabled for BME280 and LCD communication
- SPI enabled for MCP3208 ADC
- Serial port configured for MH-Z19 CO2 sensor
- GPIO pins configured for sensor connections

## Usage

### Running the Monitor
```bash
python3 uploader.py <google_keyfile.json> <spreadsheet_id>
```

### Testing Individual Sensors
```bash
python3 bme280.py          # Test BME280 sensor
python3 mh_z19.py          # Test CO2 sensor
python3 mcp3208.py         # Test ADC/light sensor
python3 amq1602xa.py       # Test LCD display
```

### Installing Dependencies
```bash
pip3 install -r requirements.txt
```

## Google Sheets Integration

The system requires:
- Google Service Account credentials JSON file
- Google Sheets API enabled
- Spreadsheet with a "Data" worksheet for storing sensor readings

Data format: timestamp, temperature, humidity, pressure, CO2, light_level

## Hardware Configuration

- BME280: I2C address 0x76
- LCD: I2C address 0x3e
- MCP3208: SPI pins (CLK=11, MOSI=10, MISO=9, CS=8)
- MH-Z19: Serial port /dev/serial0

## Common Issues

- MH-Z19 sensor requires stopping/starting Getty service for serial access
- I2C/SPI must be enabled in raspi-config
- GPIO cleanup is handled automatically in sensor destructors
- Serial permissions may require running with sudo