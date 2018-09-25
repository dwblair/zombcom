
from machine import I2C
from machine import Pin

i2c = I2C(-1, Pin(14), Pin(2))

import bme280

bme = bme280.BME280(i2c=i2c)
a=bme.read_compensated_data()

b=bme.values

print(a)
print(b)
