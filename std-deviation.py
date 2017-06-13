import pigpio
import time
from driver import *
from gyro import *
import math

print("press any key to start")

dt = 0.01
samples = 1000
M1 = 17
M2 = 18
M3 = 19
M4 = 20
values = []
val = 0
xval = 0

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4,1500)
gyro = gyro(dt)

try:
    driver.initialise()
    print('starting in 3 sec')

    time.sleep(3)

    for i in range(0, samples):
        gyroData = gyro.getGyroData()        
        accAngles = gyro.getAccelerometerAngles()

        val = gyro.comp_filter(val, 0, accAngles, gyroData)[0]
        values.append(val)

        xval = xval + val

        time.sleep(dt)

    mean = xval/samples

    std_val = 0
    for i in range(0, samples):
        values[i] = (values[i] - mean) * (values[i] - mean)
        std_val = std_val + values[i]
    
    std_deviation = math.sqrt(std_val / samples)

    print('mean')
    print(mean)
    print('standard_deviation')
    print(std_deviation)

    driver.off()

except KeyboardInterrupt:
    print("you hit ctrl-c")
    driver.off()