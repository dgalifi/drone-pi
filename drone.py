import time
import _thread
import pigpio
import keyboard
from gyro import *
from driver import *
from pid import *
import os

def adjust(rotation, dt):
    x = rotation[0]
    y = rotation[1]

    pitch_x = pid_x.update(x, dt)
    #pitch_y 

    if x != 0:
        driver.pitch('x', pitch_x)
    else:
        driver.pitch('x', 0)
        
def check_thread():
    global angles
    global stop

    current_time = time.time()
    last_time = current_time
    firstround = 1 
    dt = 0.03

    while stop == 0:
        current_time = time.time()

        # get orientation
        aData = gyro.getAccData()   
        gData = gyro.getGyroData()

        angles[0] = 0.98 * (angles[0] + gData[0] * dt) + 0.02 * (aData[0])
        #angles[1]

        if firstround == 1:
            firstround = 0
        else:
            adjust(angles, dt)
            sl = time.time() - current_time
            # print_status()

            if sl <= dt:
                time.sleep(dt - sl)
            else:
                print("out of range")

def print_status():
    global angles
    os.system('clear')
    print("---------------")
    print("| " + str(driver.getSpeed(M1))  + " | " + str(driver.getSpeed(M2)) + " |")
    print("---------------")
    print("| " + str(driver.getSpeed(M4))  + " | " + str(driver.getSpeed(M3)) + " |")
    print("---------------")
    print(str(angles))

M1 = 17
M2 = 18
M3 = 19
M4 = 20

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4,1500)
pulses = 0
stop = 0
start = 0

pid_x = PID(3, 0.4, 0.5)
# pid_y = PID(0.0, 0.0, 0.0, dt)

angles = [0,0]
calibration = [0, 0]
gyro = gyro()

aData = [0,0]
gData = [0,0,0]

try:
    # balance point
    pid_x.setPoint(0)

    aData = gyro.getAccData()                
    gData = gyro.getGyroData()
    
    angles[0] = aData[0]
    # angles[1] = aData[1]
    
    # initialise driver
    driver.initialise()
    driver.set_overall_speed(1100)

    start = 1

     # check thread
    _thread.start_new_thread(check_thread, ())

    # main thread waiting for input 
    while stop == 0:
      key = str(keyboard.getKey())
      
      if key[6:] == "[A'": #up
          driver.inc_speed(2)
      elif key[6:] == "[B'": #down
          driver.dec_speed(2)
      elif key == "b'w'":
          driver.trim_forward()
      elif key == "b's'":
          driver.trim_back()
      elif key == "b'a'":
          driver.trim_left()
      elif key == "b'd'":
          driver.trim_right()
      else:
          print(key)
                      
    print("end loop")
    driver.off()


except KeyboardInterrupt:
    print("you hit ctrl-c")
    stop = 1
    driver.off()
    
except Exception as e:
    print(str(e))
    driver.off() 