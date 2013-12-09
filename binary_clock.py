from BlinkyTape import BlinkyTape
import time
from datetime import datetime,timedelta
import optparse

MAX_BRIGHTNESS = 50 # In range(255)
     
def display(port):
  bb = BlinkyTape(port)
  dt = datetime.now()
  send_binary(int(time.time()), 32, bb, MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS)
  send_binary(dt.hour, 6, bb, MAX_BRIGHTNESS, 0, 0)
  send_binary(dt.minute, 6, bb, 0, MAX_BRIGHTNESS, 0)
  send_binary(dt.second, 6, bb, 0, 0, MAX_BRIGHTNESS)
  send_binary(0, 10, bb, 0, 0, 0) # padding empty pixels - can add more info
  bb.show()
  bb.close()

def send_binary(word, length, blinky, r, g, b):
  fmt = "{0:0" + str(length) + "b}"
  array = list(fmt.format(word))
  for bit in array:
    blinky.sendPixel(r*int(bit),g*int(bit),b*int(bit))
    
###

parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default=None)
(options, args) = parser.parse_args()

if options.portname != None:
  port = options.portname
else:
  print "Usage: python binary_clock.py -p <port name>"
  print "(ex: python binary_clock.py -p /dev/ttypACM0)"
  exit()
  
time.sleep(1 - datetime.now().microsecond/1000000.0) # roughly syncronize with seconds

while True:
  timeBegin = time.time()

  display(port)

  timeEnd = time.time()
  timeElapsed = timeEnd - timeBegin
  time.sleep(1-timeElapsed)
