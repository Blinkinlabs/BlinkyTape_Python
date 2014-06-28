"""Simple animation example using BlinkyTape.py"""

import blinkytape
import time 
import optparse

parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyUSB0)", default=None)
(options, args) = parser.parse_args()
port = options.portname

blinky = blinkytape.BlinkyTape(port)

while True:
    for x in range(60):
        for y in range(60):
            l = max(((y - x) % 60) - 40, 0)
            blinky.sendPixel(l * 3, l * 3, l * 3)
        blinky.show()
        time.sleep(0.01)
