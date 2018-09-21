from machine import UART
import time
import ssd1306
from machine import I2C
from machine import Pin

i2c = I2C(-1, Pin(14), Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()


oled.fill(0)
oled.text("Starting up ...",0,0)
oled.show()


