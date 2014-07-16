"""Simple animation example using BlinkyTape.py"""

from BlinkyTape import BlinkyTape
from time import sleep
import optparse

parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyUSB0)", default=None)
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python scanline.py -p <port name>"
    print "(ex.: python scanline.py -p /dev/ttypACM0)"
    exit()

blinky = BlinkyTape(port)

while True:
    for x in range(60):
        for y in range(60):
            l = max(((y - x) % 60) - 40, 0)
            blinky.sendPixel(l * 3, l * 3, l * 3)
        blinky.show()
        sleep(0.01)
