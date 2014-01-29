from BlinkyTape import BlinkyTape

bb = BlinkyTape('/dev/tty.usbmodemfa131')

while True:

    for x in range(60):
        bb.sendPixel(10, 10, 10)
    bb.show()

    for x in range(60):
        bb.sendPixel(0, 0, 0)
    bb.show()
