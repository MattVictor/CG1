import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
import numpy as np

class MyOpenGLFrame(OpenGLFrame):
    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-400, 400, -400, 400, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.square = np.array([
            [100, 100],
            [200, 100],
            [200, 200],
            [100, 200]
        ], dtype=float)

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # Lista de pontos clicados
        self.clicked_points = []

        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_click)  # Captura o clique do mouse

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        glViewport(0, 0, self.width, self.height)
        self.after_idle(self.redraw)

    def on_click(self, event):
        """Captura clique e converte para coordenadas do mundo"""
        screen_x = event.x
        screen_y = event.y

        # Conversão para mundo
        world_x = (screen_x / self.width) * 800 - 400
        world_y = (1 - (screen_y / self.height)) * 800 - 400

        print(f"\nClique na tela:")
        print(f"  Posição tela: ({screen_x}, {screen_y})")
        print(f"  Coordenada mundo: ({world_x:.2f}, {world_y:.2f})")

        # Adiciona o ponto
        self.clicked_points.append((world_x, world_y))
        self.after_idle(self.redraw)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # --- Eixos ---
        glLineWidth(1)
        glColor3f(1.0, 0.0, 0.0)  # vermelho
        glBegin(GL_LINES)
        glVertex2f(-400, 0)
        glVertex2f(400, 0)
        glEnd()

        glColor3f(0.0, 1.0, 0.0)  # verde
        glBegin(GL_LINES)
        glVertex2f(0, -400)
        glVertex2f(0, 400)
        glEnd()

        # --- Quadrado ---
        glColor3f(0.0, 0.0, 1.0)  # azul
        glBegin(GL_QUADS)
        for x, y in self.square:
            glVertex2f(x, y)
        glEnd()

        # --- Pontos clicados ---
        glPointSize(8)
        glColor3f(1.0, 0.0, 1.0)  # rosa
        glBegin(GL_POINTS)
        for x, y in self.clicked_points:
            print(x,y)
            glVertex2f(x, y)
        glEnd()

        glFlush()

    def reflect_x(self):
        """Reflexão no eixo X"""
        print("\n>>> Reflexão no eixo X")
        self.square[:, 1] *= -1
        self.after_idle(self.redraw)

    def reflect_y(self):
        """Reflexão no eixo Y"""
        print("\n>>> Reflexão no eixo Y")
        self.square[:, 0] *= -1
        self.after_idle(self.redraw)

def main():
    root = tk.Tk()
    root.title("Reflexão de Quadrado - OpenGL + Tkinter")

    # Frame do OpenGL
    frame = MyOpenGLFrame(root, width=800, height=800)
    frame.place(x=200, y=0, width=800, height=800)

    # Botão de reflexão no eixo X
    btn_reflect_x = tk.Button(root, text="Refletir no eixo X", command=lambda: [frame.reflect_x(), frame.redraw()])
    btn_reflect_x.place(x=0, y=100, width=150, height=30)

    # Botão de reflexão no eixo Y
    btn_reflect_y = tk.Button(root, text="Refletir no eixo Y", command= lambda: [frame.reflect_y(), frame.redraw()])
    btn_reflect_y.place(x=0, y=200, width=150, height=30)

    # Ajuste tamanho da janela
    root.geometry("1000x1000")
    root.resizable(False, False)

    root.mainloop()

if __name__ == "__main__":
    main()
