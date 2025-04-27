import numpy as np

class Transform2D():
    def homogenCoordinates(points):
        homogenCoords = []
        
        for x,y in points:
            homogenCoords.append([x,y,1])
            
        return homogenCoords
            
    def multiplyMatrix(matrix1,matrix2):
        newPosition = []
        
        for point in matrix2:
            newPoint = [(matrix1[0][0] * point[0] + matrix1 [0][1] * point[1] + matrix1[0][2] * point[2]),
                        (matrix1[1][0] * point[0] + matrix1 [1][1] * point[1] + matrix1[1][2] * point[2]),
                        (matrix1[2][0] * point[0] + matrix1 [2][1] * point[1] + matrix1[2][2] * point[2])]
                
            newPosition.append((int(newPoint[0]),int(newPoint[1])))
            
        return newPosition
                
                
    def transposition(points, movedPoints):
        newPosition = []
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
            
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, movedPoints[0]],
            [0, 1, movedPoints[1]],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(transpositionMatrix, homogenCoords)
        
        return newPosition

    def scale(points, movedPoints):
        newPosition = []
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
            
        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0],
            [0, movedPoints[1], 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(scaleMatrix, homogenCoords)
        
        return newPosition
    
    def rotation(points, angle):
        newPosition = []
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition