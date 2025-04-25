import numpy as np

class Transform2D():
    def transposition(points, movedPoints):
        newPosition = []
        
        #transformando em coordenadas homogêneas
        homogenCoords = []
        
        for x,y in points:
            homogenCoords.append([x,y,1])
            
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, movedPoints[0]],
            [0, 1, movedPoints[1]],
            [0, 0, 1]
        ]
        
        for point in homogenCoords:
            newPoint = [(transpositionMatrix[0][0] * point[0] + transpositionMatrix [0][1] * point[1] + transpositionMatrix[0][2] * point[2]),
                        (transpositionMatrix[1][0] * point[0] + transpositionMatrix [1][1] * point[1] + transpositionMatrix[1][2] * point[2]),
                        (transpositionMatrix[2][0] * point[0] + transpositionMatrix [2][1] * point[1] + transpositionMatrix[2][2] * point[2])]
            
            newPosition.append((newPoint[0],newPoint[1]))
        
        return newPosition