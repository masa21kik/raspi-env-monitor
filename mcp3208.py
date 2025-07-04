import RPi.GPIO as GPIO
from time import sleep

# AD Converter
class MCP3208(object):
  def __init__(self, clockpin=11, mosipin=10, misopin=9, cspin=8):
    self.clock = clockpin
    self.mosi = mosipin
    self.miso = misopin
    self.cs = cspin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.clock, GPIO.OUT)
    GPIO.setup(self.mosi, GPIO.OUT)
    GPIO.setup(self.miso, GPIO.IN)
    GPIO.setup(self.cs, GPIO.OUT)

  def __del__(self):
    GPIO.cleanup(self.clock)
    GPIO.cleanup(self.mosi)
    GPIO.cleanup(self.miso)
    GPIO.cleanup(self.cs)

  def read(self, ch):
    if ch > 8 or ch < 0:
      return -1
    GPIO.output(self.cs, GPIO.HIGH)
    GPIO.output(self.clock, GPIO.LOW)
    GPIO.output(self.cs, GPIO.LOW)

    commandout = ch
    commandout |= 0x18
    commandout <<= 3

    for i in range(5):
      if commandout & 0x80:
        GPIO.output(self.mosi, GPIO.HIGH)
      else:
        GPIO.output(self.mosi, GPIO.LOW)
      commandout <<= 1
      GPIO.output(self.clock, GPIO.HIGH)
      GPIO.output(self.clock, GPIO.LOW)

    adcout = 0

    for i in range(13):
      GPIO.output(self.clock, GPIO.HIGH)
      GPIO.output(self.clock, GPIO.LOW)
      adcout <<= 1
      if i > 0 and GPIO.input(self.miso) == GPIO.HIGH:
        adcout |= 0x1
    GPIO.output(self.cs, GPIO.HIGH)
    return adcout


if __name__ == '__main__':
  SPICLK = 11
  SPIMOSI = 10
  SPIMISO = 9
  SPICS = 8
  CH = 0
  mcp = MCP3208(SPICLK, SPIMOSI, SPIMISO, SPICS)

  try:
    while True:
      print(mcp.read(CH))
      sleep(0.2)
  except KeyboardInterrupt:
    pass
