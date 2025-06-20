# # import pygame
# # from pygame.locals import *
# # from OpenGL.GL import *
# # from OpenGL.GLU import *
# # import numpy as np
# # import math
# # import time

# # # Simula uma onda de batimento cardíaco (curva ECG simplificada)
# # def heartbeat_wave(x):
# #     return (
# #         math.exp(-((x - 2)**2) * 10) * 0.8
# #         - math.exp(-((x - 1.5)**2) * 30) * 0.2
# #         - math.exp(-((x - 2.5)**2) * 30) * 0.3
# #         + math.exp(-((x - 3.5)**2) * 10) * 0.15
# #     )

# # def draw_ecg(buffer):
# #     glColor3f(0, 1, 0)
# #     glBegin(GL_LINE_STRIP)
# #     for i, y in enumerate(buffer):
# #         x = i / len(buffer) * 2 - 1  # -1 a 1
# #         glVertex2f(x, y)
# #     glEnd()

# # def main():
# #     pygame.init()
# #     display = (800, 400)
# #     pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# #     glClearColor(0, 0, 0, 1)
# #     gluOrtho2D(-1, 1, -1, 1)

# #     ecg_buffer = []
# #     t = 0
# #     clock = pygame.time.Clock()

# #     running = True
# #     while running:
# #         clock.tick(60)
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 running = False

# #         t += 0.02
# #         y = heartbeat_wave(t % 5)

# #         ecg_buffer.append(y)
# #         if len(ecg_buffer) > 500:
# #             ecg_buffer.pop(0)

# #         glClear(GL_COLOR_BUFFER_BIT)
# #         draw_ecg(ecg_buffer)
# #         pygame.display.flip()

# #     pygame.quit()

# # if __name__ == "__main__":
# #     main()
# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *

# def draw_cube():
#     glBegin(GL_QUADS)
#     glColor3f(1, 0, 0)
#     # Frente
#     glVertex3f(-1, -1, 1)
#     glVertex3f(1, -1, 1)
#     glVertex3f(1, 1, 1)
#     glVertex3f(-1, 1, 1)
#     glEnd()

# def setup_isometric_projection():
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(-5, 5, -5, 5, -10, 10)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     glRotatef(35.264, 1, 0, 0)
#     glRotatef(45, 0, 1, 0)

# def main():
#     pygame.init()
#     pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
#     setup_isometric_projection()

#     clock = pygame.time.Clock()
#     running = True
#     while running:
#         clock.tick(60)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 running = False

#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         draw_cube()
#         pygame.display.flip()

#     pygame.quit()

# if __name__ == "__main__":
#     main()

import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class MyOpenGLFrame(OpenGLFrame):
    def initgl(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

        # Projeção ortográfica isométrica
        self.set_isometric_projection(self.width, self.height)

    def reshape(self, width, height):
        # Quando a janela é redimensionada
        self.set_isometric_projection(width, height)

    def set_isometric_projection(self, width, height):
        aspect = width / height if height != 0 else 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Ajuste conforme aspect ratio
        scale = 5
        if aspect >= 1:
            glOrtho(-scale * aspect, scale * aspect, -scale, scale, -20, 20)
        else:
            glOrtho(-scale, scale, -scale / aspect, scale / aspect, -20, 20)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(35.264, 1, 0, 0)
        glRotatef(45, 0, 1, 0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_cube()
        glFlush()

    def draw_cube(self):
        glColor3f(1, 0, 0)
        glBegin(GL_QUADS)
        # Frente
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        glEnd()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Cubo Isométrico")
    app = MyOpenGLFrame(root, width=800, height=600)
    app.pack(fill=tk.BOTH, expand=tk.YES)
    app.after(10, app.animate)  # inicia a animação (redesenho)
    root.mainloop()

