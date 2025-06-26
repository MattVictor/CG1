import customtkinter as ctk
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import math

# --- Constantes de Configuração ---
PONTOS_POR_ARESTA = 50
TAMANHO_PONTO = 2.0
VELOCIDADE_ROTACAO = 0.5

class AppOgl(OpenGLFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vertices = None
        self.arestas = None
        self.angulo_rotacao = 0

    def initgl(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        glPointSize(TAMANHO_PONTO)

        self.vertices = np.array([
            [-1.0, -1.0, -1.0],
            [-1.0, -1.0,  1.0],
            [-1.0,  1.0, -1.0],
            [-1.0,  1.0,  1.0],
            [1.0, -1.0, -1.0],
            [1.0, -1.0,  1.0],
            [1.0,  1.0, -1.0],
            [1.0,  1.0,  1.0]
        ], dtype=np.float32)

        self.arestas = [
            (0, 4), (0, 2), (0, 1), (7, 3), (7, 5), (7, 6),
            (2, 6), (2, 3), (1, 3), (1, 5), (4, 5), (4, 6)
        ]

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Configuração para projeção ortográfica (paralela)
        glOrtho(-2.0, 2.0, -2.0, 2.0, -10.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Rotações para obter a visualização isométrica aproximada
        glRotatef(45, 1, 0, 0)
        glRotatef(45, 0, 1, 0)
        glTranslatef(0, 0, -5)


    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Aplica as rotações para a animação
        glRotatef(self.angulo_rotacao, 1, 1, 0.5)

        glColor3f(1.0, 1.0, 1.0) # Cor dos pontos: branco
        glBegin(GL_POINTS)
        for aresta in self.arestas:
            v_inicio = self.vertices[[aresta [0]]]
            v_fim = self.vertices[[aresta [1]]]
            for i in range(PONTOS_POR_ARESTA):
                t = i / float(PONTOS_POR_ARESTA - 1)
                x = v_inicio [0][0] + t * (v_fim [0][0] - v_inicio [0][0])
                y = v_inicio [0][1] + t * (v_fim [0][1] - v_inicio [0][1])
                z = v_inicio [0][2] + t * (v_fim [0][2] - v_inicio [0][2])
                glVertex3f(x, y, z)
        glEnd()

        self.angulo_rotacao += VELOCIDADE_ROTACAO

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cubo Isométrico com GL_POINTS em CustomTkinter")
        self.geometry("800x600")

        self.ogl_frame = AppOgl(self)
        self.ogl_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    
    app.mainloop()