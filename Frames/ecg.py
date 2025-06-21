# from OpenGL.GL import *
# from OpenGL.GLU import *
# from pyopengltk import OpenGLFrame
# import numpy as np
# import math
# import time

# class ECG(OpenGLFrame):
#     def __init__(self, *args, **kw):
#         super().__init__(*args, **kw)

#     def initgl(self):
#         glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
#         glPointSize(1)  # Tamanho dos pontos
        
#         glMatrixMode(GL_PROJECTION)
#         glLoadIdentity()
#         glOrtho(-1, 1, -1, 1, -1, 1)  # Mantém coordenadas normalizadas
#         glMatrixMode(GL_MODELVIEW)
#         glLoadIdentity()
        
#         ecg_buffer = []
#         t = 0
#         clock = time.clock()

#         running = True
#         while running:
#             clock.tick(60)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#             t += 0.02
#             y = heartbeat_wave(t % 5)

#             ecg_buffer.append(y)
#             if len(ecg_buffer) > 500:
#                 ecg_buffer.pop(0)

#             glClear(GL_COLOR_BUFFER_BIT)
#             draw_ecg(ecg_buffer)
#             pygame.display.flip()
        
#         self.redraw()

#     # Simula uma onda de batimento cardíaco (curva ECG simplificada)
#     def heartbeat_wave(x):
#         return (
#             math.exp(-((x - 2)**2) * 10) * 0.8
#             - math.exp(-((x - 1.5)**2) * 30) * 0.2
#             - math.exp(-((x - 2.5)**2) * 30) * 0.3
#             + math.exp(-((x - 3.5)**2) * 10) * 0.15
#         )

#     def draw_ecg(buffer):
#         glColor3f(0, 1, 0)
#         glBegin(GL_LINE_STRIP)
#         for i, y in enumerate(buffer):
#             x = i / len(buffer) * 2 - 1  # -1 a 1
#             glVertex2f(x, y)
#         glEnd()

import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class ECGFrame(OpenGLFrame):
    def __init__(self,master, *args, **kw):
        super().__init__(master,*args, **kw)
        master.after(100, lambda: ECGFrame.loop(ecg))  # aguarda o contexto OpenGL ficar pronto
    
    def initgl(self):
        glClearColor(0, 0, 0, 1)
        glColor3f(0, 1, 0)
        glLineWidth(1)
        self.ecg_buffer = []
        self.t = 0

    def update(self):
        self.t += 0.02
        y = ECGFrame.heartbeat_wave(self.t % 5)
        self.ecg_buffer.append(y)
        if len(self.ecg_buffer) > 500:
            self.ecg_buffer.pop(0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glBegin(GL_LINE_STRIP)
        for i, y in enumerate(self.ecg_buffer):
            x = i / 500 * 2 - 1
            glVertex2f(x, y)
        glEnd()

        self.tkSwapBuffers()
        
    # Função da curva de batimento cardíaco
    def heartbeat_wave(x):
        return (
            math.exp(-((x - 2)**2) * 10) * 0.8
            - math.exp(-((x - 1.5)**2) * 30) * 0.2
            - math.exp(-((x - 2.5)**2) * 30) * 0.3
            + math.exp(-((x - 3.5)**2) * 10) * 0.15
        )
    
    def loop(frame):
        frame.update()
        frame.redraw()
        frame.after(16, lambda: ECGFrame.loop(frame))  # 60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ECG com PyOpenGLTk")

    ecg = ECGFrame(root, width=800, height=800)
    ecg.pack(fill=tk.BOTH, expand=True)

    # root.after(100, lambda: loop(ecg))  # aguarda o contexto OpenGL ficar pronto
    root.mainloop()