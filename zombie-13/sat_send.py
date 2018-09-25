from machine import UART
from machine import Pin
import ssd1306
from machine import I2C
import time


i2c = I2C(-1, Pin(14), Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()


oled.fill(0)
oled.text("Starting up ...",0,0)
oled.show()


rx=34
tx=13

uart=UART(2,baudrate=19200,bits=8, parity=None, stop=1,rx=rx,tx=tx)

filename='data3'

while True:

    oled.fill(0)
    oled.text("Connecting ...",0,0)
    oled.show()
    time.sleep(.2)
    
    uart.write('AT\r')
    print("--> AT")
    #oled.fill(0)
    oled.text("--> AT",0,20)
    oled.show()
    time.sleep(.2)
            
    a=uart.readline()
    if a!=None:
        p = str(a, 'ascii').strip()
        print("<-- "+p)
        #oled.fill(0)
        oled.text("<-- "+p,0,30)
        oled.show()
        time.sleep(.2)
    
    a=uart.readline()
    if a!=None:
        p = str(a, 'ascii').strip()
        print("<-- "+p)
        #oled.fill(0)
        oled.text("<-- "+p,0,40)
        oled.show()
        time.sleep(.2)
        
        
    oled.fill(0)
    
    send_str='AT'
    uart.write(send_str+'\r')
    print("--> "+send_str)
    oled.text('--> '+send_str,0,20)
    oled.show()
    time.sleep(.2)
            
    a=uart.readline()
    if a!=None:
        p = str(a, 'ascii').strip()
        print("<-- "+p)
        #oled.fill(0)
        oled.text("<-- "+p,0,30)
        oled.show()
        time.sleep(.2)
    
    a=uart.readline()
    if a!=None:
        p = str(a, 'ascii').strip()
        print("<-- "+p)
        #oled.fill(0)
        oled.text("<-- "+p,0,40)
        oled.show()
        time.sleep(.2)
        
        

    time.sleep(2)
