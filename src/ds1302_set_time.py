# georger420
#
from machine import Pin, RTC
import ds1302

rtc = RTC()

# DS1302 settings
ds = ds1302.DS1302(Pin(18),Pin(19),Pin(17))
# start oscilator DS1302
pom = ds.second()
print(pom)
if (pom >=128):
    ds.second(pom - 128)
print(ds.second()) 

ds_cas = ds.date_time()
print("DS cas pred nastavenim: ",ds_cas)



pico_cas = rtc.datetime()
print("Pico cas", pico_cas)

ds.date_time([pico_cas[0], pico_cas[1], pico_cas[2], pico_cas[3], pico_cas[4], pico_cas[5], pico_cas[6]])

dscas2 = ds.date_time()
print("DS cas: ", dscas2)


