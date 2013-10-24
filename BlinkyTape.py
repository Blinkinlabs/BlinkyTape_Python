import serial
import time

class BlinkyTape(object):
  def __init__(self, port):
    self.serial = serial.Serial(port, 115200)
    self.show() # Flush

  def sendPixel(self,r,g,b):
    data = ""
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    data = chr(r) + chr(g) + chr(b)
    self.serial.write(data)
    self.serial.flush()

  def show(self):
    self.serial.write(chr(255))
    self.serial.flush()


if __name__ == "__main__":

  import glob
  import optparse 

  LED_COUNT = 60

  parser = optparse.OptionParser()
  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default=None)
  (options, args) = parser.parse_args()

  if options.portname != None:
    port = options.portname
  else:
    serialPorts = glob.glob("/dev/cu.usbmodem*")
    port = serialPorts[0]

  bb = BlinkyTape(port)

  while True:

    for x in range(0, LED_COUNT):
      bb.sendPixel(255,255,255)
    bb.show();

    for x in range(0, LED_COUNT):
      bb.sendPixel(0,0,0)
    bb.show()

