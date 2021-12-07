
class Dato(object):
    def __init__(self, T,Y1,Y2,Y3,Y4):
        self.T = T
        self.Y1 = Y1
        self.Y2 = Y2
        self.Y3 = Y3
        self.Y4 = Y4

    def setvalores(self, T,Y1,Y2,Y3,Y4):
        self.T = T
        self.Y1 = Y1
        self.Y2 = Y2
        self.Y3 = Y3

    def darValores(self):
        return [self.T,self.Y1,self.Y2,self.Y3,self.Y4]