from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class ECGFrame(OpenGLFrame):
    def __init__(self,master, *args, **kw):
        super().__init__(master,*args, **kw)
        self.Animado = True
        master.after(100, lambda: self.loop())  # aguarda o contexto OpenGL ficar pronto
    
    def initgl(self):
        glViewport(0,0,self.width,self.height)
        glLoadIdentity()
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
        glPointSize(2)  # Tamanho dos pontos
        
        glColor3f(1, 1, 1)
        glLineWidth(1)
        self.ecg_buffer = []
        self.t = 0

    def update(self):
        self.t += 0.02
        y = ECGFrame.heartbeat_wave(self.t % 4.5)
        self.ecg_buffer.append(y)
        if len(self.ecg_buffer) > 300:
            self.ecg_buffer.pop(0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glBegin(GL_POINTS)
        for i, y in enumerate(self.ecg_buffer):
            x = i / 300 * 2 - 1
            glVertex2f(x, y)
        glEnd()

        self.tkSwapBuffers()
        
    # Função da curva de batimento cardíaco
    def heartbeat_wave(x):
        return (
            # Componente 1: A Onda R (o pico principal)
            
            math.exp(-((x - 2)**2) * 10) * 0.8
            # Componente 2: A Onda Q (o primeiro mergulho)
            
            - math.exp(-((x - 1.5)**2) * 30) * 0.2
            # Componente 3: A Onda S (o segundo mergulho)
            
            - math.exp(-((x - 2.5)**2) * 30) * 0.3
            
            # Componente 4: A Onda T (a onda de recuperação)
            + math.exp(-((x - 3.5)**2) * 10) * 0.15
        )
    
    def loop(self):
        self.update()
        self.redraw()
        if(self.Animado):
            self.after(16, lambda: self.loop())  # 60 FPS
        
    def turnShowAxis(self):
        if(self.Animado):
            self.Animado = False
        else:
            self.Animado = True
            self.loop()
           
    def turnRecorte(self):
        pass
        
    def turnCohensuterland(self):
        pass
            
    def clearScreen(self):
        self.ecg_buffer = []
        self.t = 0