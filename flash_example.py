import time
from BlinkyTape import BlinkyTape
  
bb = BlinkyTape('/dev/ttyACM0')

while True:

  print "Sending ON"
  for x in range(1,60):
    bb.sendPixel(255 / x, 255 / x, 255 / x)
  bb.show()
  print "Sent ON"

  time.sleep(0.1)

  print "Sending Off"
  bb.displayColor(0,0,0)
  print "Sent Off"

  time.sleep(0.1)
