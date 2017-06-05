import time
import _thread
import pigpio
import keyboard
from gyro import *
from driver import *
from pid import *

M1 = 17
M2 = 18
M3 = 19
M4 = 20

pi = pigpio.pi()
driver = driver(pi, M1,M2,M3,M4,1400)
pulses = 0
stop = 0
dt = 0.01
pid = PID(10.0, 4.0, 0.0, dt)
rotation = [0,0]
calibration = [0, 0]
gyro = gyro(dt)

def get_inc(value):
    return value

def adjust(rotation):
    x = rotation[0]
    y = rotation[1]

    pitch_x = pid.update(x)
    pitch_y = pid.update(y)

    if x > 0:
        driver.pitch('fw', pitch_x)
    elif x < 0 :
        driver.pitch('back', pitch_x)
    else:
        driver.pitch('fw', 0)
        driver.pitch('back', 0)
        
    if y > 0 :
         driver.pitch('left', pitch_y)
    elif y < 0 :
        driver.pitch('right', pitch_y)
    else:
        driver.pitch('left', 0)
        driver.pitch('right', 0)
        
def check_thread():
    global rotation
    xy_dt = [0,0]
    gyroData = [0,0,0]
    accel_out = [0,0,0]  

    while stop == 0:
        gyroData = gyro.getGyroData()        
        accAngles = gyro.getAccelerometerAngles()
        
        # get orientation
        xy_dt = gyro.comp_filter(xy_dt[0],xy_dt[1],accAngles, gyroData)
        rotation = [xy_dt[0] - calibration[0] , xy_dt[1] - calibration[1]]
        adjust(rotation)
        print_status()        
        time.sleep(dt)
        
def print_status():
    global rotation
    print("---------------")
    print("| " + str(driver.getSpeed(M1))  + " | " + str(driver.getSpeed(M2)) + " |")
    print("---------------")
    print("| " + str(driver.getSpeed(M4))  + " | " + str(driver.getSpeed(M3)) + " |")
    print("---------------")
    print(str(rotation))

try:
    calibration = gyro.calibrate(100)
    
    # balance point
    print(calibration)

    # initialise driver
    driver.initialise()
    print_status()
    
    # check thread
    _thread.start_new_thread(check_thread, ())

    # main thread waiting for input 
    while stop == 0:
      key = str(keyboard.getKey())
      
      if key[6:] == "[A'": #up
          driver.inc_speed(20)
      elif key[6:] == "[B'": #down
          driver.dec_speed(20)
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
    driver.off()
    
#except:
   # print("generic exception")
   # driver.off()  