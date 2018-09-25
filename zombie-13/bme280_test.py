
from machine import I2C
from machine import Pin

DISPLAY=True


i2c = I2C(-1, Pin(14), Pin(2))


if DISPLAY==True:
    import ssd1306
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()


import bme280

bme = bme280.BME280(i2c=i2c)
#a=bme.read_compensated_data()

b=bme.values

if DISPLAY==True:
    oled.fill(0)
    oled.text(str(b[0]),0,30)
    oled.text(str(b[1]),0,40)
    oled.text(str(b[2]),0,50)
    oled.show()

print(b)
