from BlinkyTape import BlinkyTape
from time import sleep

bb = BlinkyTape('/dev/ttyACM0')

while True:
  bb = BlinkyTape('/dev/ttyACM0')
  for x in range(0, 60):
    for y in range(0, 60):
      l = max(((y-x)%60)-40,0)
      bb.sendPixel(l*3,l*3,l*3)
    bb.show()
    sleep(0.005)
  bb.close()

