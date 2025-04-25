class Quadrado():
    def __init__(self, x1 = 100, y1 = 100, x2 = 200, y2 = 200):
        self.pontos = []
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def drawPoints(self):
        lighted_pixels = []
        
        #Desenhando Lado Esquerdo e Direito
        for i in range(self.y1, self.y2):
            lighted_pixels.append((self.x1,i))
            lighted_pixels.append((self.x2,i))
            
        #Desenhando Lado Superior e Inferior
        for i in range(self.x1,self.x2):
            print(i)
            lighted_pixels.append((i,self.y1))
            lighted_pixels.append((i,self.y2))
    
        self.pontos = lighted_pixels

        return lighted_pixels