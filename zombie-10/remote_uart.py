import board,busio,digitalio,time

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT
 
uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
    data = uart.readline()
    print(data)
    time.sleep(.2)
