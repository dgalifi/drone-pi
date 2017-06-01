import time
import pigpio

class driver:

    def __init__(self,pi, M1, M2, M3, M4):
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.pi = pi
        self.pulses = [0,0,0,0]
        self.abs_speed = 0
        
        # f b r l
        self.trims = [0,0,0,0]
        self.pitches = [0,0,0,0]

        self.MIN = 1000
        self.MAX = 2000

        self.M1Speed = 0
        self.M2Speed = 0
        self.M3Speed = 0
        self.M4Speed = 0

    def initialise(self):
        
        self.pi.set_PWM_frequency(self.M1, 1000)
        self.pi.set_PWM_frequency(self.M2, 1000)
        self.pi.set_PWM_frequency(self.M3, 1000)
        self.pi.set_PWM_frequency(self.M4, 1000)
        self.pi.set_PWM_range(self.M1, 1000)
        self.pi.set_PWM_range(self.M2, 1000)
        self.pi.set_PWM_range(self.M3, 1000)
        self.pi.set_PWM_range(self.M4, 1000)

        self.set_speed(0)

        print("initialisation...")    
        input("disconnect power, press enter to continue")
        
        self.set_speed(2000)
        input("connect battery, then press enter when ready")
        self.set_speed(self.MIN)
        
        print("ready")
        
        input("press enter to start")


    # SET SPEED
    # set speed of all the motors to the same value
    def set_speed(self, pulse):
        self.abs_speed = pulse
        
        self.pi.set_servo_pulsewidth(self.M1, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M2, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M3, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M4, self.abs_speed)

    def set_pitch_forward(self, value):
        self.pitches[0] = value
        self.updateMotorSpeed(self.M3)
        self.updateMotorSpeed(self.M4)
        
    def set_pitch_back(self, value):
        self.pitches[1] = value
        self.updateMotorSpeed(self.M1)
        self.updateMotorSpeed(self.M2)
        
    def set_pitch_right(self, value):
        self.pitches[2] = value
        self.updateMotorSpeed(self.M1)
        self.updateMotorSpeed(self.M4)
        
    def set_pitch_left(self, value):
        self.pitches[3] = value
        self.updateMotorSpeed(self.M2)
        self.updateMotorSpeed(self.M3)
        
    def getActualSpeed(self, motor):
        if motor == self.M1:
            return self.abs_speed + self.trims[1] + self.trims[2] + self.pitches[1] + self.pitches[2]
        if motor == self.M2:
            return self.abs_speed + self.trims[1] + self.trims[3] + self.pitches[1] + self.pitches[3]
        if motor == self.M3:
            return self.abs_speed + self.trims[0] + self.trims[3] + self.pitches[0] + self.pitches[3]
        else:
            return self.abs_speed + self.trims[0] + self.trims[2] + self.pitches[0] + self.pitches[2]

    def updateMotorSpeed(self, motor):
        speed = 0
        if motor == self.M1:
            speed = self.abs_speed + self.trims[1] + self.trims[2] + self.pitches[1] + self.pitches[2]
            self.M1Speed = speed
        if motor == self.M2:
            speed = self.abs_speed + self.trims[1] + self.trims[3] + self.pitches[1] + self.pitches[3]
            self.M2Speed = speed
        if motor == self.M3:
            speed = self.abs_speed + self.trims[0] + self.trims[3] + self.pitches[0] + self.pitches[3]
            self.M3Speed = speed
        else:
            speed = self.abs_speed + self.trims[0] + self.trims[2] + self.pitches[0] + self.pitches[2]
            self.M4Speed = speed
            
         self.pi.set_servo_pulsewidth(motor, speed)

    # THROTTLE UP
    def inc_speed(self, inc):
        
        while inc > 0 :
            if self.abs_speed + max(self.trims) < 2000:
                self.abs_speed = self.abs_speed + 1

                self.pi.set_servo_pulsewidth(self.M1, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M2, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M3, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M4, self.abs_speed)
                
                time.sleep(0.01)
                inc = inc - 1
            else:
                inc = 0
    
    # THROTTLE DOWN
    def dec_speed(self, dec):
        
        while dec > 0:
            self.abs_speed = self.abs_speed - 1
            
            if self.abs_speed < 1100:                
                self.set_speed(1000)
                dec = 0
            else:
                self.pi.set_servo_pulsewidth(self.M1, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M2, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M3, self.abs_speed)
                self.pi.set_servo_pulsewidth(self.M4, self.abs_speed)

                time.sleep(0.01)
                dec = dec - 1
    
    # OFF
    def off(self):
        while min(self.pulses) > 1000:
            self.dec_speed(50)
            time.sleep(0.001)
        self.set_speed(0)
        print("off!")
        self.pi.stop()

    def trim_forward(self):

        # check trim_back
        if self.trims[1] > 0:
            self.trims[1] = self.trims[1] - 2

            self.pi.set_servo_pulsewidth(self.M1, self.getSpeed(self.M1))
            self.pi.set_servo_pulsewidth(self.M2, self.getSpeed(self.M2))
        else:
            self.trims[0] = self.trims[0] + 2
            
            self.pi.set_servo_pulsewidth(self.M3, self.getSpeed(self.M3))
            self.pi.set_servo_pulsewidth(self.M4, self.getSpeed(self.M4))
        
    def trim_back(self):

        # check trim_forward
        if self.trims[0] > 0:
            self.trims[0] = self.trims[0] - 2

            self.pi.set_servo_pulsewidth(self.M3, self.getSpeed(self.M3))
            self.pi.set_servo_pulsewidth(self.M4, self.getSpeed(self.M4))
        else:
            self.trims[1] = self.trims[1] + 2
            
            self.pi.set_servo_pulsewidth(self.M1, self.getSpeed(self.M1))
            self.pi.set_servo_pulsewidth(self.M2, self.getSpeed(self.M2))

        #self.print_status()

    def trim_right(self):

        if self.trims[3] > 0:
            self.trims[3] = self.trims[3] - 2
            
            self.pi.set_servo_pulsewidth(self.M2, self.getSpeed(self.M2))
            self.pi.set_servo_pulsewidth(self.M3, self.getSpeed(self.M3))
        else:
            self.trims[2] = self.trims[2] + 2
            
            self.pi.set_servo_pulsewidth(self.M1, self.getSpeed(self.M1))
            self.pi.set_servo_pulsewidth(self.M4, self.getSpeed(self.M4))

        #self.print_status()

    def trim_left(self):

        if self.trims[2] > 0:
            self.trims[2] = self.trims[2] - 2
            
            self.pi.set_servo_pulsewidth(self.M1, self.getSpeed(self.M1))
            self.pi.set_servo_pulsewidth(self.M4, self.getSpeed(self.M4))
        else:
            self.trims[3] = self.trims[3] + 2
            
            self.pi.set_servo_pulsewidth(self.M2, self.getSpeed(self.M2))
            self.pi.set_servo_pulsewidth(self.M3, self.getSpeed(self.M3))
        
