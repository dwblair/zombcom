import time
import gc
from machine import I2C
from machine import Pin
from machine import SPI

from upy_rfm9x import RFM9x

DISPLAY=True

TIMEOUT = .1

datafile='press_compare.txt'

i2c = I2C(-1, Pin(14), Pin(2))


if DISPLAY==True:
    import ssd1306
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()

sck=Pin(25)
mosi=Pin(33)
miso=Pin(32)
cs = Pin(26, Pin.OUT)

resetNum=27

spi=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)
rfm9x = RFM9x(spi, cs, resetNum, 915.0)


import bme280

bme = bme280.BME280(i2c=i2c)
#a=bme.read_compensated_data()


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
                water_press=vals[1]
                
                b=bme.values
                amb_temp=b[0]
                amb_press=b[1]
                amb_humid=b[2]
                
                if DISPLAY==True:
                    oled.fill(0)
                    
                    output="count="+str(counter)
                    oled.text(output,0,0)
                    
                    output="wp="+water_press
                    oled.text(output,0,20)
                    
                    output="ap="+amb_press
                    oled.text(output,0,30)
                    
                    output="at="+amb_temp
                    oled.text(output,0,40)
                    
                    output="ah="+amb_humid
                    oled.text(output,0,50)
                    
                    oled.show()
                f=open(datafile,'a')
                f.write(str(counter)+" "+water_press+" "+amb_press+" "+amb_temp+" "+amb_humid+'\n')
                f.close()
            except Exception as e:
                print(str(e))
        time.sleep(1)
        
radio_listen()
