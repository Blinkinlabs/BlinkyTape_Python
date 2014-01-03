import random
from .base import BaseMode
from .mixins import FixedColorMixin


class RandomFlashMode(FixedColorMixin, BaseMode):
    last = 0

    def calc_next_step(self):
        self.colors[self.last] = (0,0,0)
        self.last = random.randint(0,len(self.colors)-1)
        if self.fixed_color:
            self.colors[self.last] = self.fixed_color
        else:
            self.colors[self.last] = (
                random.randint(0,254),
                random.randint(0,254),
                random.randint(0,254)
            )


class FillUpMode(FixedColorMixin, BaseMode):
    last = 0
    pos = 0
    fill = 1
    color = (0, 0, 254)
    clear_last = 0

    def __init__(self, *args, **kwargs):
        super(FillUpMode, self).__init__(*args, **kwargs)
        self.last = self.led_count - 1

    def calc_next_step(self):
        if self.clear_last:
            self.colors[self.last] = (0,0,0)
        if self.fill:
            self.last -= 1
            self.colors[self.last] = self.fixed_color if self.fixed_color else self.color
            if self.last > self.pos:
                self.clear_last = 1
            else:
                self.last = self.led_count - 1
                self.pos += 1
                self.clear_last = 0
                if self.pos == self.led_count:
                    self.pos = 0
                    self.fill = 0
                    self.last = 0
                    self.clear_last = 1
        else:
            self.clear_last = 1
            self.last -= 1
            if self.last < 0:
                self.pos += 1
                self.last = self.pos
                if self.pos == self.led_count:
                    self.pos = 0
                    self.fill = 1
                    self.clear_last = 0
                    self.color = (0,0,0)
                    while self.color == (0,0,0):
                        self.color = (
                            random.randint(0,1)*254,
                            random.randint(0,1)*254,
                            random.randint(0,1)*254
                        )
            if not self.fill:
                self.colors[self.last] = self.fixed_color if self.fixed_color else self.color


class FlashMode(FixedColorMixin, BaseMode):
    on = 0
    color = (0, 0, 254)

    def calc_next_step(self):
        if self.on:
            self.on = 0
            for i in range(self.led_count):
                self.colors[i] = (0,0,0)
        else:
            self.on = 1
            for i in range(self.led_count):
                self.colors[i] = self.fixed_color if self.fixed_color else self.color

