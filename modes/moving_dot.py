import random
from .base import BaseMode
from .mixins import FixedColorMixin


class MovingDotMode(FixedColorMixin, BaseMode):
    last = 0
    color = (0, 0, 254)
    change = 1

    def calc_next_step(self):
        self.colors[self.last] = (0, 0, 0)
        self.last += self.change
        if self.last >= self.led_count:
            self.change = -1
            self.last = self.led_count - 1
        elif self.last <= 0:
            self.change = 1
            self.last = 0
        self.colors[self.last] = self.fixed_color if self.fixed_color else self.color


class WideMovingDotMode(FixedColorMixin, BaseMode):
    last = 0
    color = (0, 0, 254)
    change = 1
    fps = 50

    def __init__(self, width=5, *args, **kwargs):
        self.led_count = self.led_count + width * 2
        super(WideMovingDotMode, self).__init__(*args, **kwargs)
        self.width = width

    def calc_next_step(self):
        self.colors[self.last + (self.width * self.change * (-1))] = (0, 0, 0)
        self.last += self.change
        if self.last >= self.led_count:
            self.change = -1
            self.last = self.led_count - self.width - 1
            self.color = (0, 0, 0)
            while self.color == (0, 0, 0):
                self.color = (
                    random.randint(0, 1) * 254,
                    random.randint(0, 1) * 254,
                    random.randint(0, 1) * 254
                )
        elif self.last <= 0:
            self.change = 1
            self.last = self.width
            self.color = (0, 0, 0)
            while self.color == (0, 0, 0):
                self.color = (
                    random.randint(0, 1) * 254,
                    random.randint(0, 1) * 254,
                    random.randint(0, 1) * 254
                )
        self.colors[self.last] = self.fixed_color if self.fixed_color else self.color

    def get_colors(self):
        return self.colors[self.width:len(self.colors) - self.width]
