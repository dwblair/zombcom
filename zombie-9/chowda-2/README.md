# setting up the esp32

## put relevant files on esp32:

```
ampy -p /dev/ttyUSB0 put e.html
ampy -p /dev/ttyUSB0 put zom9.html
ampy -p /dev/ttyUSB0 put static
```

## connect to esp32

```
screen /dev/ttyUSB0 115200
```

## run web server on esp32:

```
>>> import zom9
```

# running feather m0 lora with circuitpython

## install the base firmware

Follow instructions [here](https://learn.adafruit.com/welcome-to-circuitpython/non-uf2-installation)

The particular .bin file you'll use is [here](https://github.com/adafruit/circuitpython/releases/download/3.0.1/adafruit-circuitpython-feather_m0_rfm9x-3.0.1.bin)

To install BOSSA on Ubuntu, download the github repo [here](https://github.com/shumatech/BOSSA)

... but I found the instructions for installing it more explicit and easier to follow, [here](https://github.com/marklef2/armdude).

Basically, in Ubuntu you need these prequisites:

```
sudo apt-get install build-essentials
sudo apt-get install build-essential 
sudo apt-get install libreadline-dev
sudo apt-get install wx3.0-headers 
sudo apt-get install libwxgtk3.0-0v5
sudo apt-get install libwxgtk3.0-dev 
```

and then run 'make' at the proper level of the github repo you downloaded.

## installing lora support 

After installing the firmware on the M0 as above, you'll still need to install adafruit bus device, and the rfm9x libraries.

You can follow the instructions [here](https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm9x-lora)

- The rfm9x module (get 3.0 version for compatibility with 3.0 firmware installed in previous step) is [here](https://github.com/adafruit/Adafruit_CircuitPython_RFM9x/releases)

- the adafruit bus device module is [here](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice/releases).

for each, install on the M0 via ampy

## adding a convenience script for send / receive

use ampy to install 'remote.py' from this github repo

# Known issues

The ESP32 can receive messages and replace the relevant 'div' element on the page, nicely.

But when the ESP32 is sending, the picweb app seems to 'refresh' the web page, losing previous content.

This might be fixed via some tricks with flask; a more robust, longer-term solution would be to store messages (received / sent) in a local database, and display them.

A potential model for doing this is [here](https://github.com/pfalcon/notes-pico).


