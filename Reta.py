class Reta():    
    def __init__(self):
        self.currentFunction = self.DDA
        
    def setAlgoritmo(self,novoAlgoritmo):
        self.currentFunction = novoAlgoritmo
    
    def drawFunction(self,clicked_points):
        return self.currentFunction(clicked_points)
    
    def DDA(self,clicked_points_line):
        print("USANDO DDA")
        lighted_pixels = []
        
        x1,x2 = clicked_points_line[0], clicked_points_line[2]
        y1,y2 = clicked_points_line[1], clicked_points_line[3]
        
        lenghtInc = max(abs(x2 - x1),abs(y2 - y1))
        
        xinc = (x2 - x1)/lenghtInc
        yinc = (y2 - y1)/lenghtInc
        
        lighted_pixels.append((x1,y1))
        
        if(x1 < x2):
            while(x1 < x2):
                x1 += xinc
                y1 += yinc
                
                lighted_pixels.append((x1,y1))
        elif(x1 > x2):
            while(x1 > x2):
                x1 += xinc
                y1 += yinc
                
                lighted_pixels.append((x1,y1))
        
        return lighted_pixels
    
    def pontoMedio(self, clicked_points_line):
        print("USANDO PONTO MÉDIO")
        lighted_pixels = []
        
        x1,x2 = clicked_points_line[0], clicked_points_line[2]
        y1,y2 = clicked_points_line[1], clicked_points_line[3]
        
        dx = x2 - x1
        dy = y2 - y1
        
        a = dy
        b = -dx
        
        lighted_pixels.append((x1,y1))

        if dx == 0: ds1 = 1
        else: ds1 = dx/abs(dx) # sinal do dx (-1 ou 1)

        if dy == 0: ds2 = 1
        else: ds2 = dy/abs(dy) # sinal do dy
        
        incXMenor = ds1
        incYMenor = ds2
        incXMaior = incXMenor
        incYMaior = incYMenor
        
        if abs(dx) > abs(dy):
            d = 2*ds1*a + ds2*b
            inc1 = ds2*a
            inc2 = ds2*a + ds1*b
            incYMenor = 0

            stop1 = x1
            stop2 = x2
        else:
            d = ds1*a + 2*ds2*b
            inc1 = ds1*b
            inc2 = ds2*a + ds1*b
            incXMenor = 0

            stop1 = y1
            stop2 = y2

        while(stop1 != stop2):

            if abs(dy) > abs(dx):
                if (d <= 0):
                    d  += inc2
                    x1 += incXMaior
                    y1 += incYMaior
                else:
                    d  += inc1
                    x1 += incXMenor
                    y1 += incYMenor
                stop1 = y1
                stop2 = y2
            else:
                if (d >= 0):
                    d  += inc2
                    x1 += incXMaior
                    y1 += incYMaior
                else:
                    d  += inc1
                    x1 += incXMenor
                    y1 += incYMenor
                stop1 = x1
                stop2 = x2

            lighted_pixels.append((x1,y1))
            
        return lighted_pixels