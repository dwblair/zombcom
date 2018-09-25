import sdcard, os
from machine import Pin
from machine import SPI

#from upy_rfm9x import RFM9x

import time

DISPLAY = True

if DISPLAY:
    import ssd1306
    from machine import I2C
    i2c = I2C(-1, Pin(14), Pin(2))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()

def update_display(display_text):
    oled.fill(0)
    #oled.text(ip[0], 0, 0)
    #oled.text(':8081',0,10)
    oled.text(display_text,0,20)
    oled.show()
    
sck=Pin(16)
mosi=Pin(4)
miso=Pin(17)
cs = Pin(15, Pin.OUT)
spi2=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)

sd = sdcard.SDCard(spi2, cs)
os.mount(sd,'/sd')
output=os.listdir('/sd')
print(output)

update_display(output[0])

