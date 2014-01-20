from BlinkyTape import BlinkyTape


class BaseMode(object):
    fps = 10
    led_count = 60
    no_sleep = False

    def __init__(self, fps=None, led_count=None, no_sleep=None, *args, **kwargs):
        self.colors = list()
        for i in range(self.led_count):
            self.colors.append((0, 0, 0))
        if fps:
            self.fps = fps
        if led_count:
            self.led_count = led_count
        if no_sleep:
            self.no_sleep = no_sleep

    def calc_next_step(self):
        raise NotImplemented()

    def get_colors(self):
        return self.colors
