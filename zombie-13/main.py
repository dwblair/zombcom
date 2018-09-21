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


rx=35
tx=21

uart=UART(2,baudrate=9600,bits=8, parity=None, stop=1,rx=rx,tx=tx)

filename='data3'

oled.fill(0)
oled.text("Connecting ...",0,0)
oled.show()
time.sleep(1)

counter=0

while True:
    a=uart.readline()
    if a!=None:
        try:
            p = str(a, 'ascii')
            q=p.split(',')
            #print(q[0])
            if len(q)==13 and str(q[0])=='$GPRMC':
                print("--------------")
                time.sleep(1)
                oled.fill(0)
                active=str(q[2])
                #print("active=",active)
                if(active=="A"):
                    counter=0
                    lat_str=str(q[3])
                    lat_a=int(lat_str[:2])
                    lat_b=float(lat_str[2:])
                    
                    lat_out=str(lat_a)+" "+str(lat_b)
                    lat_oled="lat: "+lat_out
                    print(lat_oled)
                    

                    lon_str=str(q[5])
                    lon_a=-1*int(lon_str[:3])
                    lon_b=float(lon_str[3:])
                    
                    lon_out=str(lon_a)+" "+str(lon_b)
                    lon_oled="lon: "+lon_out
                    print(lon_oled)
                    
                    oled.text(lat_oled,0,30)
                    oled.text(lon_oled,0,40)
                    oled.show()    
                    
                else:
                    oled.fill(0)
                    oled.text("no sat sig",0,30)
                    #oled.text("try attempt #"+counter,0,40)
                    oled.show()
                    counter=counter+1    
        except Exception as e:
            oled.text("ERROR",0,30)
            oled.show()    
            print(str(e))
            #print("len(q)",len(q))
