__package__

import numpy as np

class Transform2D():
    def __init__(self):
        pass
    
    def homogenCoordinates(self,points):
        homogenCoords = []
                
        for x,y in points:
            homogenCoords.append([x,y,1])
                        
        return homogenCoords
            
    def multiplyMatrix(self,matrix1,matrix2):
        newPosition = []
        
        print(matrix2)
        
        for point in matrix2:
            newPoint = []
            for i in range(len(matrix1)):
                value = 0
                for j in range(len(point)):
                    value += matrix1[i][j] * point[j]
                
                newPoint.append(value)
            
            newPosition.append((round(newPoint[0]), round(newPoint[1])))
            
        return newPosition
                
                
    def transposition(self, points, movedPoints):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
        
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, movedPoints[0]],
            [0, 1, movedPoints[1]],
            [0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(transpositionMatrix, homogenCoords)
                
        return newPosition

    def scale(self, points, movedPoints):
        newPosition = points
                
        transpositionPoints = newPosition[0]
                
        newPosition = self.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
                
        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0],
            [0, movedPoints[1], 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(scaleMatrix, homogenCoords)
                
        newPosition = self.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def rotation(self, points,angle,x,y):
        newPosition = points
                
        reposition = False
        
        if (x != 0) or (y != 0):
            reposition = True
            transpositionPoints = (x,y)
        
            newPosition = self.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
                
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(rotationMatrix, homogenCoords)
        
        if reposition:
            newPosition = self.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def reflectionX(self, points):
        newPosition = points
                
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
                
        #matriz para Reflexão em X
        reflectioMatrix = [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(reflectioMatrix, homogenCoords)
                
        return newPosition
    
    def reflectionY(self, points):
        newPosition = points
                
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
                
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(reflectioMatrix, homogenCoords)
                
        return newPosition
    
    def schear(self, points, x, y):
        newPosition = points
                
        transpositionPoints = newPosition[0]
                
        newPosition = self.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        if x != 0:
            newPosition = self.schearX(newPosition,x)
        if y != 0:
            newPosition = self.schearY(newPosition,y)
                        
        newPosition = self.transposition(newPosition, transpositionPoints)
                    
        return newPosition
    
    def schearX(self, points, value):
        newPosition = points
                
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
                
        #matriz para Cisalhamento em X
        schearMatrix = [
            [1, value, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearY(self, points, value):
        newPosition = points
                
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
                
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, 0, 0],
            [value, 1, 0],
            [0, 0, 1]
        ]
                
        newPosition = self.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition