import serial
import time

class BlinkyTape(object):
  def __init__(self, port, ledCount = 60):
    self.ledCount = ledCount
    self.serial = serial.Serial(port, 115200)
    self.data = ""
    self.show() # Flush

  def sendPixel(self,r,g,b):
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    self.data += chr(r) + chr(g) + chr(b)

  def show(self):
    self.data += chr(255)
    self.serial.write(self.data)
    self.data = ""

  def displayColor(self, r, g, b):
    self.data = ""
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    for i in range(0, self.ledCount):
      self.data += chr(r) + chr(g) + chr(b)
    self.data += chr(255)
    self.serial.write(self.data)
    self.serial.flush()
    self.data = ""


if __name__ == "__main__":

  import glob
  import optparse 

  parser = optparse.OptionParser()
  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default=None)
  (options, args) = parser.parse_args()

  if options.portname != None:
    port = options.portname
  else:
    serialPorts = glob.glob("/dev/cu.usbmodem*")
    port = serialPorts[0]

  bt = BlinkyTape(port)

  while True:

    bt.displayColor(255,0,0)
    bt.displayColor(0,255,0)
    bt.displayColor(0,0,255)
    bt.displayColor(255,255,255)
    bt.displayColor(0,0,0)

