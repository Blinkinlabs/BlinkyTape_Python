"""
  Indexed BlinkyTape Class
  ------------------------

  This class extends the BlinkyTape class by letting the user set the color
  of specific LEDs.
"""

from .BlinkyTape import BlinkyTape


class IndexBlinkyTape(BlinkyTape):
    """
        Control BlinkyTape by setting the color of indivdidual LED's. When
        self.show() is called the LED's will be lit according to the last
        color set for that LED.
    """
    def __init__(self, *args, **kwargs):
        BlinkyTape.__init__(self, *args, **kwargs)
        self._LEDs = []

        # Create the LED index set to (0, 0, 0) by default
        for led in self.ledCount:
            self._LEDs.append((0, 0, 0))

    def set_led_color(self, led, r, g, b):
        """
            Sets the color for a particular LED.
        """
        self._LEDs[led] = (r, g, b)

    def show(self):
        """
            Set the LED colors as currently stored.
        """
        self.send_list(self._LEDs)
