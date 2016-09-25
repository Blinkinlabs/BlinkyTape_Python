""" Easily see your GPU temperature while gaming!  This sets the LED colors base on your Nvidia GPU temperature, every second.  
60F = green, 70F = yellow, 80F = red
"""

import time
from blinkytape import BlinkyTape
import subprocess
import os
import re

## To find your COM port number in Windows, run "Pattern Paint -> Help -> System Information"
#bb = BlinkyTape('/dev/tty.usbmodemfa131')
bb = BlinkyTape('COM3')

while True:

    output = subprocess.check_output(["C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe", "-a"], shell=True)
    #os.popen('C:\\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe')
    #output=os.popen("C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe").read()
    
    #print("====" + str(output) + "=====")
    temp = re.search("GPU Current.*",output).group()[30:33]
    temp_baseline = 60
    temp_multiplier = 5
    color_temp = (int(temp) - temp_baseline ) * temp_multiplier
    green = 100 - color_temp
    red = 0 + color_temp
    blue = 0
    print "Current GPU Temp: %s   RGB: %s %s %s" % (temp, red, green, blue)
    
    for x in range(60):
        bb.sendPixel(red, green, blue)
    bb.show()
    
    #time.sleep(1)
    
    #for x in range(60):
    #    bb.sendPixel(100, 0, 0)
    #bb.show()

    time.sleep(1)

    
