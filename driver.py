import time
import pigpio
# test ssh

class driver:

    def __init__(self,pi, M1, M2, M3, M4, max = 2000):
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.pi = pi
        self.pulses = [0,0,0,0]
        self.abs_speed = 0
        
        # f b r l
        self.trims = [0,0,0,0]
        self.pitches = [0,0]

        self.MIN = 1000
        self.MAX = max

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

        self.set_overall_speed(0)

        print("initialisation...")    
        input("disconnect power, press enter to continue")
        
        self.set_overall_speed(2000)
        input("connect battery, then press enter when ready")
        self.set_overall_speed(self.MIN)
        
        print("ready")
        
        input("press enter to start")

        self.set_overall_speed(1170)
        
    # SET SPEED
    # set speed of all the motors to the same value
    def set_overall_speed(self, pulse):

        if pulse > self.MAX:
            self.abs_speed = self.MAX
        else:
            self.abs_speed = pulse
        
        self.pi.set_servo_pulsewidth(self.M1, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M2, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M3, self.abs_speed)
        self.pi.set_servo_pulsewidth(self.M4, self.abs_speed)
    
    def pitch(self, direction, value):
        if direction == 'x':
            self.pitches[0] = value

        self.updateMotorSpeed()
        
    # GET SPEED
    # get actual speed of a specified motor
    def getSpeed(self, motor):
        if motor == self.M1:
            return self.M1Speed
        elif motor == self.M2:
            return self.M2Speed
        elif motor == self.M3:
            return self.M3Speed
        else:
            return self.M4Speed

    def updateMotorSpeed(self):
        
        m1 = self.abs_speed + self.pitches[0]
        if m1 > self.MAX:
            m1 = self.MAX
        elif m1 < 1100:
            m1 = 1100
        self.M1Speed = m1
    
        m2 = self.abs_speed + self.pitches[0]
        if m2 > self.MAX:
            m2 = self.MAX
        elif m2 < 1100:
            m2 = 1100
        self.M2Speed = m2

        m3 = self.abs_speed - self.pitches[0]
        if m3 > self.MAX:
            m3 = self.MAX
        elif m3 < 1100:
            m3 = 1100
        self.M3Speed = m3

        m4 = self.abs_speed - self.pitches[0]
        if m4 > self.MAX:
            m4 = self.MAX
        elif m4 < 1100:
            m4 = 1100
        self.M4Speed = m4
        
        self.pi.set_servo_pulsewidth(self.M1, self.M1Speed)
        self.pi.set_servo_pulsewidth(self.M2, self.M2Speed)
        self.pi.set_servo_pulsewidth(self.M3, self.M3Speed)
        self.pi.set_servo_pulsewidth(self.M4, self.M4Speed)

    # THROTTLE UP
    def inc_speed(self, inc):
        
        while inc > 0 :
            if self.abs_speed + max(self.trims) < 2000:
                self.abs_speed = self.abs_speed + 1

                self.updateMotorSpeed()
                
                time.sleep(0.01)
                inc = inc - 1
            else:
                inc = 0
    
    
    # THROTTLE DOWN
    def dec_speed(self, dec):
        
        while dec > 0:
            self.abs_speed = self.abs_speed - 1
            
            if self.abs_speed < 1100:                
                self.set_overall_speed(1000)
                dec = 0
            else:
                self.updateMotorSpeed()

                time.sleep(0.01)
                dec = dec - 1
    
    
    # OFF
    def off(self):
        while min(self.pulses) > 1000:
            self.dec_speed(50)
            time.sleep(0.001)
        self.set_overall_speed(0)
        print("off!")
        self.pi.stop()
# needs to be refactored
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
        
