import network
import picoweb
import uasyncio as asyncio
import network
import time
import gc

from machine import Pin
from machine import SPI

from upy_rfm9x import RFM9x

import config #local settings
from config import radio as RS
################################################################################
TIMEOUT = .01

################################################################################
# Hardware Configuration

# OLED display
if config.use_oled_display:
    import ssd1306
    from machine import I2C
    i2c = I2C(-1, Pin(14), Pin(13))
    oled = ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    oled.text("Starting up ...",0,0)
    oled.show()
    
def update_display(display_text):
    if config.use_oled_display:
        oled.fill(0)
        oled.text(ip[0], 0, 0)
        oled.text(':8081',0,10)
        oled.text(display_text,0,20)
        oled.show()

#LoRa radio device
spi = SPI(RS.spi_id,
          baudrate=RS.baudrate,
          sck=RS.sck,
          mosi=RS.mosi,
          miso=RS.miso)
rfm9x = RFM9x(spi, RS.cs, RS.resetNum, frequency=RS.freq)

#WiFi network connection
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(config.wifi.ssid, config.wifi.password)

while station.isconnected() == False:
    pass

ip_adrr, _, _, _ = station.ifconfig()

################################################################################
# Web App (picoweb)

#app = picoweb.WebApp(__name__)
app = picoweb.WebApp(None)
event_sinks = set()

#load the HTML template
f = open('e.html')
html = f.read()
f.close()

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

async def push_event(ev):
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


async def push_count():
    i = 0
    while True:
        rfm9x.receive(timeout=TIMEOUT)
        if rfm9x.packet is not None:
            try:
                packet_text = str(rfm9x.packet, 'ascii')
                rssi=str(rfm9x.rssi)
                print('Received: {}'.format(packet_text))
                print("RSSI: {}".format(rssi))
                display_text = packet_text
                update_display(display_text)
                await push_event("- {}".format(packet_text))
                i += 1
            except:
                print("some error?")
                display_text = "[{}]: (garbled msg)".format(i)
                update_display(display_text)
        gc.collect()
        await asyncio.sleep(.09)


loop = asyncio.get_event_loop()
loop.create_task(push_count())

print("host: {}".format(ip_adrr))
update_display("")   #will show just IP address
    
app.run(debug=-1,host=ip_adrr)
