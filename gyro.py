#!/usr/bin/python

import smbus
import math
import os
import time

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

dt = 0.01
acc_sensitivity = 16384.0

def comp_filter(x_dt, y_dt, accel_out, gyroData):

    x_dt += gyroData[0] * dt
    y_dt += gyroData[1] * dt

    accel_xout_scaled = accel_out[0] / acc_sensitivity
    accel_yout_scaled = accel_out[1] / acc_sensitivity
    accel_zout_scaled = accel_out[2] / acc_sensitivity

    acc_angle_x =  get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    acc_angle_y =  get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    x_dt = x_dt * 0.6 + acc_angle_x * 0.4
    y_dt = y_dt * 0.6 + acc_angle_y * 0.4

    return [x_dt, y_dt]



def calibrate(samples):
        values = []
        xval = 0
        yval = 0
        val = [0,0]
        accel_out = [0,0,0]
        
        input("press any key to start calibration")
        
        for i in range(0,samples):
            accel_out[0] = read_word_2c(0x3b)
            accel_out[1] = read_word_2c(0x3d)
            accel_out[2] = read_word_2c(0x3f)

            accel_xout_scaled = accel_out[0] / acc_sensitivity
            accel_yout_scaled = accel_out[1] / acc_sensitivity
            accel_zout_scaled = accel_out[2] / acc_sensitivity

            val[0] =  get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            val[1] =  get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

            values.append(val)
            xval = xval + val[0]
            yval = yval + val[1]

        avg = [xval/samples, yval/samples]

        return avg