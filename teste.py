from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Mapa de bits 5x3 para dígitos
digit_bitmaps = {
    '0': ["111", "101", "101", "101", "111"],
    '1': ["010", "110", "010", "010", "111"],
    '2': ["111", "001", "111", "100", "111"],
    '3': ["111", "001", "111", "001", "111"],
    '4': ["101", "101", "111", "001", "001"],
    '5': ["111", "100", "111", "001", "111"],
    '6': ["111", "100", "111", "101", "111"],
    '7': ["111", "001", "010", "010", "010"],
    '8': ["111", "101", "111", "101", "111"],
    '9': ["111", "101", "111", "001", "111"],
}

def draw_digit(digit, x, y, size=0.05):
    """Desenha um dígito com GL_POINTS a partir da posição (x, y)."""
    bitmap = digit_bitmaps.get(digit, [])
    for row_idx, row in enumerate(bitmap):
        for col_idx, pixel in enumerate(row):
            if pixel == '1':
                # Inverte a ordem do y para que o topo da matriz esteja em cima
                px = x + col_idx * size
                py = y - row_idx * size
                glVertex2f(px, py)

def draw_string(s, x, y, spacing=0.2):
    """Desenha uma string de números"""
    glBegin(GL_POINTS)
    for i, char in enumerate(s):
        draw_digit(char, x + i * spacing, y)
    glEnd()

# Setup da janela
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

    # Desenhar número na posição (-0.9, 0.5)
    draw_string("1234567890", -0.9, 0.5)

    glFlush()

# Inicialização
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow(b"OpenGL Digits with glVertex2f")
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-1, 1, -1, 1)

glutDisplayFunc(display)
glutMainLoop()
