from gyro import *


gyro = gyro(0.1)

start = gyro.gyro_start_x
print("avg: ", start)
x = 0
current_time = time.time()
last_time = current_time

while 1:
    current_time = time.time()
    dt = current_time - last_time
    
    gData = gyro.getGyroData()
    os.system('clear')
    
    print("gyro data")
    print("---------")
    print("x: ", gData[0])
    x += (gData[0] * dt)
    print("angle: ", x)

    last_time = current_time
