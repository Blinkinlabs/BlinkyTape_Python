"""BlinkyTape Python communication library.

  This code assumes stock serialLoop() in the firmware.

  Commands are issued in 3-byte blocks, with pixel data
  encoded in RGB triplets in range 0-254, sent sequentially
  and a triplet ending with a 255 causes the accumulated pixel
  data to display (a show command).

  Note that with the stock firmware changing the maximum brightness
  over serial communication is impossible.
"""

from serial.tools import list_ports
import re
import platform

def listPorts():
    allPorts = list_ports.comports()

    ports = []

    # Regular expression that identifies the serial port to use
    # for OS/X:
    if platform.system() == 'Darwin':
        match = '/dev/tty\.usb*'

    # For Linux:
    elif platform.system() == 'Linux':
        match = '/dev/ttyACM*'

    # TODO: Windows ?

    else:
        match = "*"

    for port in allPorts:
        # If the port name is acceptable, add it to the list
        if re.match(match, port[0]) != None:
            ports.append(port[0])

    return ports

# Example code

if __name__ == "__main__":

    print listPorts()
