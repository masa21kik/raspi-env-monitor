import serial
import subprocess
import json

class MH_Z19(object):
  def __init__(self, serial_port='serial0'):
    self.serial_port = serial_port
    self.serial_device = '/dev/%s' % serial_port

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
    self.stop_getty()
    res = self.readSensor()
    self.start_getty()
    return res

  def readSensor(self):
    ser = self.connect_serial()
    while 1:
      ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s = ser.read(9)
      if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86:
          return {
            'co2': s[2]*256 + s[3],
            'temperature': s[4] - 40,
            'TT': s[4],
            'SS': s[5],
            'UhUl': s[6]*256 + s[7]
          }
      break

if __name__ == '__main__':
  d = MH_Z19().readData()
  print(json.dumps(d))
