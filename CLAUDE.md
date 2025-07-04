# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

Environmental monitoring system with modular sensor drivers and centralized data collection:

- **Sensor Drivers**: Each sensor has its own Python module with device-specific I2C/SPI communication
- **Data Collection**: `env_monitor.py` orchestrates reading from all sensors and uploading to Google Sheets
- **Display**: Real-time sensor data is shown on an LCD display
- **Data Storage**: All readings are timestamped and stored in Google Sheets for historical analysis

## Key Components

- `env_monitor.py`: Main script that coordinates sensor reading, data upload, and display
- `bme280.py`: BME280 sensor driver for temperature, humidity, and pressure
- `mh_z19.py`: MH-Z19 CO2 sensor driver with serial communication
- `mcp3208.py`: MCP3208 ADC driver for analog sensors (light sensor)
- `amq1602xa.py`: AMQ1602XA LCD display driver
- `spreadsheet.py`: Google Sheets API wrapper for data upload

## Development Commands

### Running the Monitor
```bash
python3 env_monitor.py <google_keyfile.json> <spreadsheet_id>
```

### Testing Individual Sensors
```bash
python3 bme280.py          # Test BME280 sensor
python3 mh_z19.py          # Test CO2 sensor
python3 mcp3208.py         # Test ADC/light sensor
python3 amq1602xa.py       # Test LCD display
```

## Hardware Configuration

- BME280: I2C address 0x76
- LCD: I2C address 0x3e
- MCP3208: SPI pins (CLK=11, MOSI=10, MISO=9, CS=8)
- MH-Z19: Serial port /dev/ttyAMA0

## UART Configuration for MH-Z19

To use MH-Z19 without sudo privileges, configure GPIO UART:

### Required System Configuration

1. **Edit /boot/config.txt:**
   ```
   enable_uart=1
   dtoverlay=disable-bt
   ```

2. **Edit /boot/cmdline.txt:**
   Remove `console=serial0,115200` (keep `console=tty1`)

3. **Disable services:**
   ```bash
   sudo systemctl stop serial-getty@serial0.service
   sudo systemctl disable serial-getty@serial0.service
   sudo systemctl mask serial-getty@serial0.service
   sudo systemctl disable serial-getty@ttyAMA0.service
   sudo systemctl disable hciuart.service
   ```

4. **Create udev rule for proper permissions:**
   ```bash
   sudo nano /etc/udev/rules.d/10-serial.rules
   ```
   Add the following line:
   ```
   SUBSYSTEM=="tty", KERNEL=="ttyAMA0", GROUP="dialout", MODE="0664"
   ```

5. **Add user to dialout group:**
   ```bash
   sudo usermod -a -G dialout $USER
   ```

6. **Apply udev rules:**
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

7. **Reboot system** for all changes to take effect

### Note
This configuration disables Bluetooth and serial console login to dedicate /dev/ttyAMA0 to MH-Z19 sensor.

## Coding Rules

- **No spaces in blank lines**: Empty lines must contain no spaces or tabs
- Follow existing code style and indentation patterns
- Use meaningful variable names and comments where necessary
- Handle errors gracefully with proper exception handling

## Common Issues

- MH-Z19 sensor requires stopping/starting Getty service for serial access
- I2C/SPI must be enabled in raspi-config
- GPIO cleanup is handled automatically in sensor destructors
- Serial permissions may require running with sudo