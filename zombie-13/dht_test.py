import time
import machine
import onewire, ds18x20

# the device is on GPIO12
dat = machine.Pin(5)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

while True:
# scan for devices on the bus
    roms = ds.scan()
    print('found devices:', roms)
    time.sleep(1)
