import smbus2
import sys
from time import sleep

class AMQ1602XA(object):
  def __init__(self, contrast=35):
    self.address = 0x3e
    self.register_setting = 0x00
    self.register_display = 0x40
    self.position = 0
    self.line = 0
    self.chars_per_line = 16
    self.display_lines = 2
    self.display_chars = self.chars_per_line * self.display_lines
    self.bus = smbus2.SMBus(1)

    sleep(0.5)
    self._initialize_display(contrast)

  def _initialize_display(self, contrast):
    trials = 5
    for i in range(trials):
      try:
        sleep(0.1)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x38])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x39])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x14])
        sleep(0.01)
        
        c_lower = (contrast & 0xf)
        c_upper = (contrast & 0x30) >> 4
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x70|c_lower])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x54|c_upper])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x6c])
        sleep(0.3)
        
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x38])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x01])
        sleep(0.01)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x0c])
        sleep(0.01)
        
        break
      except IOError as e:
        if i == trials - 1:
          raise IOError(f"Failed to initialize LCD after {trials} attempts: {e}")
        sleep(0.1)

  def clear(self):
    self.position = 0
    self.line = 0
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x01])
    sleep(0.01)

  def power_off(self):
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x08])
    sleep(0.01)

  def power_on(self):
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x0c])
    sleep(0.01)

  def newline(self):
    if self.line == self.display_lines - 1:
      self.clear()
    else:
      self.line += 1
      self.position = self.chars_per_line * self.line
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0xc0])
    sleep(0.01)

  def write_string(self, s):
    for c in list(s):
      self.write_char(ord(c))

  def write_char(self, c):
    byte_data = self.check_writable(c)
    if self.position == self.display_chars:
      self.clear()
    elif self.position == self.chars_per_line * (self.line + 1):
      self.newline()
    self.bus.write_i2c_block_data(
      self.address,
      self.register_display,
      [byte_data])
    sleep(0.001)
    self.position += 1

  def check_writable(self, c):
    if c >= 0x08 and c <= 0xff:
      return c
    else:
      return 0x20  # space

if __name__ == '__main__':
  amq = AMQ1602XA()
  if len(sys.argv) == 1:
    amq.write_string('Hello')
    amq.newline()
    amq.write_string('World')
  elif sys.argv[1] == 'clear':
    amq.clear()
  elif sys.argv[1] == 'on':
    amq.power_on()
  elif sys.argv[1] == 'off':
    amq.power_off()
  else:
    amq.write_string(sys.argv[1])
