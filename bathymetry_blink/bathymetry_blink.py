"""
This script will modulate the blinky lights using the following algorithm:

1) uses user-provided location to obtain row of pixel data from bathy image
2) samples a 'number of LEDs' number of pixels from that row
3) shifts the sampled row data to center it at the location specified by user
4) displays resulting pixels on Blinky Tape
5) shifts next row by a given latitude, also specified by user
6) sleeps for user-specified period of time

Uses the following arguments:

-l/--location: tuple 
	Location of the user in tuple(lat, lon). This represents the center of the LED strip. Defaults to (0, 0)
-u/--update-interval: int
	Update interval of the script, in minutes. Defaults to 10.
-p/--port: str
	Serial port of the BlinkyLight (e.g., 'ttyAMA0', 'COM3'). Defaults to 'COM5'. 
-d/--delta_latitude: int
    Vertical change in latitude every update rate. May be 0, but this will result in a never-changing LEDs. 
-i/--image: str
    Name of the PNG image that contains the color coded pathymetric data.

The file current named mapserv.png was obtained using the following API:
https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv?request=getmap&service=wms&BBOX=-90,-180,90,180&format=image/png&height=600&width=1200&crs=EPSG:4326&layers=GEBCO_LATEST_SUB_ICE_TOPO&version=1.3.0

In lieu of providing command line arguments, you may alternatively edit the defaults in bath_config.json. 

NOTE: runs via:
runfile('/BlinkyTape_Python/bathymetry_blink/bathymetry_blink.py', wdir='/BlinkyTape_Python/')

(C) 2021 Joseph Post (https://joeycodes.dev)
MIT Licensed

"""


import optparse
import json
from blinkytape import BlinkyTape
from time import sleep
from PIL import Image
import numpy as np
from serial import PortNotOpenError

# Obtain default parameters
with open("./bathymetry_blink/bathy_config.json") as f:
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

parser.add_option("-i", "--image", dest="image_name",
                  help="Name of the map/bathymetry image (ex: ./mapserv.png)", default=config["image"])                  

(options, args) = parser.parse_args()

if args:
    print("Unknown parameters: " + args)

# grab the values provided by user (or defaults)
port = options.portname
loc = options.location
rate = options.update_rate
delta = options.delta_latitude
n_leds = options.num_leds
i_name = options.image_name

# Some visual indication that it works, for headless setups (green tape)
bt = BlinkyTape(port, n_leds)
bt.displayColor(0, 100, 0)
bt.show()
sleep(2)

while True:
    try:
        # first, load image
        im = Image.open(i_name) # Can be many different formats.
        cols, rows = im.size 
        a = np.asarray(im)  # of shape (rows, cols, channels)

        # map loc latitude to 0-based index 
        latitude_index = min(rows - 1, max(0, (int)(((loc[0] - -90) / (90 - -90)) * (rows - 0) + 0)))
        longitude_index = min(cols - 1, max(0, (int)(((loc[1] - -180) / (180 - -180)) * (cols - 0) + 0)))
        
        # update the location of the next row of elevation data to take
        loc[0] += delta 
        loc[0] = loc[0] % rows
        
        print("Lat index: " + str(latitude_index))
        print("Lon index: " + str(longitude_index))
        print("Next latitude: " + str(loc[0]))
        
        
        # grab the applicable pixel indices
        indices = [(int)(x*(1200/n_leds)) for x in range(n_leds)]
        
        # sample that row of pixel data
        output_pixels = np.take(a[latitude_index], indices, axis=0)
        
        # rotate the row such that the center of the 
        output_pixels = np.roll(output_pixels, longitude_index, axis=0)
        
        # send all pixel data to bt
        for pixel in output_pixels:
            print("Sending r: %1, g: %2, b: %3".format(*pixel))
            bt.sendPixel(*pixel)
        
        # finally, show the image
        bt.show()
        
        # delete variables for memory management
        del a
        del im

        # Tape resets to stored pattern after a few seconds of inactivity
        sleep(rate * 60)  # Wait specified number of minutes
        # sleep(10)  # Wait specified number of minutes

    except KeyboardInterrupt:
        print("Keyboard interrupt, ending program.")

        # just show blue and disconnect.
        # bt.displayColor(0, 0, 100)
        bt.resetToBootloader()
        try:
            bt.close()
        except PortNotOpenError as p:
            print("Issue closing serial port: " + p.args[0])
        
    except RuntimeError as e:
        print("Encountered runtime error: " + e.args[0])
        # flush any incomplete data
        bt.show()
        
