import time
import _thread
import pigpio
import keyboard
from rotation import *
from driver import *
from pid import *

M1 = 17
M2 = 18
M3 = 19
M4 = 20

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4)
pulses = 0
stop = 0
accelerometer = accelerometer()
pid = pid(10)
rotation = [0,0]
calibration = [0, 0]

gap = 0

def get_inc(value):
    return value

def adjust(rotation):
    x = rotation[0]
    y = rotation[1]

    pitch_x = pid.get(x)
    pitch_y = pid.get(y)

    if x > 0 + gap:
        driver.pitch('fw', pitch_x)
    elif x < 0 - gap:
        driver.pitch('back', pitch_x)
    else:
        driver.pitch('fw', 0)
        driver.pitch('back', 0)
        
    if y > 0 + gap:
         driver.pitch('left', pitch_y)
    elif y < 0 - gap:
        driver.pitch('right', pitch_y)
    else:
        driver.pitch('left', 0)
        driver.pitch('right', 0)

def check_orientation():
        global rotation
        orientation = accelerometer.get_orientation()
        rotation = [orientation[0] - calibration[0] , orientation[1] - calibration [1]]
        adjust(rotation)
        
def check_thread():
    while stop == 0:
        check_orientation()
        print_status()        
        time.sleep(0.1)
        
def print_status():
    global rotation
    print("---------------")
    print("| " + str(driver.getSpeed(M1))  + " | " + str(driver.getSpeed(M2)) + " |")
    print("---------------")
    print("| " + str(driver.getSpeed(M4))  + " | " + str(driver.getSpeed(M3)) + " |")
    print("---------------")
    print(str(rotation))

try:
    calibration = accelerometer.calibration(100)

    # balance point
    print(calibration)

    # initialise driver
    driver.initialise()
    print_status()
    
    # check thread
    _thread.start_new_thread(check_thread, ())

    input("press any key to stop")
    # main thread waiting for input 
   #while stop == 0:
   #    key = str(keyboard.getKey())
   #    
   #    if key[6:] == "[A'": #up
   #        driver.inc_speed(20)
   #    elif key[6:] == "[B'": #down
   #        driver.dec_speed(20)
   #    elif key == "b'w'":
   #        driver.trim_forward()
   #    elif key == "b's'":
   #        driver.trim_back()
   #    elif key == "b'a'":
   #        driver.trim_left()
   #    elif key == "b'd'":
   #        driver.trim_right()
   #    else:
   #        print(key)
   #                    
    print("end loop")
    driver.off()


except KeyboardInterrupt:
    print("you hit ctrl-c")
    driver.off()
    
#except:
   # print("generic exception")
   # driver.off()  