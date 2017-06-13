#!/usr/bin/python

import smbus
import math
import time
import os

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

bus.write_byte_data(address, 0x1B, 0x08) # set new range

gyro_x_all = 0
for i in range(0, 2000):
    gyro_xout = read_word_2c(0x43)
    gyro_x_all += gyro_xout

gyro_x_calibration = gyro_x_all / 2000
x = 0

current_time = time.time()
last_time = current_time

while 1:

    print "gyro data"
    print "---------"

    gyro_xout = read_word_2c(0x43) - gyro_x_calibration
    scaled = gyro_xout / 65.5
    print "gyro_xout: ", gyro_xout, " scaled: ", scaled

    
    current_time = time.time()
    
    delta = current_time - last_time
    x += (scaled * delta)
    print("angle: ", x)

    last_time = current_time

    # print
    # print "accelerometer data"
    # print "------------------"

    # accel_xout = read_word_2c(0x3b)
    # accel_yout = read_word_2c(0x3d)
    # accel_zout = read_word_2c(0x3f)

    # accel_xout_scaled = accel_xout / 16384.0
    # accel_yout_scaled = accel_yout / 16384.0
    # accel_zout_scaled = accel_zout / 16384.0

    # print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    # print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    # print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

    # print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    # print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    os.system('clear')
