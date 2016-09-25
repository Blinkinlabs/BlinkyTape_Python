"""
London Underground Status for Blinky Tape

To run on default (Raspberry Pi) USB serial port: python London_Underground_Status.py &

(C) 2015 James Singleton (https://unop.uk)
MIT Licensed

"""

from blinkytape import BlinkyTape
from time import sleep
import optparse
import urllib
import json
import tempfile

# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python London_Underground_Status.py -p <port name>"
    print "(ex.: python London_Underground_Status.py -p /dev/ttyACM0)"
    exit()

url = "https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status"

colours = { "bakerloo" : (137, 78, 36),
            "central" : (220, 36, 31),
            "circle" : (255, 206, 0),
            "district" : (0, 114, 41),
            "dlr" : (0, 175, 173),
            "hammersmith-city" : (215, 153, 175),
            "jubilee" : (106, 114, 120), 
            "london-overground" : (232, 106, 16),
            "metropolitan" : (117, 16, 86),
            "northern" : (0, 0, 0),
            "piccadilly" : (0, 25, 168),
            "victoria" : (0, 160, 226),
            "waterloo-city" : (118, 208, 189),
            "tfl-rail" : (0, 25, 168) }

bt = BlinkyTape(port)

# Some visual indication that it works for headless setups (green tape)
bt.displayColor(0, 100, 0)
sleep(2)
# Tape resets to stored pattern after a couple of seconds of inactivity

while True:
    try:
        print "GET %s" % (url)
        rawHttpResponse = urllib.urlopen(url)
        lines = json.load(rawHttpResponse)

        if not len(lines) or lines is None:
            raise Exception("Error parsing data")

        # Sort the lines
        lines.sort(key = lambda l: l['modeName'], reverse = True)

        # Takes at least 2 min
        for cycles in xrange(240):
            for pixel in xrange(2):
                bt.sendPixel(0, 0, 0)
            for line in lines:
                alert = False
                for status in line['lineStatuses']:
                    # https://api.tfl.gov.uk/line/meta/severity
                    if status['statusSeverity'] != 10:
                        alert = True
                r, g, b = colours[line['id']]
                for pixel in xrange(4):
                    if alert:
                        # Flash for delays
                        l = (cycles - pixel) % 2
                        if line['id'] == "northern":
                            # Because black on black doesn't show up
                            r, g, b = 100, 100, 100
                        bt.sendPixel(l * r, l * g, l * b)
                    else:
                        bt.sendPixel(r, g, b)
            for pixel in xrange(2):        
                bt.sendPixel(0, 0, 0)
            bt.show()
            sleep(0.5)

    except:
        # Blue indicates an error
        bt.displayColor(0, 0, 100)
        sleep(120) # wait 2 min
        pass

