import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import time

# Simula uma onda de batimento cardíaco (curva ECG simplificada)
def heartbeat_wave(x):
    return (
        math.exp(-((x - 2)**2) * 10) * 0.8
        - math.exp(-((x - 1.5)**2) * 30) * 0.2
        - math.exp(-((x - 2.5)**2) * 30) * 0.3
        + math.exp(-((x - 3.5)**2) * 10) * 0.15
    )

def draw_ecg(buffer):
    glColor3f(0, 1, 0)
    glBegin(GL_LINE_STRIP)
    for i, y in enumerate(buffer):
        x = i / len(buffer) * 2 - 1  # -1 a 1
        glVertex2f(x, y)
    glEnd()

def main():
    pygame.init()
    display = (800, 400)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0, 0, 0, 1)
    gluOrtho2D(-1, 1, -1, 1)

    ecg_buffer = []
    t = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t += 0.02
        y = heartbeat_wave(t % 5)

        ecg_buffer.append(y)
        if len(ecg_buffer) > 500:
            ecg_buffer.pop(0)

        glClear(GL_COLOR_BUFFER_BIT)
        draw_ecg(ecg_buffer)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()