import time
import _thread
import pigpio
import keyboard
from gyro import *
from driver import *
from pid import *
import os

def get_inc(value):
    return value

def adjust(rotation, dt):
    x = x_angle

    pitch_x = pid_x.update(x, dt)

    if x != 0:
        driver.pitch('x', pitch_x)
    else:
        driver.pitch('x', 0)
        
def check_thread():
    global stop
    global start
    global x_angle
    global gyro

    current_time = time.time()
    last_time = current_time

    test = 0
    dt = 0.03
    with open('times.txt', 'w') as f:
        while stop == 0:
            current_time = time.time()

            # get orientation
            aData = gyro.getAccData()   
            gData = gyro.getGyroData()

            x_angle = 0.98 * (x_angle + gData[0] * dt) + 0.02 * (aData[0])
            
            # print(str(diff))

            if test == 0:
                test = 1
            else:
                adjust(x_angle, dt)
                sl = time.time() - current_time

                if sl <= dt:
                    time.sleep(dt - sl)
                else:
                    print("out of range")

def print_status():
    global p
    global i
    global d
    global x_angle
    global speed
    os.system('clear')
    print("----------------------")
    print("|  P    |   I   |   D   |")
    print("--------------------")
    print("|  " + str(p) + "  |  "+ str(i) + "   |  " + str(d) +  "  |")
    print("----------------------")
    print("x : ", x_angle)
    print("speed: ", speed)

M1 = 17
M2 = 18
M3 = 19
M4 = 20

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4,1500)
pulses = 0
stop = 0
start = 0

x_angle = 0

p = 0.0
i = 0.0
d = 0.0
set_angle = 0

pid_x = PID()

calibration = [0, 0]
gyro = gyro()

aData = [0,0]
gData = [0,0,0]

speed = 1120

try:
    # balance point
    pid_x.setPoint(0)

    aData = gyro.getAccData()                
    gData = gyro.getGyroData()
    
    x_angle = aData[0]

    print("first value x: ", x_angle)
    # initialise driver
    driver.initialise()
    driver.set_overall_speed(speed)
    start = 1

    # check thread
    _thread.start_new_thread(check_thread, ())

    # main thread waiting for input 
    while stop == 0:
        print_status()
        key = str(keyboard.getKey())
      
        if key[6:] == "[A'": #up
            driver.inc_speed(2)
            speed += 2
        elif key[6:] == "[B'": #down
            driver.dec_speed(2)
            speed -= 2
        elif key == "b'p'":
            try:
                p = float(input("enter value for P"))
                pid_x.setParameters(p,i,d)
            except:
                print('invalid')
        elif key == "b'i'":
            try:
                i = float(input("enter value for I"))
                pid_x.setParameters(p,i,d)
            except:
                print('invalid')
        elif key == "b'd'":
            try:
                d = float(input("enter value for D"))
                pid_x.setParameters(p,i,d)
            except:
                print('invalid')
        elif key == "b's'":
            try:
                set_angle = float(input("set angle"))
                pid_x.setPoint(set_angle)
            except:
                print('invalid')
                      
    print("end loop")
    driver.off()


except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()