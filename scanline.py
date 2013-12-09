from BlinkyTape import BlinkyTape
from time import sleep

bb = BlinkyTape('/dev/ttyACM0', debug=True)
n = 0

while True:
  # bb = BlinkyTape('/dev/ttyACM0', debug=True)
  n += 1
  print ">> " + str(n)
  for x in range(0, 60):
    for y in range(0, 60):
      l = max(((y-x)%60)-40,0)
      bb.sendPixel(l*3,l*3,l*3)
    bb.show()
    bb.close()
    sleep(0.01) # BlinkyTape seems unstable if commands are issued too quickly
    bb.reopen() # peSerial(?) seems unstable after a los of writes
  # bb.close()
  # bb.reopen() 

