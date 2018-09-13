import network
import picoweb
import uasyncio
import network
import time
import gc

from machine import Pin
from machine import SPI

from upy_rfm9x import RFM9x

TIMEOUT = .01
DISPLAY = True

if DISPLAY:
    import ssd1306
    from machine import I2C
    i2c = I2C(-1, Pin(14), Pin(13))
    oled = ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    oled.show()

if DISPLAY:
    oled.fill(0)
    oled.text("Starting up ...",0,0)
    oled.show()

sck=Pin(25)
mosi=Pin(33)
miso=Pin(32)
cs = Pin(26, Pin.OUT)
#reset=Pin(13)
led = Pin(13,Pin.OUT)

resetNum=27

spi=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)



rfm9x = RFM9x(spi, cs, resetNum, 915.0)

ssid = "zombie"
password =  "disaster"
 
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

ip = station.ifconfig()

event_sinks = set()

f=open('e.html')
html=f.read()
f.close()

#app = picoweb.WebApp(__name__)
app = picoweb.WebApp(None)


def update_display(display_text):
    oled.fill(0)
    oled.text(ip[0], 0, 0)
    oled.text(':8081',0,10)
    oled.text(display_text,0,20)
    oled.show()
    

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

@app.route('/parse_data', methods=['GET', 'POST'])
def goofy(request, response):
    print("wheee")
    if request.method == 'POST':
        print(request.headers)
        yield from request.read_form_data()
        if request.form.get('test'):
            print("hello")
            content=request.form['test'][0]
            rfm9x.send(str(content))
            print("Sending:",content)
            await push_event("- %s" % str(content))
            yield from picoweb.start_response(response, "application/json")
            yield from response.awriteiter(ijson.idumps({'note': 'huzzah', 'success': 1}))
            return

        yield from picoweb.jsonify(response, {'success': 0})
        return

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


def push_count():
    i = 0
    while True:
        rfm9x.receive(timeout=TIMEOUT)
        if rfm9x.packet is not None:
            try:
                packet_text = str(rfm9x.packet, 'ascii')
                rssi=str(rfm9x.rssi)
                print('Received: {0}'.format(packet_text))
                print("RSSI:",rssi)
                if DISPLAY:
                    display_text="%s" % packet_text
                    update_display(display_text)
                #await push_event("[#%s RSSI:%s]:  %s" % (i, rssi, packet_text))
                await push_event("- %s" % packet_text)
                i += 1
            except:
                print("some error?")
                if DISPLAY:
                    display_text="[%s]: (garbled msg)" % i
                    update_display(display_text)
        #blink(.1)
        gc.collect()
        await uasyncio.sleep(.09)


loop = uasyncio.get_event_loop()
loop.create_task(push_count())

print("host:"+ip[0])

if DISPLAY:
    oled.fill(0)
    oled.text("IP ADDRESS:",0,0)
    oled.text(ip[0], 0, 10)
    oled.text(':8081',0,20)
    #oled.text(display_text,0,20)
    oled.show()
    
app.run(debug=-1,host=ip[0])
#print(ip[0])
