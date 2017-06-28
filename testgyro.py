from gyro import *
from driver import *
import pigpio

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
    
    while stop == 0:
        current_time = time.time()
        aData = gyro.getCalibratedAccData()                
        gData = gyro.getGyroData()
        
        dt = current_time - last_time

        x += gData[0] * dt

        if setGyroAngles == 1:
            x = (x * 0.9996) + (aData[0] * 0.0004)
        else:
            x = aData[0]
            setGyroAngles = 1
        
        output[0] = (output[0] * 0.9) + (x * 0.1)
        os.system('clear')
        
        print("gyro data")
        print("---------")
        print("x: ", round(gData[0], 2))
        print("angle: ", round(x, 2))
        print("")
        print("acc data")
        print("---------")
        print("x angle: ", round(aData[0], 2))
        print("")
        print("comp filter")
        print("---------")
        print("out_x: ", round(output[0], 2))

        last_time = current_time
        
except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()

   
