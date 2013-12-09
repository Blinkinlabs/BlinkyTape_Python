import serial

# This code assumes stock serialLoop() in the firmware

class BlinkyTape(object):
  def __init__(self, port, ledCount = 60, debug = False, buffered = True):
    self.port = port
    self.ledCount = ledCount
    self.position = 0 # Safety: do not write more than ledCount pixels
    # If True (default), queue up commands until show
    # If False, send every command (3 bytes) immediately and flush
    self.buffered = buffered
    self.buf = ""
    # Debug
    self.debug = debug
    self.count = 0 # Debug: number of shows
    # Connect to BlinkyTape
    self.serial = serial.Serial(port, 115200)

  def sendPixel(self,r,g,b):
    data = ""
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    data = chr(r) + chr(g) + chr(b)
    if self.position < self.ledCount:
      if self.buffered:
        self.buf += data
      else:
        self.serial.write(data)
        self.serial.flush()
      self.position += 1
    else:
      raise RuntimeError("Attempting to set pixel outside range! Issue 'show' to reset.")
      
  def show(self):
    control = chr(0)+chr(0)+chr(255)
    if self.buffered:
      self.serial.write(self.buf + control)
      self.buf=""
    else:
      self.serial.write(control)
    self.serial.flush()
    
    self.position=0
    
    if (self.debug):
      self.count = self.count + 1
      print self.count

  def displayColor(self, r, g, b):
    for i in range(0, self.ledCount):
      self.sendPixel(r,g,b)
    self.show()

  def resetToBootloader(self):
    """ Reset the blinkytape (note: this disconnects it!) """
    self.serial.setBaudrate(1200)
#    self.serial.close()
#    self.serial = serial.Serial(self.port, 1200)
#    self.serial.close()

  def reopen(self):
    self.serial.close()
    self.serial = serial.Serial(self.port, 115200)

  def close(self):
    self.serial.close()
    
    

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

