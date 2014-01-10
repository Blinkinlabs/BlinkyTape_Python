"""Binary clock example using BlinkyTape.py

Displays UNIX epoch time using 32 LEDs (white),
  localtime hours using 6 LEDs (red),
  localtime minutes using 6 LEDs (green),
  localtime seconds using 6 LEDs (blue)
"""
from BlinkyTape import BlinkyTape
import time
from datetime import datetime, timedelta
import optparse

MAX_BRIGHTNESS = 50  # in range(255)


def display(blinky):
    dt = datetime.now()
    send_binary(int(time.time()), 32, blinky, MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS)
    send_binary(dt.hour, 6, blinky, MAX_BRIGHTNESS, 0, 0)
    send_binary(dt.minute, 6, blinky, 0, MAX_BRIGHTNESS, 0)
    send_binary(dt.second, 6, blinky, 0, 0, MAX_BRIGHTNESS)
    send_binary(0, 10, blinky, 0, 0, 0)  # padding empty pixels - can add more info
    blinky.show()


def send_binary(word, length, blinky, r, g, b):
    fmt = "{0:0" + str(length) + "b}"
    array = list(fmt.format(word))
    for bit in array:
        blinky.sendPixel(r * int(bit), g * int(bit), b * int(bit))


parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyUSB0)", default=None)
options, args = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python binary_clock.py -p <port name>"
    print "(ex: python binary_clock.py -p /dev/ttypACM0)"
    exit()

blinky = BlinkyTape(port)
time.sleep(1 - datetime.now().microsecond / 1000000.0)  # roughly synchronize with seconds

while True:
    timeBegin = time.time()

    display(blinky)

    timeEnd = time.time()
    timeElapsed = timeEnd - timeBegin
    time.sleep(1 - timeElapsed)
