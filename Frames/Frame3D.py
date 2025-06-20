__package__

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class GLUTFrame3D(OpenGLFrame):
    def __init__(self, master, forma, **kwargs):
        super().__init__(master,**kwargs)
        
        self.position = [500,500,500]
        
        self.bind("<MouseWheel>", self.zoom)
        
        master.bind("<Left>", self.rotateLeft)
        master.bind("<Up>", self.rotateUp)
        master.bind("<Down>", self.rotateDown)
        master.bind("<Right>", self.rotateRight)
        
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
        self.forma = forma
    
    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glPointSize(1)
        glEnable(GL_DEPTH_TEST)
        # Tamanho dos pontos
        
        #glViewport(0, 0, 800, 800)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # gluPerspective(45,1.0,0.1,1000.0)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-300, 300, -300, 300, -800, 800)  # projeção ortográfica
        
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
        self.draw_axes()

        # Desenhar o cubo
        self.draw_cube()

        self.tkSwapBuffers()
        
    def draw_axes(self):
        glLineWidth(1.0)
        glBegin(GL_LINES)

        # Eixo X - vermelho
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-400, 0, 0)
        glVertex3f(400, 0, 0)

        # Eixo Y - verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, -400, 0)
        glVertex3f(0, 400, 0)

        # Eixo Z - azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, -400)
        glVertex3f(0, 0, 400)

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
                print(self.vertices[vertex])
                glVertex3fv(self.vertices[vertex])
        glEnd()
    
    def zoom(self,event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            for i in range(len(self.position)):
                self.position[i] += 10
        if event.num == 4 or event.delta == 120:
            for i in range(len(self.position)):
                self.position[i] -= 10
        
        self.redraw()
        
    def rotateUp(self,event):
        self.position[1] += 10
        
        self.redraw()
        
    def rotateDown(self,event):
        self.position[1] -= 10
        
        self.redraw()
        
    def rotateLeft(self,event):
        self.position[0] += 10
        
        self.redraw()
        
    def rotateRight(self,event):
        self.position[0] -= 10
        
        self.redraw()

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