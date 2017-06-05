#!/usr/bin/python

import smbus
import math
import os
import time

class gyro:

    def __init__(self, dt):
        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        self.dt = dt
        self.acc_sensitivity = 16384.0
        self.gyro_sensitivity = 131

        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def comp_filter(self, x_dt, y_dt, accAngles, gyroData):

        x_dt += gyroData[0] * self.dt
        y_dt += gyroData[1] * self.dt

        x_dt = x_dt * 0.6 + accAngles[0] * 0.4
        y_dt = y_dt * 0.6 + accAngles[1] * 0.4

        return [x_dt, y_dt]

    def getAccelerometerAngles(self):
        accel_out = [0,0,0]
        accel_out[0] = self.read_word_2c(0x3b)
        accel_out[1] = self.read_word_2c(0x3d)
        accel_out[2] = self.read_word_2c(0x3f)
        
        accel_xout_scaled = accel_out[0] / self.acc_sensitivity
        accel_yout_scaled = accel_out[1] / self.acc_sensitivity
        accel_zout_scaled = accel_out[2] / self.acc_sensitivity

        acc_angle_x =  self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        acc_angle_y =  self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

        return [acc_angle_x, acc_angle_y]

    def getGyroData(self):
        gyro_xout = self.read_word_2c(0x43)
        gyro_yout = self.read_word_2c(0x45)
        gyro_zout = self.read_word_2c(0x47)

        gyroData = [0,0,0]
        gyroData[0] = gyro_xout / self.gyro_sensitivity
        gyroData[1] = gyro_yout / self.gyro_sensitivity
        gyroData[2] = gyro_zout / self.gyro_sensitivity

        return gyroData

    def calibrate(self, samples):
            values = []
            xval = 0
            yval = 0
            val = [0,0]
            accel_out = [0,0,0]
            xy_dt = [0,0]

            input("press any key to start calibration")
            
            for i in range(0,samples):
                
                gyroData = self.getGyroData()        
                accAngles = self.getAccelerometerAngles()

                val = self.comp_filter(val[0], val[1], accAngles, gyroData)

                values.append(val)
                xval = xval + val[0]
                yval = yval + val[1]

            avg = [xval/samples, yval/samples]

            return avg