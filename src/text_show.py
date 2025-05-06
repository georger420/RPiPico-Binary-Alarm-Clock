# georger420
#

import machine
import max7219
import utime
import bitops as bt
import nznaky2 as zn

# MAX7219 control
spi = machine.SPI(0,sck=machine.Pin(2),mosi=machine.Pin(3))
cs = machine.Pin(5, machine.Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(1)
display.fill(0)
display.show()

def display_col_bin(co, col):
    for x in range(0, 8):
        if (bt.get_bit(co, x) > 0):
            display.pixel(7 - x, col, 1)
        else:
            display.pixel(7 - x, col, 0)
            
def show_character(co):
    kod = ord(co) - 32
    zacatek = kod * 4
    znak = []
    for i in range(0, 4):
        znak.append(zn.font[zacatek + i])
    # print(co, " - ", kod)
    # print(znak)
    for i in range(0, 4):
        display_col_bin(znak[i], i)
    display.show()
    
def show_2_chars(zceho):
    if len(zceho) > 2:
        text = zceho[:2]
    elif len(zceho) == 2:
        text = zceho
    elif len(zceho) == 1:
        text = zceho + " "
    else: text = ".."

    leve = text[:1]
    print(leve)
    prave = text[1:]
    print(prave)
    kl = ord(leve) - 32
    kp = ord(prave) - 32
    lodkud = kl * 4
    podkud = kp * 4
    znak = []
    for i in range(0, 4):
        znak.append(zn.font[lodkud + i])
    for i in range (4, 8):
        znak.append(zn.font[podkud + i - 4])
    delka = len(znak)
    print("delka: {}".format(delka))
    for i in range(0, delka):
        display_col_bin(znak[i], i)
    display.show()
        
def scroll_ntext(jaky, kam=0, rychlost=0):
    text = jaky
    delka = len(text)
    znaky = []
    for k in range(0, delka):
        pismeno = text[(k):(k+1)]
        kod = ord(pismeno) - 32
        odkud = kod * 4
        for i in range(0, 4):
            znaky.append(zn.font[odkud + i])
    print(len(znaky))
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
                
                print("j:", j)
                print("\n")
                for i in range(j - 8, j):
                    # n = 8 - i
                    print("i - j:", j - i - 1)
                    # display_col_bin(znaky[i], 7 - (j - i - 1))
                    display_col_bin(znaky[i], (i - j + 8))
                    #pass
                display.show()
                utime.sleep(rychlost)
while True:
    scroll_ntext("20:03", 0, 0.05)
    utime.sleep(1)
    scroll_ntext("20:03", 5, 0.05)
    utime.sleep(1)
    utime.sleep(1)
    scroll_ntext("T: 22.5'C", 0, 0.2)
    utime.sleep(2)
    scroll_ntext("Hello world!", 0, 0.2)
    utime.sleep(2)
    

