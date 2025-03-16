import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Lista para armazenar os pontos clicados em coordenadas normalizadas
clicked_points_line = []
clicked_points = []
point_color = (0.0, 0.0, 0.0)  # Cor dos pontos (preto)

# Tamanho inicial da janela
window_width = 800
window_height = 600

def draw():
    """ Função para desenhar os pontos na tela """
    glClear(GL_COLOR_BUFFER_BIT)
    GL_PIXEL = GL_POINTS
    glLoadIdentity()

    # Desenha os pontos clicados
    glColor3f(*point_color)
    glPointSize(0.1)

    # Primitiva
    glBegin(GL_PIXEL)
    for x, y in clicked_points:
        glVertex2f(x, y)
    glEnd()

    glutSwapBuffers()

def converter_coordenadas_mouse(windowSize, coords):

    mouse_x = int(coords[0])
    mouse_y = int(coords[1])
    
    mouseMin_x = 0
    mouseMax_x = windowSize[0]
    
    mouseMin_y = windowSize[1]
    mouseMax_y = 0

    glMin = -1
    glMax = 1

    point_x = ((mouse_x - mouseMin_x) * (glMax - glMin) / (mouseMax_x - mouseMin_x)) + glMin
    point_y = ((mouse_y - mouseMin_y) * (glMax - glMin) / (mouseMax_y - mouseMin_y)) + glMin

    return [point_x, point_y]

def converter_coordenadas_tela(screenSize, coords):

    screen_x = coords[0]
    screen_y = coords[1]
    
    screenMin_x = 0
    screenMax_x = screenSize[0]
    
    screenMin_y = screenSize[1]
    screenMax_y = 0

    glMin = -1
    glMax = 1
    
    point_x = (screen_x + 1) / 2 * screenMax_x
    point_y = (-screen_y + 1) / 2 * screenMin_y

    return [point_x, point_y]

def mostrar_coordenadas(window,state,coords):
    normalized_x, normalized_y = converter_coordenadas_mouse([window[0],window[1]],coords)
    coord_tela = converter_coordenadas_tela([1920,1080],[normalized_x,normalized_y])
    
    if state == 0:
        print(f'coordenadas mundo: ({coord_tela[0]:.3f},{coord_tela[1]:.3f})')
        print(f'coordenadas convertidas OpenGL: ({normalized_x:.3f}, {normalized_y:.3f})')
        print(f'coordenadas convertidas tela: ({coords[0]}, {coords[1]})\n')

def mouseClick(button, state, x, y):
    """ Captura cliques do mouse e converte para coordenadas normalizadas"""
    global window_width, window_height

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Converte as coordenadas da tela para coordenadas normalizadas OpenGL
        normalizeAndAddPoints(x,y)
        mostrar_coordenadas([window_width,window_height],state,[x,y])
        
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Desenha uma linha nos pontos escolhidos
        mostrar_coordenadas([window_width,window_height],state,[x,y])
        global clicked_points_line
        
        clicked_points_line.append(x)
        clicked_points_line.append(y)
        
        if(len(clicked_points_line) == 4):
            pontoMedioUltraOPT()
             
            clicked_points_line = []

    glutPostRedisplay()  # Redesenha a tela
    
def DDA():
    x1,x2 = clicked_points_line[0], clicked_points_line[2]
    y1,y2 = clicked_points_line[1], clicked_points_line[3]
    
    lenghtInc = max(abs(x2 - x1),abs(y2 - y1))
    
    xinc = (x2 - x1)/lenghtInc
    yinc = (y2 - y1)/lenghtInc
    
    normalizeAndAddPoints(x1,y1)
    
    if(x1 < x2):
        while(x1 < x2):
            x1 += xinc
            y1 += yinc
            
            normalizeAndAddPoints(x1,y1)
    elif(x1 > x2):
        while(x1 > x2):
            x1 += xinc
            y1 += yinc
            
            normalizeAndAddPoints(x1,y1)
            

def pontoMedioUltraOPT():
    
    x1,x2 = clicked_points_line[0], clicked_points_line[2]
    y1,y2 = clicked_points_line[1], clicked_points_line[3]
    
    dx = x2 - x1
    dy = y2 - y1
    
    a = dy
    b = -dx

    normalizeAndAddPoints(x1,y1)

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

        normalizeAndAddPoints(x1,y1)


def pontoMedio():
    x1,x2 = clicked_points_line[0], clicked_points_line[2]
    y1,y2 = clicked_points_line[1], clicked_points_line[3]
    
    dx = x2 - x1
    dy = y2 - y1
    
    normalizeAndAddPoints(x1,y1)
    
    if(dy <= 0): #Reta em cima do eixo X
        dy *= -1 #deixando positivo (devido ao (0,0) ficar no canto superior esquerdo da tela)
        if(dx >= 0): #Reta no primeiro Quadrante
            if(dx >= dy): #Reta no primeiro Octante
                d = 2 * dy - dx
        
                incE = 2 * dy
                incNE = 2 * (dy-dx)
                
                while(x1 < x2):
                    if (d <= 0):
                        d = d+incE
                        x1 += 1
                    else:
                        d = d+incNE
                        x1 += 1
                        y1 -= 1
                    
                    normalizeAndAddPoints(x1,y1)
            else:# Reta no segundo Octante
                d = dy - 2* dx
        
                incN = 2 * -dx
                incNE = 2 * (dy-dx)
                
                while(x1 < x2):
                    if (d <= 0):
                        d = d+incNE
                        y1 -= 1
                        x1 += 1
                    else:
                        d = d+incN
                        y1 -= 1
                    
                    normalizeAndAddPoints(x1,y1)
                    
        else: #Reta no segundo Quadrante
            dx *= -1
            if(dx <= dy): #Reta no terceiro Octante
                d = -(dy) - 2 * dx
        
                incN = 2 * -dx
                incNW = 2 * (dy-dx)
                
                while(x1 > x2):
                    if (d <= 0):
                        d = d+incNW
                        x1 -= 1
                        y1 -= 1
                    else:
                        d = d+incN
                        y1 -= 1
                    
                    normalizeAndAddPoints(x1,y1)
                    
            else: #Reta no quarto Octante
                d = 2*dy - dx
        
                incW = 2 * dy
                incNW = 2 * (dy-dx)

                while(x1 > x2):
                    if (d <= 0):
                        d = d+incW
                        x1 -= 1
                    else:
                        d = d+incNW
                        x1 -= 1
                        y1 -= 1
                    
                    normalizeAndAddPoints(x1,y1)
    else: #Reta abaixo do eixo X
        if(dx <= 0): #Reta no Terceiro Quadrante
            dx *= -1
            if(dx >= dy): #Reta no quinto Octante
                d = -2 * dy - dx
        
                incW = 2 * -dy
                incSW = 2 * (-dy+dx)
                
                while(x1 > x2):
                    if (d <= 0):
                        d = d+incSW
                        x1 -= 1
                        y1 += 1
                    else:
                        d = d+incW
                        x1 -= 1
                    
                    normalizeAndAddPoints(x1,y1)
            else:# Reta no sexto Octante
                d = -dy + 2* dx
        
                incS = 2 * dx
                incSW = 2 * (-dy+dx)
                
                while(x1 > x2):
                    if (d <= 0):
                        d = d+incS
                        y1 += 1
                    else:
                        d = d+incSW
                        x1 -= 1
                        y1 += 1
                    
                    normalizeAndAddPoints(x1,y1)
                    
        else: #Reta no Quarto Quadrante
            dy *= -1
            if(dx <= -dy): #Reta no setimo Octante
                d = dy + 2 * dx
        
                incS = 2 * dx
                incSE = 2 * (dy+dx)
                
                while(x1 < x2):
                    if (d <= 0):
                        d = d+incS
                        y1 += 1
                    else:
                        d = d+incSE
                        x1 += 1
                        y1 += 1
                    
                    normalizeAndAddPoints(x1,y1)
                    
            else: #Reta no oitavo Octante
                d = 2*dy + dx
        
                incE = 2 * dy
                incSE = 2 * (dy+dx)

                while(x1 < x2):
                    if (d >= 0):
                        d = d+incE
                        x1 += 1
                    else:
                        d = d+incSE
                        x1 += 1
                        y1 += 1
                    
                    normalizeAndAddPoints(x1,y1)

def pontoMedioOPT():
    x1,x2 = clicked_points_line[0], clicked_points_line[2]
    y1,y2 = clicked_points_line[1], clicked_points_line[3]
    
    dx = x2 - x1
    dy = y2 - y1
    
    d=0
    
    incDMaior = 0
    incDMenor = 0
    
    incXMaior = 1
    incXMenor = 1
    incYMenor = 1
    incYMaior = 1
    
    normalizeAndAddPoints(x1,y1)
    
    if(dx >= 0): #Reta do lado Direito do eixo dos Y
        if(dy <= 0): #Reta no primeiro Quadrante
            dy *= -1 #deixando positivo (devido ao (0,0) ficar no canto superior esquerdo da tela)
            if(dx >= dy): #Reta no primeiro Octante
                d = 2 * dy - dx
        
                incDMenor = 2 * dy
                incDMaior = 2 * (dy-dx)
                
                incXMenor,incXMaior = 1, 1
                incYMenor, incYMaior = 0,-1

            else:# Reta no segundo Octante
                d = dy - 2* dx
        
                incDMaior = 2 * -dx
                incDMenor = 2 * (dy-dx)
                
                incXMenor,incXMaior = 1, 0
                incYMenor, incYMaior = -1,-1
        
        else: #Reta no Quarto Quadrante
            dy *= -1
            if(dx <= -dy): #Reta no setimo Octante
                d = dy + 2 * dx
        
                incDMenor = 2 * dx
                incDMaior = 2 * (dy+dx)
                
                incXMenor,incXMaior = 0, 1
                incYMenor, incYMaior = 1,1
                    
            else: #Reta no oitavo Octante
                d = 2*dy + dx
        
                incDMaior = 2 * dy
                incDMenor = 2 * (dy+dx)
                
                incXMenor,incXMaior = 1, 1
                incYMenor, incYMaior = 1,0

        while(x1 < x2):
            if (d <= 0):
                d += incDMenor
                x1 += incXMenor
                y1 += incYMenor
            else:
                d += incDMaior
                x1 += incXMaior
                y1 += incYMaior
            
            normalizeAndAddPoints(x1,y1)

    elif(dx <= 0): #Reta do lado esquerdo do eixo dos Y
        dx *= -1
        if(dy <= 0): #Reta no segundo Quadrante
            dy *= -1
            if(dx <= dy): #Reta no terceiro Octante
                d = dy - 2 * dx
        
                incDMaior = 2 * -dx
                incDMenor = 2 * (dy-dx)
                
                incXMenor,incXMaior = -1, 0
                incYMenor, incYMaior = -1,-1
                    
            else: #Reta no quarto Octante
                d = 2*dy - dx
        
                incDMenor = 2 * dy
                incDMaior = 2 * (dy-dx)
                
                incXMenor,incXMaior = -1, -1
                incYMenor, incYMaior = 0,-1
                    
        else: #Reta no Terceiro Quadrante
            if(dx >= dy): #Reta no quinto Octante
                d = -2 * dy - dx
        
                incDMaior = 2 * -dy
                incDMenor = 2 * (-dy+dx)
                
                incXMenor,incXMaior = -1, -1
                incYMenor, incYMaior = 1, 0

            else: # Reta no sexto Octante
                d = -dy + 2* dx
        
                incDMenor = 2 * dx
                incDMaior = 2 * (-dy+dx)
                
                incXMenor,incXMaior = 0, -1
                incYMenor, incYMaior = 1, 1
        
        while(x1 > x2):
            if (d <= 0):
                d += incDMenor
                x1 += incXMenor
                y1 += incYMenor
            else:
                d += incDMaior
                x1 += incXMaior
                y1 += incYMaior
            
            normalizeAndAddPoints(x1,y1)


def normalizeAndAddPoints(x,y):
    global clicked_points
    
    normalized_x = (x / window_width) * 2 - 1
    normalized_y = -((y / window_height) * 2 - 1)

    # Armazena o ponto clicado
    clicked_points.append((normalized_x, normalized_y))

def reshape(width, height):
    """ Ajusta a projeção ao redimensionar a janela """
    global window_width, window_height
    window_width = width
    window_height = height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)  # Mantém coordenadas normalizadas
    glMatrixMode(GL_MODELVIEW)

def main():
    """ Inicializa a janela e define os callbacks """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"OpenGL Clickable Points")

    glClearColor(1.0, 1.0, 1.0, 1.0)  # Define o fundo preto
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)

    glutDisplayFunc(draw)
    glutMouseFunc(mouseClick)
    glutReshapeFunc(reshape)  # Captura redimensionamento da janela

    glutMainLoop()

if __name__ == "__main__":
    main()
