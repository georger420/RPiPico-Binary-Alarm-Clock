# georger420
#

#Include the library files

import time
from machine import Pin, freq
import print_error
from nec import NEC_8

#Define the IR receiver pin and motor pins
pin_ir = Pin(12, Pin.IN)

def decodeKeyValue(data):
    return data
    
# User callback
def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print(data)
       
ir = NEC_8(pin_ir, callback)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

try:
    while True:
        pass
except KeyboardInterrupt:
    ir.close()

