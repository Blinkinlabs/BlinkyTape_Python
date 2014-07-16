"""
  BlinkyTape Python communication library.
  ----------------------------------------

  This code assumes stock serialLoop() in the firmware.

  Commands are issued in 3-byte blocks, with pixel data
  encoded in RGB triplets in range 0-254, sent sequentially
  and a triplet ending with a 255 causes the accumulated pixel
  data to display (a show command).

  Note that with the stock firmware changing the maximum brightness
  over serial communication is impossible.
"""

import logging
import serial


def to_chr(number):
    """
        Converts a number to it equivalent character.
    """
    if number < 0:
        number = 0
    elif number > 254:
        number = 254

    return chr(number)


class NullHandler(logging.Handler):
    """
        A logging handler which does nothing so that applications which don't
        configure logging won't print a warning.
    """
    def emit(self, record):
        pass


class BlinkyTape(object):
    """
        Creates a BlinkyTape object and opens the port.

        Parameters:

          port
            Required, port name as accepted by PySerial library:

            http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial

            It is the same port name that is used in Arduino IDE.
            Ex.: COM5 (Windows), /dev/ttyACM0 (Linux).

          ledCount
            Optional, total number of LEDs to work with, defaults to 60
            LEDs. The limit is enforced and an attempt to send more pixel
            data will throw an exception.

          buffered
            Optional, enabled by default. If enabled, will buffer pixel
            data until a show command is issued. If disabled, the data
            will be sent in byte triplets as expected by firmware, with
            immediate flush of the serial buffers (slower).

          log_level
            What log level to set.
    """
    def __init__(self, port, ledCount=60, buffered=True,
                 log_level=logging.DEBUG):
        self.control = chr(0) + chr(0) + chr(255)
        self.port = port
        self.ledCount = ledCount
        self.position = 0
        self.buffered = buffered
        self.buf = ""
        self.serial = serial.Serial(port, 115200)

        # Setup logging
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)
        self.log.addHandler(NullHandler())

        self.log.debug('BlinkyTape initialized!')
        self.show()  # Flush any incomplete data

    def send_list(self, colors):
        """
            Set all the LED's at once by passing in a list of color tuples.
        """
        self.log.debug('send_list(%s)', colors)
        if len(colors) > self.ledCount:
            raise RuntimeError("Attempting to set pixel outside range!")

        self.show()  # Ensure that we start at LED 0

        # Concatenate all the LED commands together
        colors = [''.join(map(to_chr, color)) for color in colors]
        data = ''.join(colors)

        # Send the commands to the BlinkyTape
        self.serial.write(data)
        self.show()

    def sendPixel(self, r, g, b):
        """
            Sends the next pixel data triplet in RGB format.

            Values are clamped to 0-254 automatically.

            Throws a RuntimeException if [ledCount] pixels are already set.
        """
        self.log.debug('sendPixel(%s, %s, %s)', r, g, b)

        data = ''.join((to_chr(r), to_chr(g), to_chr(b)))

        if self.position > self.ledCount:
            raise RuntimeError("Attempting to set pixel outside range!")

        if self.buffered:
            self.buf += data
        else:
            self.serial.write(data)
            self.serial.flush()

        self.position += 1

    def show(self):
        """
            Sends the command(s) to display all accumulated pixel data.

            Resets the next pixel position to 0, flushes the serial buffer,
            and discards any accumulated responses from BlinkyTape.
        """
        self.log.debug('show()')

        if self.buffered:
            self.serial.write(self.buf)
            self.buf = ""

        self.serial.write(self.control)
        self.serial.flush()
        self.serial.flushInput()  # Clear responses from BlinkyTape, if any
        self.position = 0

    def displayColor(self, r, g, b):
        """
            Fills self.ledCount pixels with the color described by r, g, b.
        """
        self.log.debug('displayColor(%s, %s, %s)', r, g, b)
        for i in range(0, self.ledCount):
            self.sendPixel(r, g, b)

        self.show()

    def resetToBootloader(self):
        """
            Initiates a reset on BlinkyTape. Note that it will be disconnected.
        """
        self.log.debug('resetToBootloader()')
        self.serial.setBaudrate(1200)
        self.close()

    def close(self):
        """
            Safely closes the serial port.
        """
        self.log.debug('close()')
        self.serial.close()
