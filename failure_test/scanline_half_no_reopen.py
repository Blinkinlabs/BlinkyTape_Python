from BlinkyTape import BlinkyTape
from time import sleep
import optparse

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
	
bb = BlinkyTape(port, debug=True)
n = 0

while True:
  # bb = BlinkyTape('/dev/ttyACM0', debug=True)
  n += 1
  print ">> " + str(n)
  for x in range(0, 30):
    for y in range(0, 30):
      l = max(((y-x)%30)-10,0)
      bb.sendPixel(l*3,l*3,l*3)
    bb.show()
  # bb.close()
    sleep(0.01) # BlinkyTape seems unstable if commands are issued too quickly
  # bb.reopen() # pySerial(?) seems unstable after a lots of writes