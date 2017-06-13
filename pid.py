import math

class PID:
	#"""
	#Discrete PID control
	#"""

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, dt = 0.01, Integrator_max=500, Integrator_min=-500):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

        self.set_point = 0.0
        self.error = 0.0
        self.dt = dt
        
        self.arrCount = 20
        self.index = 0
        self.arr = [0]
        for i in range(0,self.arrCount):
            self.arr.append(0)

    def update(self,current_value):

        # if current_value < 0:
        #     current_value = current_value * (-1)
            
        self.error = self.set_point - current_value
        
        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error
        self.Integrator = self.Integrator + (self.error * self.dt)

        self.I_value = self.Integrator * self.Ki
        
        PID = self.P_value + self.I_value + self.D_value
        
        return math.floor(PID)
    
    def setPoint(self, point):
        self.set_point = point