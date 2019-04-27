#!/usr/bin/env python

import sys, os, re
import serial
import struct
import time

if os.name == 'nt':
    from list_ports_windows import *
elif os.name == 'posix':
    from list_ports_posix import *
else:
    raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))

def getports():
    ports = []
    iterator = sorted(comports())
    for port, desc, hwid in iterator:
        # print("%-20s" % (port,))
        ports = ports + [port]
    return ports

def checksum(listsum):
    sum = 0
    for i in range(len(listsum)):
        sum ^= listsum[i]
    return sum

def check_sum(listsum):
    if not listsum:
        print "check_sum err: list is NULL"
        return

    sum = checksum(listsum[:(len(listsum)-1)])

    if listsum[len(listsum)-1] == sum:
        return True

    return False


class MySerial(object):
    def __init__(self, port, baudrate, timeout):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=timeout)
        except serial.SerialException:
            print "Can not open %s" % port
            return None

    def read(self):
        "get data from serial"

        r1 = [0, 0]
        for i in range(2):
            buf = self.serial.read(size=1)
            if not buf:
                return -1
            x, = struct.unpack('B', buf)
            r1[i] = x

        if r1[0] != 0x3c:
            print "first character is not 0x3c, is 0x%x" % r1[0]
            return -2

        r2 = []
        for i in range(r1[1]+1):
            buf = self.serial.read(size=1)
            if not buf:
                return -3
            x, = struct.unpack('B', buf)
            r2 = r2 + [x]

        return r1 + r2

    def write(self, sendlist):
        for i in sendlist:
            buf = struct.pack('B', i)
            self.serial.write(buf)
            time.sleep(0.01)
        self.serial.flush()
        time.sleep(0.1)

    def close(self):
        self.serial.close()

if __name__ == '__main__':
    print os.name
    print getports()
    list = [0x3b,0x4,0x5,0x34,0x1,0x0,0xf]
    print check_sum(list)
    # ser = MySerial("/dev/ttyUSB0", 115200, 1)
    # ser = MySerial("COM6", 115200, 1)
    # ser.write(list)
    # print check_sum(ser.read())
    # ser.close()
