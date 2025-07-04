__package__

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class GLUTFrame3D(OpenGLFrame):
    def __init__(self, master, forma, **kwargs):
        super().__init__(master,**kwargs)
        self.position = [500,500,500]
        
        self.vertices = [
            [0, 0, 0],
            [ 100, 0, 0],
            [ 100,  100, 0],
            [0,  100, 0],
            [0, 0,  100],
            [ 100, 0,  100],
            [ 100,  100,  100],
            [0,  100,  100],
        ]
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []
        
        self.clicked_points_line = []
        self.clicked_points = []
        self.point_color = (1.0,1.0,1.0)
        self.modoEscuro = True
        self.showAxis = True
        self.forma = forma
    
    def initgl(self):
        self.GL_PIXELS = GL_LINES
        
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glPointSize(1)
        glEnable(GL_DEPTH_TEST)
        # Tamanho dos pontos
        
        glViewport(0, 0, self.width, self.height)
        
        x = self.width/2
        y = self.height/2
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-x, x, -y, y, -500, 1000)  # projeção ortográfica
        
        glRotatef(35.264, 1, 0, 0)
        glRotatef(315, 0, 1, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.redraw()
        
    def redraw(self):
        """ Função para desenhar os pontos na tela """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # gluLookAt(self.position[0], self.position[1], self.position[1], 0, 0, 0, 0, 1, 0)

        # Desenhar eixos
        if(self.showAxis):
            self.draw_axes()

        # Desenhar o cubo
        self.draw_cube()

        self.tkSwapBuffers()
        
    def draw_axes(self):
        glLineWidth(1.0)
        glBegin(self.GL_PIXELS)

        x = self.width/2
        y = self.height/2
        z = self.width/2

        if(self.showAxis):
            # Eixo X - vermelho
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(-x, 0, 0)
            glVertex3f(x, 0, 0)

            # Eixo Y - verde
            glColor3f(0.0, 1.0, 0.0)
            glVertex3f(0, -y, 0)
            glVertex3f(0, y, 0)

            # Eixo Z - azul
            glColor3f(0.0, 0.0, 1.0)
            glVertex3f(0, 0, -z)
            glVertex3f(0, 0, z)

        glEnd()

    def draw_cube(self):
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        glColor3f(*self.point_color)  # Cubo amarelo
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def setVertices(self, vertex):
        self.vertices = vertex

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
     
    def resetCamera(self):
        self.position = [500,500,500]
        
        self.redraw()
        
    def turnShowAxis(self):
        if(self.showAxis):
            self.showAxis = False
        else:
            self.showAxis = True
        
        self.redraw()
        
    def turnRecorte(self):
        pass
        
    def turnCohensuterland(self):
        pass     

    def clearScreen(self):
        self.vertices = [
            [0, 0, 0],
            [ 100, 0, 0],
            [ 100,  100, 0],
            [0,  100, 0],
            [0, 0,  100],
            [ 100, 0,  100],
            [ 100,  100,  100],
            [0,  100,  100],
        ]
        
        self.redraw()