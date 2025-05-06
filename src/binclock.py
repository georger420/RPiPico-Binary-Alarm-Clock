# georger420
#

from machine import Pin, SPI, RTC, ADC, PWM, freq, I2C
import max7219
# from time import sleep
import utime
import bitops as bt
import ds1302
import print_error
import nec
import dht2
import bmp180
import nznaky2 as zn

# Infra receiver data pin settings
pin_ir = Pin(12, Pin.IN)

# DS1302 settings
ds = ds1302.DS1302(Pin(18),Pin(19),Pin(17))
# start oscilator DS1302
pom = ds.second()
print(pom)
if (pom >=128):
    ds.second(pom - 128)
print(ds.second())  

# MAX7219 settings
spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(1)
display.fill(0)

# DHT11 control
dhtpin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
dhtsensor = dht2.DHT11(dhtpin)

# BMP180 control
bmpsda = Pin(8)
bmpscl = Pin(9)
bmpbus = I2C(0, sda=bmpsda, scl=bmpscl, freq=100000)
bmp = bmp180.BMP180(bmpbus)
bmp.oversample_sett = 3
bmp.baseline = 101325
bmp.debug = False

# PICO RTC settings
rtc = RTC()
print(rtc.datetime())
print("Control: {}".format(bin(ds.get_control())))


c = ds.date_time()
print("DS1302 time: ", c)
rtc.datetime((c[0], c[1], c[2], c[3], c[4], c[5], c[6], 0))
print("Pico time:", rtc.datetime())

# Pico temperature sensor settings
TempSensor = ADC(4)
conversion_factor = 3.3 / 65535

# Buzzer settings
buzzerPIN=16
BuzzerObj=PWM(Pin(buzzerPIN))

# Alarm settings
budik = [20,30]
print("Alarm: {}:{}".format(budik[0], budik[1]))

actbzucak = 0
nodisplay = 0

# Days of week
dnyvtydnu = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def leadZero(zceho = 0):
    if (zceho < 10):
        return "0" + str(zceho)
    else:
        return str(zceho)

def buzzer(buzzerPinObject,frequency,sound_duration,silence_duration):
    # Set duty cycle to a positive value to emit sound from buzzer
    buzzerPinObject.duty_u16(int(65536*0.2))
    # Set frequency
    buzzerPinObject.freq(frequency)
    # wait for sound duration
    utime.sleep(sound_duration)
    # Set duty cycle to zero to stop sound
    buzzerPinObject.duty_u16(int(65536*0))
    # Wait for sound interrumption, if needed 
    utime.sleep(silence_duration)

def ton(f, d, s):
    buzzer(BuzzerObj, f, d, s)

# Alarm melody
def budicek():
    if (actbzucak == 1):
        ton(1046,0.38,0.1)  # c1
        ton(880,0.125,0.1)  # a
        ton(1046,0.38,0.1)  # c1
        ton(880,0.125,0.1)  # a
        ton(698,0.125,0.1)  # f
        ton(698,0.125,0.1)  # f
        ton(523,0.125,0.1)  # c
        ton(698,0.125,0.1)  # f
        ton(698,0.125,0.1)  # f
        ton(880,0.125,0.1)  # a
        ton(1046,0.38,0.1)  # c1
        ton(880,0.125,0.1)  # a
        ton(1046,0.38,0.1)  # c1
        ton(880,0.125,0.1)  # a
        ton(1046,0.125,0.2) # c1
        ton(1046,0.125,0.1) # c1
        ton(880,0.125,0.1)  # a
        ton(1046,0.125,0.1) # c1
        ton(1396,0.125,0.1) # f1
        ton(1046,0.75,0.1)  # c1

# Happy Birthday melody
def happy_birthday():
    ton(262, 0.25, 0.1) # C
    ton(262, 0.25, 0.1) # C
    ton(294, 0.5, 0.1) # D
    ton(262, 0.5, 0.1) # C
    ton(349, 0.5, 0.1) # F
    ton(330, 1, 0.1) # E

    ton(262, 0.25, 0.1) # C
    ton(262, 0.25, 0.1) # C
    ton(294, 0.5, 0.1) # D
    ton(262, 0.5, 0.1) # C
    ton(392, 0.5, 0.1) # G
    ton(349, 1, 0.1) # F

    ton(262, 0.25, 0.1) # C
    ton(262, 0.25, 0.1) # C
    ton(523, 0.5, 0.1) # +C
    ton(440, 0.5, 0.1) # A
    ton(349, 0.25, 0.1) # F
    ton(349, 0.25, 0.1) # F
    ton(330, 0.25, 0.1) # E
    ton(330, 0.25, 0.1) # E
    ton(294, 0.5, 0.2) # D

    ton(466, 0.25, 0.1) # A#
    ton(466, 0.25, 0.1) # A#
    ton(440, 0.5, 0.1) # A
    ton(349, 0.5, 0.1) # F
    ton(392, 0.5, 0.1) # G
    ton(349, 1, 0.1) # F
    

def clear_display():
    display.fill(0)
    display.show()

def display_col_bin(co, col):
    for x in range(0, 8):
        if (bt.get_bit(co, x) > 0):
            display.pixel(7 - x, col, 1)
        else:
            display.pixel(7 - x, col, 0)

def time_pure_Binary(cas1):
    display_col_bin(cas1[6],7) # seconds
    display_col_bin(cas1[5],6) # minutes
    display_col_bin(cas1[4],5) # hours
    display_col_bin(cas1[2],4) # day of month
    display_col_bin(cas1[1],3) # month
    display_col_bin(cas1[0] - 2000,2) # year (only in 21th century)
    display_col_bin(0,0)
    display_col_bin(cas1[3] + 1,0) # day of week (1 = Monday, 7 = Sunday)
    
def time_bcd(cas1):
    sekunda1 = cas1[6]
    secdes = int(sekunda1 / 10)
    secjed = sekunda1 - secdes * 10
    minuta1 = cas1[5]
    mindes = int(minuta1 / 10)
    minjed = minuta1 - mindes * 10
    hodina1 = cas1[4]
    hoddes = int(hodina1 / 10)
    hodjed = hodina1 - hoddes * 10
    display_col_bin(secjed, 7)
    display_col_bin(secdes, 6)
    display_col_bin(0, 5)
    display_col_bin(minjed, 4)
    display_col_bin(mindes, 3)
    display_col_bin(0, 2)
    display_col_bin(hodjed, 1)
    display_col_bin(hoddes, 0)
    
def scroll_ntext(jaky, kam=0, rychlost=0.2):
    text = jaky
    delka = len(text)
    znaky = []
    for k in range(0, delka):
        pismeno = text[(k):(k+1)]
        kod = ord(pismeno) - 32
        odkud = kod * 4
        for i in range(0, 4):
            znaky.append(zn.font[odkud + i])
    if (len(znaky)<=8):
        for i in range(0, len(znaky)):
            display_col_bin(znaky[i], i)
            display.show()
    else:
        if (kam == 0):
            for j in range(0, len(znaky) - 7):
                for i in range(j, j + 8):
                    display_col_bin(znaky[i], i - j)
                display.show()
                utime.sleep(rychlost)
        else:
            for j in reversed(range(8, len(znaky) + 1)):
                for i in range(j - 8, j):
                    display_col_bin(znaky[i], (i - j + 8))
                display.show()
                utime.sleep(rychlost)

def scroll_full_time(cas1):
    message = " " + dnyvtydnu[cas1[3]] + ", " + leadZero(cas1[2]) + "." + leadZero(cas1[1]) + "." + str(cas1[0]) + " " + leadZero(cas[4]) + ":" + leadZero(cas[5])
    print(message)
    scroll_ntext(message, 0, 0.2)
    utime.sleep(1)

def scroll_time(cas1):
    message = leadZero(cas[4]) + ":" + leadZero(cas[5])
    scroll_ntext(message, 0, 0.05)
    utime.sleep(1)
    scroll_ntext(message, 1, 0.05)
    utime.sleep(1)

def showPicotemp():
    utime.sleep(1)
    reading = TempSensor.read_u16() * conversion_factor
    t = 27 - (reading - 0.706)/0.001721
    message = " Pico temp: " + str(round(t, 1)) + "'C."
    print(message)
    scroll_ntext(message, 0, 0.2)
    
def showDHTtemp():
    utime.sleep(1)
    t = dhtsensor.temperature
    message = " DHT temp: " + str(round(t, 1)) + " 'C."
    print(message)
    scroll_ntext(message, 0, 0.2)

def showDHThum():
    utime.sleep(1)
    hum = dhtsensor.humidity
    message = " Humidity: " + str(round(hum, 1)) + " %."
    print(message)
    scroll_ntext(message, 0, 0.2)
    
def showBMPtemp():
    utime.sleep(1)
    t = bmp.temperature
    message = " BMP temp: " + str(round(t, 1)) + " 'C."
    print(message)
    scroll_ntext(message, 0, 0.2)
    
def showBMPpressure():
    utime.sleep(1)
    p = bmp.pressure / 100
    message = " Pressure: " + str(round(p, 0)) + " hPa."
    print(message)
    scroll_ntext(message, 0, 0.2)

def showBMPaltitude():
    utime.sleep(1)
    a = bmp.altitude
    message = " Altitude: " + str(round(a, 0)) + " m."
    print(message)
    scroll_ntext(message, 0, 0.2)

def decodeKeyValue(data1):
    return data1

def obsluha(kod, kaddr, ctrl):
    global actbzucak
    global nodisplay
    if kod < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        if (kod == 28): # RECALL key
            actbzucak = 1
            budicek()
        elif (kod == 9): # key "1"
            showPicotemp()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 29): # key "2"
            showDHTtemp()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 31): # key "3"
            showBMPtemp()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 13): # key "4"
            showDHThum()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 25): # key "5"
            showBMPpressure()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 27): # key = "6"
            showBMPaltitude()
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 17): # key = "7"
            scroll_time(rtc.datetime())
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 21): # key = "8"
            scroll_full_time(rtc.datetime())
            if (nodisplay == 1):
                clear_display() 
        elif (kod == 22): # key "Speaker Off"
            actbzucak = 0
        elif (kod == 23): # key "9"
            clear_display()
            utime.sleep(2)
            scroll_ntext("  Happy birthday!!!  ", 0, 0.1)
            scroll_ntext("14", 0, 0.15)
            happy_birthday()
            for poc in range(1, 9):
                clear_display()
                utime.sleep(0.25)
                scroll_ntext("14", 0, 0.15)
                utime.sleep(0.25)
            clear_display()
            utime.sleep(2)
        elif (kod == 18): # key = "0"
            if (nodisplay == 1):
                nodisplay = 0
            else:    
                clear_display()
                nodisplay = 1
                

        else:
            pass

# ir receiver settings
ir = nec.NEC_8(pin_ir, obsluha)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

try:
    while True:
        display.fill(0)
        utime.sleep(0.15)
        cas = rtc.datetime()
        hodina = cas[4] # hour
        minuta = cas[5] # minute
        sekunda = cas[6] # second
        if (minuta == budik[1] and hodina == budik[0]):
            scroll_time(cas)
            budicek()
            if (nodisplay == 1):
                clear_display() 
        else:
            if (minuta == 0):
                scroll_full_time(cas)
                if (nodisplay == 1):
                    clear_display()                 
            elif ((minuta > 0) and ((minuta % 15)==0)):
                scroll_time(cas)
                if (nodisplay == 1):
                    clear_display()                 
            elif ((minuta > 0) and ((minuta % 2) > 0)):
                time_pure_Binary(cas)
            elif (sekunda == 0):
                pass
            else:
                time_bcd(cas)
            if (nodisplay == 0):
                display.show()

except KeyboardInterrupt:
    ir.close()        
        





