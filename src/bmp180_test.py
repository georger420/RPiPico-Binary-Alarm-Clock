# georger420
#

from bmp180 import BMP180
from machine import I2C, Pin                        # create an I2C bus object accordingly to the port you are using

h = 236	#altitude in meters read from geographical map

sda = machine.Pin(8)
scl = machine.Pin(9)
bus = machine.I2C(0, sda=sda, scl=scl, freq=100000)

# bus = I2C(1, baudrate=100000)           # on pyboard
# bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # on esp8266
bmp180 = BMP180(bus)
bmp180.oversample_sett = 3
bmp180.baseline = 101325
bmp180.debug = True

temp = bmp180.temperature
p = bmp180.pressure
altitude = bmp180.altitude
print("Temperature: ", temp, " °C")
print("Pressure:    ", p / 100, " hP")
print("Altitude:    ", altitude, " m")

p0 = p / pow(1.0 - 0.0065 * h / (temp + 273.15), 5.255);
print("Pressure recalculated to altitude ", h, "m: ", p0 / 100, " hP")
