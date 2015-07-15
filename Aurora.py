"""
Aurora Alert for Blinky Tape

To run on default (Raspberry Pi) USB serial port: python Aurora.py &

This script works by turning off the tape when there is no Aurora.
You need to save one of the images to the tape with pattern paint first.

(C) 2015 James Singleton (https://unop.uk)
MIT Licensed

"""

from BlinkyTape import BlinkyTape
from time import sleep
from xml.etree import ElementTree
import urllib2
import optparse

# Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="portname",
                  help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
(options, args) = parser.parse_args()

if options.portname is not None:
    port = options.portname
else:
    print "Usage: python Aurora.py -p <port name>"
    print "(ex.: python Aurora.py -p /dev/ttyACM0)"
    exit()

# Documentation: http://aurorawatch.lancs.ac.uk/api_info/
# Code and spec: https://github.com/stevemarple/AuroraWatchNet
url = 'http://aurorawatch.lancs.ac.uk/api/0.1/status.xml'
bt = BlinkyTape(port)

request = urllib2.Request(url)
request.add_header('User-Agent', 'BlinkyTape Aurora Alert unop.uk')
opener = urllib2.build_opener()

# Some visual indication that it works, for headless setups (green tape)
bt.displayColor(0, 100, 0)
sleep(2)

while True:
    try:
        print "GET %s" % (url)
        rawXml = opener.open(request).read()
        tree = ElementTree.fromstring(rawXml)  

        if not len(tree) or tree is None:
            raise Exception("Error loading data")

        currentStateName = tree.find('current').find('state').get('name')
        print currentStateName

        if currentStateName != "red":
            for x in xrange(300):
                bt.displayColor(0, 0, 0)
                sleep(1)
        else:
            # Tape resets to stored pattern after a few seconds of inactivity
            sleep(300) # Wait 5min
            
    except:
        # Blue indicates an error
        bt.displayColor(0, 0, 100)
        sleep(300) # Wait 5min
        pass

