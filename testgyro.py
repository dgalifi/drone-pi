from gyro import *
from driver import *
import pigpio
import time

try:
    pi = pigpio.pi()
    driver = driver(pi, 17,18,19,20,1500)

    gyro = gyro()

    start = gyro.gyro_start_x
    print("avg: ", start)
    x = 0

    stop = 0
    setGyroAngles = 0
    output = [0,0]

   # driver.initialise()
    last_time =  time.time()
    
    aData = gyro.getAccData()                
    gData = gyro.getGyroData()
    
    print("acc calib: ", gyro.acc_start_x)
    print("aData: ", aData)

    with open('acc_values.txt', 'w') as f:
        
        while stop == 0:
            current_time = time.time()
            dt = current_time - last_time

            aData = gyro.getAccData()   
            gData = gyro.getGyroData()
            
            x +=  (gData[0] * dt * 0.96) + (aData[0] * 0.04)
            
            # f.write(str(aData[0])+"\n")
            f.write(str(dt)+"\n")
            print("dt: ", dt)

            last_time = current_time
            
        # current_time = time.time()
        
        # dt = current_time - last_time

        # if setGyroAngles == 1:
        #     x +=  (gData[0] * dt * 0.96) + (aData[0] * 0.04)
        # else:
        #     x = aData[0]
        #     setGyroAngles = 1
        
        # output[0] = (output[0] * 0.9) + (x * 0.1)

        # os.system('clear')
        
        # print("gyro data")
        # print("---------")
        # print("x angle: ", round(x, 2))
        # print("")
        # print("acc data")
        # print("---------")
        # print("x angle: ", round(aData[0], 2))
        # print("")
        # print("comp filter")
        # print("---------")
        # print("out_x: ", round(output[0], 2))

        # last_time = current_time
        
except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()

   
