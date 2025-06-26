import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
import numpy as np
import sys

# --- 1. Geração de Dados de ECG ---
def gerar_dados_ecg(num_pontos=2000, frequencia_cardiaca=75):
    """
    Gera uma forma de onda de ECG simulada e mais longa para a animação.
    """
    fs = 1000.0
    ts = 1.0 / fs
    tempo = np.arange(0, num_pontos * ts, ts)

    p = 0.1 * np.exp(-((tempo % (60.0/frequencia_cardiaca) - 0.15)**2) / 0.002)
    q = -0.1 * np.exp(-((tempo % (60.0/frequencia_cardiaca) - 0.2)**2) / 0.001)
    r = 1.0 * np.exp(-((tempo % (60.0/frequencia_cardiaca) - 0.25)**2) / 0.001)
    s = -0.3 * np.exp(-((tempo % (60.0/frequencia_cardiaca) - 0.3)**2) / 0.002)
    t = 0.2 * np.exp(-((tempo % (60.0/frequencia_cardiaca) - 0.45)**2) / 0.01)

    ecg = p + q + r + s + t
    return ecg

# --- 2. Preparação dos Dados ---
dados_ecg = gerar_dados_ecg()
dados_ecg_normalizados = (dados_ecg - np.min(dados_ecg)) / (np.max(dados_ecg) - np.min(dados_ecg)) * 2 - 1
num_pontos = len(dados_ecg_normalizados)
# Mapeia os pontos para a largura da janela
x_coords = np.linspace(-1, 1, num_pontos)

# Variável global para controlar a posição da animação
posicao_atual = 0

# --- 3. Configuração e Renderização com OpenGL ---
def inicializar():
    """Inicializa o ambiente OpenGL."""
    gl.glClearColor(0.0, 0.0, 0.0, 1.0) # Fundo preto
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluOrtho2D(-1.0, 1.0, -1.0, 1.0) # Define as coordenadas da tela

def desenhar_ecg():
    """Função de desenho do OpenGL."""
    global posicao_atual
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    # Define a cor da linha como verde
    gl.glColor3f(0.0, 1.0, 0.0)
    
    # Usa GL_LINE_STRIP para uma linha contínua e animada
    gl.glBegin(gl.GL_LINE_STRIP)
    # Desenha a linha apenas até a posição atual
    for i in range(posicao_atual):
        gl.glVertex2f(x_coords[i], dados_ecg_normalizados[i])
    gl.glEnd()

    glut.glutSwapBuffers()

def atualizar(value):
    """Função para atualizar a animação."""
    global posicao_atual
    
    # Avança a posição da linha
    posicao_atual += 5 # Aumente este valor para uma animação mais rápida
    
    # Reinicia a animação quando chegar ao fim
    if posicao_atual >= num_pontos:
        posicao_atual = 0
        
    glut.PostRedisplay() # Solicita que a janela seja redesenhada
    glut.glutTimerFunc(16, atualizar, 0) # Chama a si mesma a cada ~16ms (~60 FPS)


# --- Função Principal ---
def main():
    """Função principal que configura a janela GLUT."""
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE)
    glut.glutInitWindowSize(800, 400)
    glut.glutInitWindowPosition(100, 100)
    glut.glutCreateWindow(b"Animacao de ECG com Python e OpenGL")
    glut.glutDisplayFunc(desenhar_ecg)
    inicializar()
    glut.glutTimerFunc(16, atualizar, 0) # Inicia o loop de atualização
    glut.glutMainLoop()

if __name__ == "__main__":
    main()