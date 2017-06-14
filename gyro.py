#!/usr/bin/python

import smbus
import math
import os
import time

class gyro:

    def __init__(self):
        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
        
        self.acc_sensitivity = 16384.0
        self.gyro_sensitivity = 65.5

        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

        GYRO_CONFIG_REGISTER = 0x1B
        GYRO_500DEG = 0x08

        self.bus.write_byte_data(self.address, GYRO_CONFIG_REGISTER, GYRO_500DEG)

        sumGyro = [0,0,0]
        dataGyro= [0,0,0]
        
        for i in range(0, 2000):
            dataGyro[0] = self.read_word_2c(0x43)
            sumGyro[0] += dataGyro[0]
            
        self.gyro_start_x = sumGyro[0] / 2000
        

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
        gyroData[0] = (gyro_xout - self.gyro_start_x) / self.gyro_sensitivity
        return gyroData

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