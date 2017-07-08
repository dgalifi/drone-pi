from gyro import *
from driver import *
import pigpio
import time

try:
    pi = pigpio.pi()
    driver = driver(pi, 17,18,19,20,1500)

    gyro = gyro()

    x_angle = 0

    stop = 0

    last_time =  time.time()
    
    aData = gyro.getAccData()                
    gData = gyro.getGyroData()
    
    x_angle = aData[0]
    x_gyro = aData[0]

    driver.initialise()
    driver.set_overall_speed(1120)

    print("acc calib: ", gyro.acc_start_x)
    print("aData: ", aData)

    with open('values.txt', 'w') as f:
        
        f.write("gyro angle x" + "     " + "composite filter x\n")
        while stop == 0:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            aData = gyro.getAccData()   
            gData = gyro.getGyroData()

            x_gyro = x_gyro + gData[0] * dt
            x_angle = 0.98 * (x_angle + gData[0] * dt) + 0.02 * (aData[0])
            
            f.write(str(x_gyro) + "     " + str(x_angle) +"\n")
            print("dt: ", dt)

            os.system('clear')
            
            print("gyro angle")
            print("---------")
            print("x: ", round(x_gyro, 2))

            print("composite filter angle")
            print("---------")
            print("x: ", round(x_angle, 2))
        
except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()

   
