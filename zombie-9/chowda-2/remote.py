import board
import busio
import digitalio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)
import adafruit_rfm9x
r = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

def send(message):
    r.send(message)
    
def receive(timeout):
    result=r.receive(timeout=timeout)
    return result
