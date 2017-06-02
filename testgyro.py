from gyro import *

xy_dt = [0,0]
gyroData = [0,0,0]
accel_out = [0,0,0]

while 1:
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    gyroData[0] = gyro_xout / 131
    gyroData[1] = gyro_yout / 131
    gyroData[2] = gyro_zout / 131
    
    accel_out[0] = read_word_2c(0x3b)
    accel_out[1] = read_word_2c(0x3d)
    accel_out[2] = read_word_2c(0x3f)
    
    xy_dt = comp_filter(xy_dt[0],xy_dt[1],accel_out, gyroData)

    os.system('clear')
    print "gyro data"
    print "---------"
    print "x: ", xy_dt[0]
    print "y: ", xy_dt[1]

    time.sleep(dt)