"""
Huxley - UK Live Train Status Blinky Tape Example

This example uses the Huxley Live Departure Board delays endpoint:
https://github.com/jpsingleton/Huxley#delays

If there are delays between the configured stations then the Blinky Tape will throb red.

To run on default (Raspberry Pi) USB serial port: python Huxley_UK_Rail_Station_Delays.py &

(C) 2015 James Singleton (https://unop.uk)
MIT Licensed

"""

import tempfile
import json
from blinkytape import BlinkyTape
from time import sleep
from itertools import chain
import optparse
import sys
if sys.version_info > (3, 0):
    import urllib.request as requestlib
else:
    import urllib2 as requestlib


# This token will only work on the demo server. You may also want to host Huxley yourself.
# Get a token here: https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration
accessToken = "DA1C7740-9DA0-11E4-80E6-A920340000B1"

# CRS codes here: http://www.nationalrail.co.uk/static/documents/content/station_codes.csv
crs = "clj"        # Clapham Junction
filterCrs = "wat"  # to Waterloo
# STD of a specific train to look for (24hr format HHmm) blank for none
trainTime = ""


# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print("Usage: python Huxley_UK_Rail_Station_Delays.py -p <port name>")
    print("(ex.: python Huxley_UK_Rail_Station_Delays.py -p /dev/ttyACM0)")
    exit()

url = "https://huxley.apphb.com/delays/{}/to/{}/50/{}?accessToken={}".format(
    crs, filterCrs, trainTime, accessToken)

bt = BlinkyTape(port)

# Some visual indication that it works for headless setups (green tape)
bt.displayColor(0, 100, 0)
sleep(2)
# Tape resets to stored pattern after a couple of seconds of inactivity

while True:
    try:
        print("GET %s" % (url))
        rawHttpResponse = requestlib.urlopen(url)
        stationStatus = json.load(rawHttpResponse)

        if not len(stationStatus) or stationStatus is None:
            raise Exception("Error parsing data")

        alert = stationStatus["delays"]  # bool

        print("%s to %s - Trains Delayed by over 5 minutes: %s" % (
            stationStatus["locationName"], stationStatus["filterLocationName"], stationStatus["delays"]))

        # Throb red for delays (or black for none) - takes at least 2 min
        for x in range(60):
            for y in chain(range(100), range(100, 0, -1)):
                bt.displayColor(y * alert, 0, 0)
                sleep(0.01)

    except:
        # Blue indicates an error
        bt.displayColor(0, 0, 100)
        sleep(120)  # wait 2 min
        pass
