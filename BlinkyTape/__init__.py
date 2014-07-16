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

from BlinkyTape import BlinkyTape
from IndexBlinkyTape import IndexBlinkyTape
from ModeManager import ModeManager

# For compatability purposes
mode_manager = ModeManager

# Make flake8 happy
assert BlinkyTape
assert IndexBlinkyTape
