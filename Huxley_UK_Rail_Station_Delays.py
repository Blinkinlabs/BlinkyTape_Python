"""
Huxley - UK Live Train Status Blinky Tape Example

This example uses the Huxley Live Departure Board delays endpoint:
https://github.com/jpsingleton/Huxley#delays

If there are delays between the configured stations then the Blinky Tape will throb red.

To run on default (Raspberry Pi) USB serial port: python Huxley_UK_Rail_Station_Delays.py &

(C) 2015 James Singleton
MIT Licensed

"""

from BlinkyTape import BlinkyTape
from time import sleep
import optparse
import urllib
import json
import tempfile


# This token will only work on the demo server. You may also want to host Huxley yourself.
# Get a token here: https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration
accessToken = "DA1C7740-9DA0-11E4-80E6-A920340000B1"

# CRS codes here: http://www.nationalrail.co.uk/static/documents/content/station_codes.csv
crs = "clj"        # Clapham Junction
filterCrs = "wat"  # to Waterloo
trainTime = "0825" # STD of a specific train to look for (24hr format HHmm) blank for none


# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python huxley.py -p <port name>"
    print "(ex.: python huxley.py -p /dev/ttyACM0)"
    exit()

url = "https://huxley.apphb.com/delays/{}/to/{}/50/{}?accessToken={}".format(crs, filterCrs, trainTime, accessToken)

bt = BlinkyTape(port)

# Some visual indication that it works for headless setups (green tape)
bt.displayColor(0, 100, 0)
sleep(2)
# Tape resets to stored pattern after a couple of seconds of inactivity

while True:
    try:
        print "GET %s" % (url)
        rawHttpResponse = urllib.urlopen(url)
        stationStatus = json.load(rawHttpResponse)

        if not len(stationStatus) or stationStatus is None:
            raise Exception("Error parsing data")

        alert = stationStatus["delays"] # bool

        print "%s to %s - Trains Delayed by over 5 minutes: %s" % (
        stationStatus["locationName"], stationStatus["filterLocationName"], stationStatus["delays"])

        # Throb red for delays (or black for none) - takes at least 2 min
        for xx in range(0,60):
            for xy in xrange(0, 100):
                bt.displayColor(xy * alert, 0, 0)
                sleep(0.01)
            for yx in xrange(100, 0, -1):
                bt.displayColor(yx * alert, 0, 0)
                sleep(0.01)

    except:
        # Blue indicates an error
        bt.displayColor(0, 0, 100)
        sleep(120) # wait 2 min
        pass

