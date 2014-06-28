#!/usr/bin/env python


class FixedColorMixin(object):
    def __init__(self, fixed_color=None, *args, **kwargs):
        super(FixedColorMixin, self).__init__(*args, **kwargs)
        self.fixed_color = fixed_color
