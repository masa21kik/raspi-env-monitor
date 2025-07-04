import smbus
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
    self.bus = smbus.SMBus(1)

    trials = 5
    for i in range(trials):
      try:
        c_lower = (contrast & 0xf)
        c_upper = (contrast & 0x30) >> 4
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
        sleep(0.2)
        self.bus.write_i2c_block_data(
          self.address,
          self.register_setting,
          [0x38, 0x01, 0x0d])
        sleep(0.001)
        break
      except IOError:
        if i == trials - 1:
          sys.exit()

  def clear(self):
    self.position = 0
    self.line = 0
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x01])
    sleep(0.001)

  def power_off(self):
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x08])
    sleep(0.001)

  def power_on(self):
    self.bus.write_i2c_block_data(
      self.address,
      self.register_setting,
      [0x0c])
    sleep(0.001)

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
    sleep(0.001)

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
