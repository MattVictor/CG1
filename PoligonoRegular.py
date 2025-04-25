from Point import Point

class Quadrado():
    def __init__(self, x1 = 100, y1 = 100, x2 = 200, y2 = 200):
        self.pontos = []
        self.A = Point(x1,y1)
        self.B = Point(x2,y1)
        self.C = Point(x2,y2)
        self.D = Point(x1,y2)
        
    def drawPoints(self):
        lighted_pixels = []
        
        #Desenhando Lado Esquerdo e Direito
        for i in range(self.A.Y, self.C.Y):
            lighted_pixels.append((self.A.X,i))
            lighted_pixels.append((self.B.X,i))
            
        #Desenhando Lado Superior e Inferior
        for i in range(self.A.X,self.C.X):
            lighted_pixels.append((i,self.A.Y))
            lighted_pixels.append((i,self.C.Y))
    
        self.pontos = lighted_pixels

        return lighted_pixels
    
    def getPoints(self):
        return [self.A.getPointAsArray(),
                self.B.getPointAsArray(),
                self.C.getPointAsArray(),
                self.D.getPointAsArray()]
        
    def setPoints(self, newPoints):
        self.A.setPoints(newPoints[0][0], newPoints[0][1])
        self.B.setPoints(newPoints[1][0], newPoints[1][1])
        self.C.setPoints(newPoints[2][0], newPoints[2][1])
        self.D.setPoints(newPoints[3][0], newPoints[3][1])