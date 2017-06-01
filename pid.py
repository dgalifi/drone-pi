import math

class pid:

    prop = 1;
    
    def __init__(self, p):
        self.prop = p    
    
    def get(self, value):
        if value < 0:
            value = value * (-1)

        return round(self.prop * value)