from machine import UART
import time
import ssd1306
from machine import I2C
from machine import Pin

#i2c = I2C(-1, Pin(14), Pin(2))
#oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#oled.fill(0)
#oled.show()


#oled.fill(0)
#oled.text("Starting up ...",0,0)
#oled.show()



#rx=34
#tx=13

rx=21
tx=19

uart=UART(2,baudrate=9600,rx=rx,tx=tx)

index = 1

while True:
    try:
        a=uart.readline().strip()
        packet_text = str(a, 'ascii')
        print('Received: {0}'.format(packet_text))
        oled.fill(0)
        oled.text(str(index),0,0)
        oled.text(packet_text,0,20)
        oled.show()
        index=index+1
    except:
        print("Some error?")
    time.sleep(1)
