# georger420
#

from machine import Pin, SPI, RTC, ADC
import max7219
spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(1)
display.fill(0)
display.show()