"""Simple animation example using BlinkyTape.py"""

from BlinkyTape import BlinkyTape
from time import sleep
import optparse

parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyUSB0)", default=None)
parser.add_option("-c", "--count", dest="ledcount",
                  help="LED count", default=60, type=int)
parser.add_option("-s", "--size", dest="size",
                  help="Size of the light wave", default=20, type=int)
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print("Usage: python scanline.py -p <port name>")
    print("(ex.: python scanline.py -p /dev/ttypACM0)")
    exit()

blinky = BlinkyTape(port, options.ledcount)

while True:
    for position in range(-options.size, options.ledcount + options.size):
        for led in range(options.ledcount):
            if abs(position - led) < options.size:
                blinky.sendPixel(255,0,200)
            else:
                blinky.sendPixel(0,0,0)
        blinky.show()
        sleep(0.005)
