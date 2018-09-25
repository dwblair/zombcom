

import time
import gc

from machine import Pin
from machine import SPI

from upy_rfm9x import RFM9x


from machine import I2C


datafile='water.txt'

TIMEOUT = .1
DISPLAY=True


if DISPLAY==True:
    i2c = I2C(-1, Pin(14), Pin(2))
    import ssd1306
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

sck=Pin(25)
mosi=Pin(33)
miso=Pin(32)
cs = Pin(26, Pin.OUT)

resetNum=27

spi=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)
rfm9x = RFM9x(spi, cs, resetNum, 915.0)


def update_display(display_text):
    oled.fill(0)
    #oled.text(ip[0], 0, 20)
    #oled.text(':8081',0,30)
    oled.text(display_text,0,30)
    oled.show()


def radio_listen():
    counter=0
    while True:
        gc.collect()
        rfm9x.receive(timeout=TIMEOUT)
        if rfm9x.packet is not None:
            try:
                packet_text = str(rfm9x.packet, 'ascii')
                rssi=str(rfm9x.rssi)
                print('Received: {0}'.format(packet_text))
                print("RSSI:",rssi)
                print("Counter:",counter)
                counter=counter+1

                #await push_event("- %s" % packet_text)
                vals=packet_text.split("=")
                depth=vals[1]
                if DISPLAY==True:
                    oled.fill(0)
                    output="depth="+vals[1]
                    oled.text(output,0,30)
                    output="count="+str(counter)
                    oled.text(output,0,40)
                    oled.show()
                f=open(datafile,'a')
                f.write(depth+'\n')
                f.close()
            except Exception as e:
                print(str(e))
        time.sleep(0.9)

radio_listen()

