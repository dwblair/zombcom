# auart_hd.py
# Author: Peter Hinch
# Copyright Peter Hinch 2018 Released under the MIT license

# Demo of running a half-duplex protocol to a device. The device never sends
# unsolicited messages. An example is a communications device which responds
# to AT commands.
# The master sends a message to the device, which may respond with one or more
# lines of data. The master assumes that the device has sent all its data when
# a timeout has elapsed.

# In this test a physical device is emulated by the DEVICE class
# To test link X1-X4 and X2-X3

#https://github.com/MakerSnake/pyRockBlock/blob/master/rockBlock.py

from machine import UART
import uasyncio as asyncio
import aswitch
import random

# Dummy device waits for any incoming line and responds with 4 lines at 1 second
# intervals.

# The master's send_command() method sends a command and waits for a number of
# lines from the device. The end of the process is signified by a timeout, when
# a list of lines is returned. This allows line-by-line processing.
# A special test mode demonstrates the behaviour with a non-responding device. If
# None is passed, no commend is sent. The master waits for a response which never
# arrives and returns an empty list.
class MASTER():
    def __init__(self, uart_no = 2, timeout=2000,rx=34,tx=13):
        self.uart = UART(1,baudrate=19200,rx=rx,tx=tx)
        self.timeout = timeout
        self.loop = asyncio.get_event_loop()
        self.swriter = asyncio.StreamWriter(self.uart, {})
        self.sreader = asyncio.StreamReader(self.uart)
        self.delay = aswitch.Delay_ms()
        self.response = []
        loop = asyncio.get_event_loop()
        loop.create_task(self._recv())

    async def _recv(self):
        while True:
            res = await self.sreader.readline()
            self.response.append(res)  # Append to list of lines
            self.delay.trigger(self.timeout)  # Got something, retrigger timer

    async def send_command(self, command):
        self.response = []  # Discard any pending messages
        if command is None:
            print('Timeout test.')
        else:
            await self.swriter.awrite("{}\r\n".format(command))
            #print('Command sent:', command)
        self.delay.trigger(self.timeout)  # Re-initialise timer
        while self.delay.running():
            await asyncio.sleep(1)  # Wait for 4s after last msg received
        return self.response

async def send_irid(cmd):
    print("Sending:\n"+cmd)
    res = await master.send_command(cmd)
    if res:
        print('Result is:')
        for line in res:
            print(line.decode('UTF8'), end='')
        print("----\n")
    else:
        print('Timed out waiting for result.')

async def test():
    print('This test takes 10s to complete.')
    while True:

        cmd='AT'
        
        print("Sending:\n"+cmd)
        res = await master.send_command(cmd)
        if res:
            print('Result is:')
            for line in res:
                print(line.decode('UTF8'), end='')
            print("----\n")
        else:
            print('Timed out waiting for result.')
            
    
        cmd='AT+CSQ'
        
        print("Sending:\n"+cmd)
        res = await master.send_command(cmd)
        if res:
            print('Result is:')
            for line in res:
                print(line.decode('UTF8'), end='')
            print("----\n")
        else:
            print('Timed out waiting for result.')


loop = asyncio.get_event_loop()
#master = MASTER(uart_no=2,timeout=4000,rx=12,tx=13)
#device = DEVICE(uart_no=4,rx=16,tx=17)

rx=34
tx=13
master = MASTER(uart_no=2,timeout=4000,rx=rx,tx=rx)
#master = MASTER(uart_no=2,timeout=4000,rx=22,tx=34)
#device = DEVICE(uart_no=4,rx=32,tx=35)
loop.run_until_complete(test())
#loop.create_task(test())

# Expected output
# >>> import auart_hd
# This test takes 10s to complete.
#
# Command sent: Run
# Result is:
# Line 1
# Line 2
# Line 3
# Goodbye
#
# Timeout test.
# Timed out waiting for result.
# >>> 
