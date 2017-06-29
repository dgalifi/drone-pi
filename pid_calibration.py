import time
import _thread
import pigpio
import keyboard
from gyro import *
from driver import *
from pid import *
import os

M1 = 17
M2 = 18
M3 = 19
M4 = 20

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4,1500)
pulses = 0
stop = 0
start = 0

p = 0.0
i = 0.0
d = 0.0

pid_x = PID()

rotation = [0,0]
calibration = [0, 0]
gyro = gyro()

def get_inc(value):
    return value

def adjust(rotation, dt):
    global p
    global i
    global d
    x = rotation[0]
    y = rotation[1]

    pitch_x = pid_x.update(x, dt, p, i, d)

    if x != 0:
        driver.pitch('x', pitch_x)
    else:
        driver.pitch('x', 0)
        
def check_thread():
    global rotation
    global stop
    global start
    xy_dt = [0,0]
    gyroData = [0,0,0]
    accel_out = [0,0,0]  
    x_gyro = 0
    current_time = time.time()
    last_time = current_time

    while stop == 0:
        current_time = time.time()
        dt = current_time - last_time

        # get orientation
        gyroData = gyro.getGyroData()     
        aData = gyro.getCalibratedAccData()

        x_gyro += (gyroData[0] * 0.9996 * dt) + (aData[0] * 0.0004) 
        
        rotation = [x_gyro, 0]
        
        # start printing status
        if start == 1:
            adjust(rotation, dt)

        last_time = current_time

def print_status():
    global p
    global i
    global d
    os.system('clear')
    print("----------------------")
    print("|  P    |   I   |   D   |")
    print("--------------------")
    print("|  " + str(p) + "  |  "+ str(i) + "   |  " + str(d) +  "  |")
    print("----------------------")
    print("x : ", x_gyro)
try:
    # balance point
    pid_x.setPoint(0)

    # check thread
    _thread.start_new_thread(check_thread, ())

    # initialise driver
    driver.initialise()
    start = 1

    # main thread waiting for input 
    while stop == 0:
        print_status()

        key = str(keyboard.getKey())
      
        if key[6:] == "[A'": #up
            driver.inc_speed(2)
        elif key[6:] == "[B'": #down
            driver.dec_speed(2)
        elif key == "b'p'":
            try:
                p = float(input("enter value for P"))
            except:
                print('invalid')
        elif key == "b'i'":
            try:
                i = float(input("enter value for I"))
            except:
                print('invalid')
        elif key == "b'd'":
            try:
                d = float(input("enter value for D"))
            except:
                print('invalid')
        else:
            print(key)
                      
    print("end loop")
    driver.off()


except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()