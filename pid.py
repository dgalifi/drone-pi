import math

class PID:
	#"""
	#Discrete PID control
	#"""

    def __init__(self, P=0.0, I=0.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=400, Integrator_min=-400):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator = Derivator
        self.Integrator = Integrator
        self.Integrator_max = Integrator_max
        self.Integrator_min = Integrator_min

        self.set_point = 0.0
        self.error = 0.0
        
        self.arrCount = 20
        self.index = 0
        self.arr = [0]
        for i in range(0,self.arrCount):
            self.arr.append(0)

    def update(self,current_value, dt):

        self.error = self.set_point - current_value
        
        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator) / dt
        self.Derivator = self.error
        self.Integrator = self.Integrator + (self.error * dt)

        self.I_value = self.Integrator * self.Ki

        if self.I_value > self.Integrator_max:
            self.I_value = self.Integrator_max
        elif self.I_value < self.Integrator_min:
            self.I_value = self.Integrator_min

        PID = self.P_value + self.I_value + self.D_value
        
        return math.floor(PID)
    
    def setParameters(self, p,i,d):
        self.Kp = p
        self.Ki = i
        self.Kd = d
        
    def setPoint(self, point):
        self.set_point = point