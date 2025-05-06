# georger420
#

from machine import Pin
import utime

from dht2 import DHT11, InvalidChecksum


# Wait 1 second to let the sensor power up
utime.sleep(1)

dhtpin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
dhtsensor = DHT11(dhtpin)

while True:
    utime.sleep(2)
    try:
        print("Temperature: {}".format(dhtsensor.temperature))
        print("Humidity: {}".format(dhtsensor.humidity))
    except InvalidChecksum:
        print("Checksum from the sensor was invalid")
