import numpy as np

class Transform2D():
    def homogenCoordinates(points, text):
        homogenCoords = []
        
        text += "Primeiro Homogenizamos as coordenadas, adicionando 1 como uma coordenada adicional: \n\n"
        
        for x,y in points:
            homogenCoords.append([x,y,1])
            
        text += f"Novos pontos homogenizados: {homogenCoords}\n"
            
        return [homogenCoords,text]
            
    def multiplyMatrix(matrix1,matrix2, text):
        newPosition = []
        
        for point in matrix2:
            newPoint = []
            text += "["
            for i in range(len(matrix1)):
                text += "("
                value = 0
                for j in range(len(point)):
                    value += matrix1[i][j] * point[j]
                    text += f" {matrix1[i][j]} * {point[j]}"
                    if(j != (len(point)-1)):
                        text+= " + "
                
                text += ")"
                
                if(j != (len(matrix1)-1)):
                        text+= ","
                
                newPoint.append(value)
            
            text += "]\n"
            
            text += f"= {newPoint}\n\n"
            newPosition.append((round(newPoint[0]), round(newPoint[1])))
            
        return [newPosition,text]
                
                
    def transposition(points, movedPoints, text):
        newPosition = points
        
        text += "Transposição: \n\n"
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(newPosition,text)
        
        text += "Utilizamos da matriz: \n[1, 0, x]\n[0, 1, y]\n[0, 0, 1]\n\n"
        
        #matriz para transposição
        transpositionMatrix = [
            [1, 0, movedPoints[0]],
            [0, 1, movedPoints[1]],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(transpositionMatrix, homogenCoords,text)
        
        text += f"Por fim temos os novos pontos transladados: {newPosition}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n"
        
        return newPosition, text

    def scale(points, movedPoints,text):
        newPosition = points
        
        text += "Escala: \n\n"
        
        transpositionPoints = newPosition[0]
        
        text += "Primeiro Precisamos transladar o ponto para a origem, para evitar erros na hora da operação: \n"
        
        newPosition,text = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1],text)
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(newPosition,text)
        
        text += "Utilizamos da matriz: \n[x, 0, 0]\n[0, y, 0]\n[0, 0, 1]\n\n"
        
        #matriz para escala
        scaleMatrix = [
            [movedPoints[0], 0, 0],
            [0, movedPoints[1], 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(scaleMatrix, homogenCoords,text)
        
        text += "Depois trazemos objeto de volta ao ponto anterior com outra Transladação\n"
        
        newPosition,text = Transform2D.transposition(newPosition, transpositionPoints,text)
        
        return newPosition,text
    
    def rotation(points,angle,x,y,text):
        newPosition = points
        
        text += "Rotação: \n\n"
        
        reposition = False
        
        if (x != 0) or (y != 0):
            text += "Primeiro Precisamos transladar o ponto para a origem, para evitar erros na hora da operação: \n\n"
            reposition = True
            transpositionPoints = newPosition[0]
        
            newPosition,text = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1],text)
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(newPosition,text)
            
        theta = np.radians(angle)
        
        text += f"Utilizamos da matriz: \n[cos({theta}), -sen({theta}), 0]\n[sen({theta}), cos({theta}), 0]\n[0, 0, 1]\n\n"
        
        #matriz para Rotação
        rotationMatrix = [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(rotationMatrix, homogenCoords,text)
        
        if reposition:
            text += "Depois trazemos objeto de volta ao ponto anterior, com outra Transladação\n"
            newPosition,text = Transform2D.transposition(newPosition, transpositionPoints,text)

        text += f"Por fim temos os novos pontos Rotacionados: {newPosition}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n"
        
        return newPosition,text
    
    def reflectionX(points,text):
        newPosition = points
        
        text += "Reflexão em X: \n\n"
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(points,text)
        
        text += "Utilizamos da matriz: \n[1, 0, 0]\n[0, -1, 0]\n[0, 0, 1]\n\n"
        
        #matriz para Reflexão em X
        reflectioMatrix = [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(reflectioMatrix, homogenCoords,text)
        
        text += f"Por fim temos os novos pontos Refletidos: {newPosition}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n"
        
        return newPosition,text
    
    def reflectionY(points,text):
        newPosition = points
        
        text += "Reflexão em Y: \n\n"
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(points,text)
        
        text += "Utilizamos da matriz: \n[-1, 0, 0]\n[0, 1, 0]\n[0, 0, 1]\n\n"
        
        #matriz para Reflexão em Y
        reflectioMatrix = [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(reflectioMatrix, homogenCoords,text)
        
        text += f"Por fim temos os novos pontos Refletidos: {newPosition}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n"
        
        return newPosition,text
    
    def schear(points, x, y,text):
        newPosition = points
        
        text += "Cisalhamento: \n\n"
        
        transpositionPoints = newPosition[0]
        
        text += "Primeiro Precisamos transladar o ponto para a origem, para evitar erros na hora da operação: \n\n"
        
        newPosition, text = Transform2D.transposition(newPosition, [transpositionPoints[0]*-1,transpositionPoints[1]*-1],text)
        
        if x != 0:
            newPosition, text = Transform2D.schearX(newPosition,x,text)
        if y != 0:
            newPosition, text = Transform2D.schearY(newPosition,y,text)
            
        text += "Depois trazemos objeto de volta ao ponto anterior, com outra Transladação\n"
            
        newPosition, text = Transform2D.transposition(newPosition, transpositionPoints,text)
        
        text += f"Por fim temos os novos pontos Cisalhados: {newPosition}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n"
            
        return newPosition, text
    
    def schearX(points, value,text):
        newPosition = points
        
        text += "Cisalhamento em X: \n\n"
        
        #transformando em coordenadas homogêneas
        homogenCoords, text = Transform2D.homogenCoordinates(points,text)
        
        text += "Utilizamos da matriz: \n[1, x, 0]\n[0, 1, 0]\n[0, 0, 1]\n\n"
        
        #matriz para Cisalhamento em X
        schearMatrix = [
            [1, value, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(schearMatrix, homogenCoords,text)
        
        return newPosition,text
    
    def schearY(points, value,text):
        newPosition = points
        
        text += "Cisalhamento em Y: \n\n"
        
        #transformando em coordenadas homogêneas
        homogenCoords,text = Transform2D.homogenCoordinates(points,text)
        
        text += "Utilizamos da matriz: \n[1, 0, 0]\n[y, 1, 0]\n[0, 0, 1]\n\n"
        
        #matriz para Cisalhamento em Y
        schearMatrix = [
            [1, 0, 0],
            [value, 1, 0],
            [0, 0, 1]
        ]
        
        text += "Para definir as novas coordenadas, realizando a multiplicação desta matriz por cada ponto do quadrado temos:\n\n"
        
        newPosition,text = Transform2D.multiplyMatrix(schearMatrix, homogenCoords,text)
        
        return newPosition,text