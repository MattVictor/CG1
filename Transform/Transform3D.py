__package__

import numpy as np

class Transform3D():
    def __init__(self):
        pass
    
    def homogenCoordinates(self,points):
        homogenCoords = []
        
        for x,y,z in points:
            homogenCoords.append([x,y,z,1])
            
        return homogenCoords
            
    def multiplyMatrix(self,matrix1,matrix2):
        newPosition = []
        
        for point in matrix2:
            newPoint = []
            for i in range(len(matrix1)):
                value = 0
                for j in range(len(point)):
                    value += matrix1[i][j] * point[j]
                
                newPoint.append(value)
            
            newPosition.append((round(newPoint[0]), round(newPoint[1]), round(newPoint[2])))
            
        return newPosition
    
    def transposition(self,points, movedPoints):
        newPosition = points

        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
        
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, 0, movedPoints[0]],
            [0, 1, 0, movedPoints[1]],
            [0, 0, 1, movedPoints[2]],
            [0, 0, 0, 1]
        ]

        newPosition = self.multiplyMatrix(transpositionMatrix, homogenCoords)

        return newPosition
    
    def scale(self, points, movedPoints):
        newPosition = points

        transpositionPoints = newPosition[0]

        newPosition = self.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1, transpositionPoints[2]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)

        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0, 0],
            [0, movedPoints[1], 0, 0],
            [0, 0, movedPoints[2], 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(scaleMatrix, homogenCoords)

        newPosition = self.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def rotation(self, points, x, y, z):
        newPosition = points

        if x != 0:
            newPosition = self.rotationX(newPosition, x)
        if y != 0:
            newPosition = self.rotationY(newPosition, y)
        if z != 0:
            newPosition = self.rotationZ(newPosition, z)
            
        return newPosition
    
    def rotationX(self, points,angle):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
    
        #matriz para Rotação
        rotationMatrix = [
            [1, 0, 0, 0],
            [0, np.cos(theta), -np.sin(theta), 0],
            [0, np.sin(theta), np.cos(theta), 0],
            [0, 0, 0, 1]
        ]

        newPosition = self.multiplyMatrix(rotationMatrix, homogenCoords)

        return newPosition
    
    def rotationY(self, points,angle):
        newPosition = points

        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
    
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), 0, np.sin(theta), 0],
            [0, 1, 0, 0],
            [-np.sin(theta), 0, np.cos(theta), 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition
    
    def rotationZ(self, points,angle):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionXY(self, points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Reflexão em X
        reflectioMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionYZ(self, points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionXZ(self, points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def schear(self, points, x, y, z):
        newPosition = points
        
        transpositionPoints = newPosition[0]
        
        newPosition = self.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1, transpositionPoints[2]*-1])
        
        if x == 0:
            newPosition = self.schearX(newPosition, y, z)
        if y == 0:
            newPosition = self.schearY(newPosition, x, z)
        if z == 0:
            newPosition = self.schearZ(newPosition, x, y)
            
        newPosition = self.transposition(newPosition, transpositionPoints)
            
        return newPosition
    
    def schearX(self, points, y, z):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Cisalhamento em X
        schearMatrix = [
            [1, 0, 0, 0],
            [y, 1, 0, 0],
            [z, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearY(self, points, x, z):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, x, 0, 0],
            [0, 1, 0, 0],
            [0, z, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearZ(self, points, x, y):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = self.homogenCoordinates(points)
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, 0, x, 0],
            [0, 1, y, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = self.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition