#!/usr/bin/python

import smbus
import math
import os
import time

class gyro:

    def __init__(self, calibration_samples = 1000):
        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        
        self.acc_sensitivity = 8192.0
        self.gyro_sensitivity = 65.5

        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

        GYRO_CONFIG_REGISTER = 0x1B
        GYRO_500DEG = 0x08
        self.bus.write_byte_data(self.address, GYRO_CONFIG_REGISTER, GYRO_500DEG)
        
        ACCEL_CONFIG_REGISTER = 0x1C
        ACCEL_4G = 0x08

        self.bus.write_byte_data(self.address, ACCEL_CONFIG_REGISTER, ACCEL_4G)

        sumAcc = [0,0]
        dataAcc = [0,0]

        self.acc_start_x = 0
        self.acc_start_y = 0

        for i in range(0, calibration_samples):
            dataAcc = self.getAccData()
            sumAcc[0] += dataAcc[0]

        self.acc_start_x = sumAcc[0] / calibration_samples

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

    def getGyroData(self):
        gyro_xout = self.read_word_2c(0x43)
        
        gyroData = [0,0,0]
        gyroData[0] = gyro_xout / self.gyro_sensitivity
        return gyroData
    
    def getCalibratedAccData(self):
        accData = self.getAccData()
        return [accData[0] - self.acc_start_x, accData[1] - self.acc_start_y]


    def getAccData(self):
        accel_xout = self.read_word_2c(0x3b)
        accel_yout = self.read_word_2c(0x3d)
        accel_zout = self.read_word_2c(0x3f)

        out_scaled = [0,0,0]
        out_scaled[0] = accel_xout / self.acc_sensitivity
        out_scaled[1] = accel_yout / self.acc_sensitivity
        out_scaled[2] = accel_zout / self.acc_sensitivity

        xy = [0,0]
        xy[0] = self.get_x_rotation(out_scaled[0], out_scaled[1], out_scaled[2])
        xy[1] = self.get_y_rotation(out_scaled[0], out_scaled[1], out_scaled[2])
        return xy

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
    
    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))

    def calibrate(self, samples):
            values = []
            xval = 0
            yval = 0
            val = [0,0]
            accel_out = [0,0,0]

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