import numpy as np

class Transform3D():
    def homogenCoordinates(points):
        homogenCoords = []
        
        for x,y,z in points:
            homogenCoords.append([x,y,z,1])
            
        return homogenCoords
            
    def multiplyMatrix(matrix1,matrix2):
        newPosition = []
        
        for point in matrix2:
            newPoint = [(matrix1[0][0] * point[0] + matrix1[0][1] * point[1] + matrix1[0][2] * point[2] + matrix1[0][3] * point[3]),
                        (matrix1[1][0] * point[0] + matrix1[1][1] * point[1] + matrix1[1][2] * point[2] + matrix1[1][3] * point[3]),
                        (matrix1[2][0] * point[0] + matrix1[2][1] * point[1] + matrix1[2][2] * point[2] + matrix1[2][3] * point[3]),
                        (matrix1[3][0] * point[0] + matrix1[3][1] * point[1] + matrix1[3][2] * point[2] + matrix1[3][3] * point[3])]
                
            newPosition.append((round(newPoint[0]), round(newPoint[1]), round(newPoint[2])))
            
        return newPosition
    
    def transposition(points, movedPoints):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(newPosition)
            
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, 0, movedPoints[0]],
            [0, 1, 0, movedPoints[1]],
            [0, 0, 1, movedPoints[2]],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(transpositionMatrix, homogenCoords)
        
        return newPosition
    
    def scale(points, movedPoints):
        newPosition = points
        
        transpositionPoints = newPosition[0]
        
        newPosition = Transform3D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1, transpositionPoints[2]*-1])
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(newPosition)
            
        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0, 0],
            [0, movedPoints[1], 0, 0],
            [0, 0, movedPoints[2], 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(scaleMatrix, homogenCoords)
        
        newPosition = Transform3D.transposition(newPosition, transpositionPoints)
        
        return newPosition
    
    def rotation(points, x, y, z):
        newPosition = points
        
        if x != 0:
            newPosition = Transform3D.rotationX(newPosition, x)
        if y != 0:
            newPosition = Transform3D.rotationY(newPosition, y)
        if z != 0:
            newPosition = Transform3D.rotationZ(newPosition, z)
            
        return newPosition
    
    def rotationX(points,angle):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [1, 0, 0, 0],
            [0, np.cos(theta), -np.sin(theta), 0],
            [0, np.sin(theta), np.cos(theta), 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition
    
    def rotationY(points,angle):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), 0, np.sin(theta), 0],
            [0, 1, 0, 0],
            [-np.sin(theta), 0, np.cos(theta), 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition
    
    def rotationZ(points,angle):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(newPosition)
            
        theta = np.radians(angle)
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(rotationMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionXY(points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Reflexão em X
        reflectioMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionYZ(points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def reflectionXZ(points):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(reflectioMatrix, homogenCoords)
        
        return newPosition
    
    def schear(points, x, y, z):
        newPosition = points
        
        transpositionPoints = newPosition[0]
        
        newPosition = Transform3D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1, transpositionPoints[2]*-1])
        
        if x == 0:
            newPosition = Transform3D.schearX(newPosition, y, z)
        if y == 0:
            newPosition = Transform3D.schearY(newPosition, x, z)
        if z == 0:
            newPosition = Transform3D.schearZ(newPosition, x, y)
            
        newPosition = Transform3D.transposition(newPosition, transpositionPoints)
            
        return newPosition
    
    def schearX(points, y, z):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Cisalhamento em X
        schearMatrix = [
            [1, 0, 0, 0],
            [y, 1, 0, 0],
            [z, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearY(points, x, z):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, x, 0, 0],
            [0, 1, 0, 0],
            [0, z, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition
    
    def schearZ(points, x, y):
        newPosition = points
        
        #transformando em coordenadas homogêneas
        homogenCoords = Transform3D.homogenCoordinates(points)
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, 0, x, 0],
            [0, 1, y, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        newPosition = Transform3D.multiplyMatrix(schearMatrix, homogenCoords)
        
        return newPosition