
import uasyncio as asyncio
import picoweb
import network
import time
import gc

import aswitch

from machine import UART

from machine import Pin
from machine import SPI

from upy_rfm9x import RFM9x

TIMEOUT = .01
DISPLAY=False

sck=Pin(25)
mosi=Pin(33)
miso=Pin(32)
cs = Pin(26, Pin.OUT)

resetNum=27

spi=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)
rfm9x = RFM9x(spi, cs, resetNum, 915.0)


class MASTER():
    def __init__(self, uart_no = 2, timeout=4000,rx=35,tx=21):
        self.uart = UART(2,baudrate=9600,rx=rx,tx=tx)
        self.timeout = timeout
        self.loop = asyncio.get_event_loop()
        self.swriter = asyncio.StreamWriter(self.uart, {})
        self.sreader = asyncio.StreamReader(self.uart)
        self.delay = aswitch.Delay_ms()
        self.response = []

    async def _recv(self):
        while True:
            gc.collect()
            a = await self.sreader.readline()
            if a!=None:
                try:
                    p = str(a, 'ascii')
                    q=p.split(',')
                    #print(q)
                    if len(q)==13 and str(q[0])=='$GPRMC':
                        print("--------------")
                        time.sleep(1)
                        #oled.fill(0)
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
                            
                            push_phrase=lat_oled+" "+lon_oled
                            await push_event(push_phrase)
                            
                            #oled.text(lat_oled,0,30)
                            #oled.text(lon_oled,0,40)
                            #oled.show()    
                            
                        else:
                            await push_event("no signal")
                            #oled.fill(0)
                            #oled.text("no sat sig",0,30)
                            #oled.text("try attempt #"+counter,0,40)
                            #oled.show()
                            counter=counter+1    
                except Exception as e:
                    print(str(e))




app = picoweb.WebApp(__name__)





ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(1)
#ap.config(essid='uPY_12n', authmode=network.AUTH_WPA_WPA2_PSK, password="uPy1234")
ap.config(essid='tardigrade',  password="tardigrade")
ap.active(True)
#while accesspoint.isconnected() == False:
#    pass
#    
ip=ap.ifconfig()

event_sinks = set()

#
# Webapp part
#
f=open('e.html')
html=f.read()
f.close()

@app.route('/_add_numbers')
def add_numbers():
    print("hallo")
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/receivedata', methods=['POST'])
def receive_data():
    print(request.form['myData'])

@app.route("/byzanga",methods=['POST'])
def byzanga():
    if request.method == 'POST':
        print("hello")
        return "sure"
    print("bobby")
    return("jane")
    
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(html)
    

@app.route("/events")
def events(req, resp):
    global event_sinks
    print("Event source %r connected" % resp)
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/event-stream\r\n")
    yield from resp.awrite("\r\n")
    event_sinks.add(resp)
    return False

def update_display(display_text):
    oled.fill(0)
    oled.text(ip[0], 0, 20)
    oled.text(':8081',0,30)
    oled.text(display_text,0,40)
    oled.show()


def push_event(ev):
    global event_sinks
    to_del = set()

    for resp in event_sinks:
        try:
            await resp.awrite("data: %s\n\n" % ev)
        except OSError as e:
            print("Event source %r disconnected (%r)" % (resp, e))
            await resp.aclose()
            # Can't remove item from set while iterating, have to have
            # second pass for that (not very efficient).
            to_del.add(resp)

    for resp in to_del:
        event_sinks.remove(resp)


def radio_listen():
    while True:
        gc.collect()
        rfm9x.receive(timeout=TIMEOUT)
        if rfm9x.packet is not None:
            try:
                packet_text = str(rfm9x.packet, 'ascii')
                rssi=str(rfm9x.rssi)
                print('Received: {0}'.format(packet_text))
                print("RSSI:",rssi)
                await push_event("- %s" % packet_text)
            except Exception as e:
                print(str(e))
        await asyncio.sleep(.09)


rx=35
tx=21
master = MASTER()

loop = asyncio.get_event_loop()
#loop.create_task(push_count())
loop.create_task(master._recv())
loop.create_task(radio_listen())


#app = picoweb.WebApp(__name__, ROUTES)
#app = picoweb.WebApp(None, ROUTES)

# debug values:
# -1 disable all logging
# 0 (False) normal logging: requests and errors
# 1 (True) debug logging
# 2 extra debug logging
print("host:"+ip[0])


# note: you'll need to visit ipaddress:8081
app.run(debug=-1,host=ip[0])

