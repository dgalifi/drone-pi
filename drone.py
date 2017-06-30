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

pid_x = PID(1.0, 1.2, 9.0)
# pid_y = PID(0.0, 0.0, 0.0, dt)
rotation = [0,0]
calibration = [0, 0]
gyro = gyro()

def get_inc(value):
    return value

def adjust(rotation, dt):
    x = rotation[0]
    y = rotation[1]

    pitch_x = pid_x.update(x, dt)
    # pitch_y = pid_y.update(y)

    # if x > 60:
    #     driver.off()
    #     stop = 1
    #     return
    
    # print('pitch_x: ', pitch_x)

    if x != 0:
        driver.pitch('x', pitch_x)
    else:
        driver.pitch('x', 0)
        
    #if y > 0 :
    #     driver.pitch('left', pitch_y)
    #elif y < 0 :
    #    driver.pitch('right', pitch_y)
    #else:
    #    driver.pitch('left', 0)
    #    driver.pitch('right', 0)
        
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

        x_gyro += ((gyroData[0] * 0.9996) + (aData[0] * 0.0004)) * dt 
        
        rotation = [x_gyro, 0]
        
        # start printing status
        if start == 1:
            # adjust(rotation, dt)
            print_status()

        last_time = current_time

def print_status():
    global rotation
    os.system('clear')
    print("---------------")
    print("| " + str(driver.getSpeed(M1))  + " | " + str(driver.getSpeed(M2)) + " |")
    print("---------------")
    print("| " + str(driver.getSpeed(M4))  + " | " + str(driver.getSpeed(M3)) + " |")
    print("---------------")
    print(str(rotation))

try:
    #calibration = gyro.calibrate(100)
    # balance point
    pid_x.setPoint(0)

    print("avg: ", gyro.gyro_start_x)
    # check thread
    _thread.start_new_thread(check_thread, ())

    # initialise driver
    driver.initialise()
    driver.set_overall_speed(1100)

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
    
#except:
   # print("generic exception")
   # driver.off()  