class FixedColorMixin(object):
    def __init__(self, fixed_color=None, *args, **kwargs):
        super(FixedColorMixin, self).__init__(*args, **kwargs)
        self.fixed_color = fixed_color

    def pick_color(self):
        return self.fixed_color if self.fixed_color else self.color
