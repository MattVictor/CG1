__package__

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class GLUTFrame2D(OpenGLFrame):
    def __init__(self, master, forma, **kwargs):
        super().__init__(master,**kwargs)
        
        self.bind("<Button>", self.mouseClick)
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []
        
        self.clicked_points_line = []
        self.clicked_points = []
        self.point_color = (1.0,1.0,1.0)
        self.modoEscuro = True
        self.showAxis = True
        self.recorte = False
        self.forma = forma
    
    def initgl(self):
        glViewport(0,0,self.width,self.height)
        glLoadIdentity()
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glPointSize(1)  # Tamanho dos pontos
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  # Mantém coordenadas normalizadas
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.redraw()
        
    def redraw(self):
        """ Função para desenhar os pontos na tela """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GL_PIXEL = GL_POINTS
        glLoadIdentity()
        
        if(self.showAxis):
            # --- Eixos ---
            glLineWidth(1)
            glColor3f(1.0, 0.0, 0.0)  # vermelho
            glBegin(GL_LINES)
            glVertex2f(-1, 0)
            glVertex2f(1, 0)
            glEnd()

            glColor3f(0.0, 1.0, 0.0)  # verde
            glBegin(GL_LINES)
            glVertex2f(0, -1)
            glVertex2f(0, 1)
            glEnd()

        # Desenha os pontos clicados
        glColor3f(*self.point_color)

        # Primitiva
        glBegin(GL_PIXEL)
        for x, y in self.clicked_points:
            glVertex2f(x, y)
        glEnd()

        self.tkSwapBuffers()
        
    def dadosFornecidos(self,x1=0,y1=0,x2=False,y2=False,raio=False,figura=False):
        if raio:
            clicked_points = self.forma.drawFunction(self.clicked_points_line,[x1,y1], raio)
        if figura:
            clicked_points = figura.drawPoints()
        else:
            clicked_points = self.forma.drawFunction([x1,y1,x2,y2])
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []

        for x1, y1 in clicked_points:
            self.mostrar_coordenadas(coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
        
        self.redraw()
    
    def mouseClick(self, event):
        """ Captura cliques do mouse e converte para coordenadas normalizadas"""
        window_width = self.width/2
        window_height = self.height/2

        print(window_width)
        print(window_height)
        
        x,y = event.x, event.y
        
        if event.num == 1:
            # Converte as coordenadas da tela para coordenadas normalizadas OpenGL
            self.normalizeAndAddPoints(event.x,event.y)
            self.mostrar_coordenadas(coords=[x,y])
        elif event.num == 3:
            # Desenha uma linha nos pontos escolhidos
            
            self.clicked_points_line.append((x / self.width) * self.width - window_width)
            self.clicked_points_line.append((1 - (y / self.height)) * self.height - window_height)
            
            if(len(self.clicked_points_line) == 4):
                self.algoritmoDoisPontos()
                
                self.clicked_points_line = []
        
        self.redraw()
        
    def algoritmoDoisPontos(self):
        clicked_points = self.forma.drawFunction(self.clicked_points_line)
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []

        for x1, y1 in clicked_points:
            self.mostrar_coordenadas(coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
            
    def normalizeAndAddPoints(self,x,y):
        normalized_x = x/(self.width/2)
        normalized_y = y/(self.height/2)
        
        # Armazena o ponto clicado
        self.coordenadas_OpenGL.append((f"{(normalized_x):.3f}",f"{(normalized_y):.3f}"))
        self.clicked_points.append((normalized_x, normalized_y))

    def mostrar_coordenadas(self,coords):
        self.coordenadas_Mundo.append((f"{(coords[0]):.3f}",f"{(coords[1]):.3f}"))
        self.coordenadas_Tela.append((round(coords[0]+(self.width/2)),round((coords[1]-(self.height/2))*-1)))
    
    def setForma(self,novaForma):
        self.forma = novaForma
    
    def invertColors(self):
        if self.modoEscuro:
            self.modoEscuro = False
            self.point_color = (0,0,0)
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            self.modoEscuro = True
            self.point_color = (1,1,1)
            glClearColor(0.0, 0.0, 0.0, 1.0)  
        
        self.redraw()
        
    def clearScreen(self):
        self.clicked_points = []
        self.redraw()
    