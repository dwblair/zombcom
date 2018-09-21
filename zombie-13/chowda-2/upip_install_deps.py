import os, network, time
from config import wifi #local settings


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(wifi.ssid, wifi.password)

while station.isconnected() == False:
    print("Waiting for WiFi connection (ssid='{}',password='{}')...".format(wifi.ssid, wifi.password))
    time.sleep(2.0)

if not 'lib' in os.listdir('/'):
    os.mkdir('/lib')

import upip

try:
    upip.install('picoweb')
    import picoweb
    #so we are done now we delete ourselves
    os.remove('/upip_install_deps.py')
    print("SUCCESS!")
except ImportError:
    print("WARNING: 'picoweb' package failed to install, check Internet connection!")
