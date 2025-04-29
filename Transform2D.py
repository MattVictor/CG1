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
            newPoint = []
            for i in range(len(matrix1)):
                value = 0
                for j in range(len(point)):
                    value += matrix1[i][j] * point[j]
                
                newPoint.append(value)
            
            print(newPoint)
            
            newPosition.append((round(newPoint[0]), round(newPoint[1])))
            
        return newPosition
                
                
    def transposition(points, movedPoints):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(newPosition)
            
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, movedPoints[0]],
            [0, 1, movedPoints[1]],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(transpositionMatrix, homogenCoords)
        
        return newPosition

    def scale(points, movedPoints):
        newPosition = points
        
        transpositionPoints = newPosition[0]
        
        newPosition = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(newPosition)
            
        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0],
            [0, movedPoints[1], 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(scaleMatrix, homogenCoords)
        
        newPosition = Transform2D.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def rotation(points,angle,x,y):
        newPosition = points
        
        reposition = False
        
        if (x != 0) or (y != 0):
            reposition = True
            transpositionPoints = newPosition[0]
        
            newPosition = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(rotationMatrix, homogenCoords)
        
        if reposition:
            newPosition = Transform2D.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def reflectionX(points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
        
        #matriz para Reflexão em X
        reflectioMatrix = [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionY(points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def schear(points, x, y):
        newPosition = points
        
        transpositionPoints = newPosition[0]
        
        newPosition = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1])
        
        if x != 0:
            newPosition = Transform2D.schearX(newPosition,x)
        if y != 0:
            newPosition = Transform2D.schearY(newPosition,y)
            
        newPosition = Transform2D.transposition(newPosition, transpositionPoints)
            
        return newPosition
    
    def schearX(points, value):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
        
        #matriz para Cisalhamento em X
        schearMatrix = [
            [1, value, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearY(points, value):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform2D.homogenCoordinates(points)
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, 0, 0],
            [value, 1, 0],
            [0, 0, 1]
        ]
        
        newPosition = Transform2D.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition