import serial
import subprocess
import json
import time
import logging

class MH_Z19(object):
  def __init__(self, serial_port='serial0', max_retries=3, retry_delay=1.0):
    self.serial_port = serial_port
    self.serial_device = '/dev/%s' % serial_port
    self.max_retries = max_retries
    self.retry_delay = retry_delay
    self.logger = logging.getLogger(__name__)

  def stop_getty(self):
    cmd = 'sudo systemctl stop serial-getty@%s.service' % self.serial_port
    subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

  def start_getty(self):
    cmd = 'sudo systemctl start serial-getty@%s.service' % self.serial_port
    subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)

  def connect_serial(self):
    return serial.Serial(self.serial_device,
                          baudrate=9600,
                          bytesize=serial.EIGHTBITS,
                          parity=serial.PARITY_NONE,
                          stopbits=serial.STOPBITS_ONE,
                          timeout=1.0)

  def readData(self):
    for attempt in range(self.max_retries):
      try:
        self.stop_getty()
        res = self.readSensor()
        self.start_getty()
        if res and 'co2' in res:
          return res
        else:
          self.logger.warning(f"Attempt {attempt + 1}: Invalid data received")
      except Exception as e:
        self.logger.error(f"Attempt {attempt + 1}: Error reading sensor: {e}")
        self.start_getty()

      if attempt < self.max_retries - 1:
        time.sleep(self.retry_delay)

    self.logger.error("Failed to read sensor after all retries")
    return None

  def readSensor(self):
    ser = None
    try:
      ser = self.connect_serial()
      time.sleep(0.1)

      for attempt in range(3):
        ser.reset_input_buffer()
        ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
        time.sleep(0.1)
        s = ser.read(9)

        if len(s) == 9 and s[0] == 0xff and s[1] == 0x86:
          checksum = 0xff - (sum(s[1:8]) & 0xff) + 1
          if s[8] == (checksum & 0xff):
            return {
              'co2': s[2]*256 + s[3],
              'temperature': s[4] - 40,
              'TT': s[4],
              'SS': s[5],
              'UhUl': s[6]*256 + s[7]
            }
          else:
            self.logger.warning(f"Checksum mismatch on attempt {attempt + 1}")
        else:
          self.logger.warning(f"Invalid response length or header on attempt {attempt + 1}: {len(s)} bytes")

        if attempt < 2:
          time.sleep(0.5)

      return None
    finally:
      if ser:
        ser.close()

if __name__ == '__main__':
  d = MH_Z19().readData()
  print(json.dumps(d))
