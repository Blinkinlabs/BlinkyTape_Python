import blinkytape
import time

blinky = blinkytape.BlinkyTape()

while True:

    for x in range(60):
        blinky.sendPixel(255, 255, 255)
    blinky.show()
    time.sleep(.03)

    for x in range(60):
        blinky.sendPixel(0, 0, 0)
    blinky.show()
    time.sleep(.03)
