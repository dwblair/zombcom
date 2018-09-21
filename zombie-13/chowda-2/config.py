from machine import Pin

led = Pin(13,Pin.OUT)

use_oled_display = False

class radio:
    spi_id = 2
    baudrate = 5000000
    sck  = Pin(25)
    mosi = Pin(33)
    miso = Pin(32)
    cs   = Pin(26, Pin.OUT)
    resetNum = 27
    freq = 915.0

class wifi:
    ssid     = "zombie"
    password = "disaster"
