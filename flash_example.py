from BlinkyTape import BlinkyTape
from time import sleep
  
bb = BlinkyTape('/dev/ttyACM1')

while True:

  for x in range(0, 30):
    for y in range(0, 30):
      l = max(((y-x)%60)-40,0)
      bb.sendPixel(l,l,l)
    bb.show()
    #sleep(0.2)
