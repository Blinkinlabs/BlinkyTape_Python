from BlinkyTape import BlinkyTape
import time

bb = BlinkyTape()

while True:

    for x in range(60):
        bb.sendPixel(255, 255, 255)
    bb.show()
    time.sleep(.03)

    for x in range(60):
        bb.sendPixel(0, 0, 0)
    bb.show()
    time.sleep(.03)
