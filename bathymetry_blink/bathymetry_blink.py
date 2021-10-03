"""
This script will modulate the blinky lights using the following algorithm:

1) uses time of day to map to a particular latitude of the earth 
2) obtain the entire latitude's worth of elevation data via netCDF
3) scales the entire circumferential elevation data to fit the entire color spectrum
4) transmits entire circumferential elevation profile to BlinkyLights
5) Updates every 10 minutes

Uses the following arguments:

-l/--location: tuple 
	Location of the user in tuple(lat, lon). This represents the center of the LED strip. Defaults to (0, 0)
-u/--update-interval: int
	Update interval of the script, in minutes. Defaults to 10.
-p/--port: str
	Serial port of the BlinkyLight (e.g., 'ttyAMA0', 'COM3'). Defaults to 'COM5'. 
-d/--delate_latitude: int
    Vertical change in latitude every update rate. May be 0, but this will result in a never-changing LEDs. 

In lieu of providing command line arguments, you may alternatively edit the defaults in bath_config.json. 

(C) 2021 Joseph Post (https://joeycodes.dev)
MIT Licensed

"""


import optparse
import json
from blinkytape import BlinkyTape
from time import sleep
from xml.etree import ElementTree
import sys

# Obtain default parameters
with open("./bathy_config.json") as f:
    config = json.load(f)

# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default=config["port"])

parser.add_option("-l", "--location", dest="location",
                  help="Location of the center of the LED strip (ex: 70,-110)", default=config["location"])

parser.add_option("-u", "--update-rate", dest="update_rate",
                  help="How often to update elevation profile (mins) (ex: 5)", default=config["update_rate"])

parser.add_option("-d", "--delta-latitude", dest="delta_latitude",
                  help="Change in latitude during update (ex: 5)", default=config["delta_latitude"])

parser.add_option("-n", "--num-leds", dest="num_leds",
                  help="Number of LEDs in strip (ex: 60)", default=config["num_leds"])

(options, args) = parser.parse_args()

if args:
    print("Unknown parameters: " + args)

# grab the values provided by user (or defaults)
port = options.portname
loc = options.location
rate = options.update_rate
delta = options.delta_latitude
n_leds = options.num_leds

# Some visual indication that it works, for headless setups (green tape)
bt = BlinkyTape(port, n_leds)
bt.displayColor(0, 100, 0)
bt.show()
sleep(2)

while True:
    try:
        print("GET %s" % (url))
        rawXml = opener.open(request).read()
        tree = ElementTree.fromstring(rawXml)

        if not len(tree) or tree is None:
            raise Exception("Error loading data")

        currentStateName = tree.find('current').find('state').get('name')
        print(currentStateName)

        if currentStateName != "red":
            for x in range(300):
                bt.displayColor(0, 0, 0)
                sleep(1)
        else:
            # Tape resets to stored pattern after a few seconds of inactivity
            sleep(rate * 60)  # Wait specified number of minutes

    except KeyboardInterrupt:
        print("Keyboard interrupt, ending program.")

        # just show blue and disconnect.
        bt.displayColor(0, 0, 100)
        bt.close()
