from tkinter import *
from tkinter import ttk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from Reta import Reta
from Circunferencia import Circunferencia
from PoligonoRegular import Quadrado
from Transform2D import Transform2D
from Transform3D import Transform3D

quadradoBase = [(100,100),
                (200,100),
                (200,200),
                (100,200)]

cuboBase = [
            [0, 0, 0],
            [ 100, 0, 0],
            [ 100,  100, 0],
            [0,  100, 0],
            [0, 0,  100],
            [ 100, 0,  100],
            [ 100,  100,  100],
            [0,  100,  100],
        ]

def LIMPA_CT(array):
    for objeto in array:
        if isinstance(objeto,Text):
            objeto.delete("1.0","end")
        else:
            objeto.delete(0,END)
            
def insertText(widget=Text, text=str):
    widget.insert(END, text)

def limpa_frame(frame:Widget):
    for widget in frame.winfo_children():
        widget.place_forget()

def insertDataTreeview(tree=ttk.Treeview, data=[]):
    tree.delete(*tree.get_children())
    
    for x, y in data:
        tree.insert(parent='', index='end', text='', values=(x,y))

def VALIDAR_FLOAT(text):
    if text == '': return True
    try:
        value = float(text)
    except ValueError:
        return False
    return 0<=value

class GLUTFrame2D(OpenGLFrame):
    def __init__(self, master, forma, **kwargs):
        super().__init__(master,**kwargs)
        
        self.bind("<Button>", self.mouseClick)
        
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
        glPointSize(1)  # Tamanho dos pontos
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-400, 400, -400, 400, -1, 1)  # Mantém coordenadas normalizadas
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.redraw()
        
    def redraw(self):
        """ Função para desenhar os pontos na tela """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GL_PIXEL = GL_POINTS
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

        # Desenha os pontos clicados
        glColor3f(*self.point_color)

        # Primitiva
        glBegin(GL_PIXEL)
        for x, y in self.clicked_points:
            glVertex2f(x, y)
        glEnd()

        self.tkSwapBuffers()
        
    def dadosFornecidos(self,x1=0,y1=0,x2=False,y2=False,raio=False,figura=False):
        if raio:
            clicked_points = self.forma.drawFunction(self.clicked_points_line,[x1,y1], raio)
        if figura:
            clicked_points = figura.drawPoints()
        else:
            clicked_points = self.forma.drawFunction([x1,y1,x2,y2])
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []

        for x1, y1 in clicked_points:
            self.mostrar_coordenadas([self.width,self.height],state=0,coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
        
        self.redraw()
    
    def mouseClick(self, event):
        """ Captura cliques do mouse e converte para coordenadas normalizadas"""
        window_width = self.width
        window_height = self.height

        x,y = event.x, event.y
        
        if event.num == 1:
            # Converte as coordenadas da tela para coordenadas normalizadas OpenGL
            self.normalizeAndAddPoints(event.x,event.y)
            self.mostrar_coordenadas(window=[int(window_width),int(window_height)],state=0,coords=[x,y])
        elif event.num == 3:
            # Desenha uma linha nos pontos escolhidos
            
            self.clicked_points_line.append((x / self.width) * 800 - 400)
            self.clicked_points_line.append((1 - (y / self.height)) * 800 - 400)
            
            if(len(self.clicked_points_line) == 4):
                self.algoritmoDoisPontos()
                
                self.clicked_points_line = []
        
        self.redraw()
        
    def algoritmoDoisPontos(self):
        clicked_points = self.forma.drawFunction(self.clicked_points_line)
        
        self.coordenadas_Mundo = []
        self.coordenadas_OpenGL = []
        self.coordenadas_Tela = []

        for x1, y1 in clicked_points:
            self.mostrar_coordenadas([self.width,self.height],state=0,coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
            
    def normalizeAndAddPoints(self,x,y):
        normalized_x = x
        normalized_y = y
        
        # Armazena o ponto clicado
        self.coordenadas_OpenGL.append((f"{(normalized_x/400):.3f}",f"{(normalized_y/400):.3f}"))
        self.clicked_points.append((normalized_x, normalized_y))
        
    def converter_coordenadas_mouse(self,windowSize, coords):

        mouse_x = int(coords[0])
        mouse_y = int(coords[1])
        
        mouseMin_x = 0
        mouseMax_x = windowSize[0]
        
        mouseMin_y = windowSize[1]
        mouseMax_y = 0

        glMin = -1
        glMax = 1

        point_x = ((mouse_x - mouseMin_x) * (glMax - glMin) / (mouseMax_x - mouseMin_x)) + glMin
        point_y = ((mouse_y - mouseMin_y) * (glMax - glMin) / (mouseMax_y - mouseMin_y)) + glMin

        return [point_x, point_y]

    def converter_coordenadas_tela(self,screenSize, coords):

        screen_x = coords[0]
        screen_y = coords[1]
        
        screenMin_x = 0
        screenMax_x = screenSize[0]
        
        screenMin_y = screenSize[1]
        screenMax_y = 0

        glMin = -1
        glMax = 1
        
        point_x = (screen_x + 1) / 2 * screenMax_x
        point_y = (-screen_y + 1) / 2 * screenMin_y

        return [f"{point_x:.3f}", f"{point_y:.3f}"]

    def mostrar_coordenadas(self,window,state,coords):
        normalized_x, normalized_y = self.converter_coordenadas_mouse([window[0],window[1]],coords)
        coord_tela = self.converter_coordenadas_tela([1920,1080],[normalized_x,normalized_y])

        self.coordenadas_Mundo.append((coords[0],coords[1]))
        self.coordenadas_Tela.append((round(coords[0]+400),round((coords[1]-400)*-1)))
    
    def setForma(self,novaForma):
        self.forma = novaForma
    
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
        
    def clearScreen(self):
        self.clicked_points = []
        self.redraw()

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
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45,1.0,0.1,1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.redraw()
        
    def redraw(self):
        """ Função para desenhar os pontos na tela """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(self.position[0], self.position[1], self.position[1], 0, 0, 0, 0, 1, 0)

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

class Main():
    def __init__(self):
        self.reta = Reta()
        self.circunferencia = Circunferencia()
        self.quadrado = Quadrado()
        self.transform2D = Transform2D()
        self.transform3D = Transform3D()

        # Tamanho inicial do GL
        self.window_width = 800
        self.window_height = 680

        # Tamanho da janela TK
        self.tkwindow_width = 1200
        self.tkwindow_height = 700

        self.root = Tk()
        self.root.geometry(f"{self.tkwindow_width}x{self.tkwindow_height}")
        self.root.resizable = False
        self.root.title("Computação Gráfica")

        self.formaFrame = Frame(self.root,bg="gray", width=300,height=680)
        self.formaFrame.place(x=25,y=10)
                
        self.VALIDAÇÃO_FLOAT()
                
        self.generateWidgets()
        
        self.frameReta()
        
        self.root.mainloop()
        
    def generateWidgets(self):
        self.glFrame = GLUTFrame2D(self.root,width=self.window_width,height=self.window_height,forma=self.reta)
        self.glFrame3D = GLUTFrame3D(self.root,width=self.window_width,height=self.window_height,forma=self.reta)
        self.glFrame.place(x=350,y=10)

        self.labelForma = Label(self.formaFrame, text="RETA", bg="grey", font=("Segoe UI Black", 17))
        self.processoString = ""

        #Explicações
        self.processoDeTrasform = Text(self.formaFrame, font=("Segoe UI Black", 13))
        
        #Criando Menus
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label='Menu', menu=filemenu)
        filemenu.add_command(label='2D', command= lambda: [self.glFrame3D.place_forget(), self.glFrame.place(x=350,y=10)])
        filemenu.add_command(label='3D', command= lambda: [self.glFrame.place_forget(), self.glFrame3D.place(x=350,y=10)])
        filemenu.add_separator()
        filemenu.add_command(label='Limpar GL', command= lambda: [self.glFrame.clearScreen()])
        filemenu.add_command(label='Inverter Cores', command=lambda: [self.glFrame.invertColors(), self.glFrame3D.invertColors()])
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.root.quit)
        formas = Menu(self.menu)
        self.menu.add_cascade(label='Formas', menu=formas)
        formas.add_command(label='Reta', command= lambda: [self.glFrame.setForma(self.reta),
                                                           limpa_frame(self.formaFrame), 
                                                           self.frameReta()])
        formas.add_command(label="Circunferência", command= lambda: [self.glFrame.setForma(self.circunferencia), 
                                                                     limpa_frame(self.formaFrame), 
                                                                     self.frameCircunferencia()])
        
        Graphic2D = Menu(self.menu)
        self.menu.add_cascade(label='Algoritmo', menu=Graphic2D)
        Graphic2D.add_command(label='DDA', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        Graphic2D.add_command(label="Ponto Medio", command=lambda:[self.reta.setAlgoritmo(self.reta.pontoMedio)])
        Graphic2D.add_separator()
        Graphic2D.add_command(label='Equação Explicita', command=lambda:[self.circunferencia.setAlgoritmo(self.circunferencia.metodo_equacao_explicita)])
        Graphic2D.add_command(label='Ponto Medio', command=lambda:[self.circunferencia.setAlgoritmo(self.circunferencia.pontoMedio)])
        Graphic2D.add_command(label='Metodo Polinomial', command=lambda:[self.circunferencia.setAlgoritmo(self.circunferencia.metodo_polinomial)])
        Graphic2D.add_command(label='Metodo Trigonometrico', command=lambda:[self.circunferencia.setAlgoritmo(self.circunferencia.metodo_trigonometrico)])
        
        transformacoes2D = Menu(self.menu)
        self.menu.add_cascade(label='Transformações 2D', menu=transformacoes2D)
        transformacoes2D.add_command(label='Translação', command=lambda:[limpa_frame(self.formaFrame), 
                                                                        self.Transformation2DFrame(0, "TRANSLAÇÃO")])
        transformacoes2D.add_command(label='Escala', command=lambda:[limpa_frame(self.formaFrame), 
                                                                        self.Transformation2DFrame(1, "ESCALA")])
        transformacoes2D.add_command(label='Rotação', command=lambda:[limpa_frame(self.formaFrame), 
                                                                        self.Transformation2DFrame(2,"ROTAÇÃO")])
        transformacoes2D.add_separator()
        transformacoes2D.add_command(label='Reflexão', command=lambda:[limpa_frame(self.formaFrame), 
                                                                        self.Transformation2DFrame(3, "REFLEXÃO")])
        transformacoes2D.add_command(label='Cisalhamento', command=lambda:[limpa_frame(self.formaFrame), 
                                                                        self.Transformation2DFrame(4, "CISALHAMENTO")])
        
        transformacoes3D = Menu(self.menu)
        self.menu.add_cascade(label='Transformações 3D', menu=transformacoes3D)
        transformacoes3D.add_command(label='Translação', command=lambda:[limpa_frame(self.formaFrame),
                                                                         self.Transformation3DFrame(0, "TRANSLAÇÃO")])
        transformacoes3D.add_command(label='Escala', command=lambda:[limpa_frame(self.formaFrame),
                                                                         self.Transformation3DFrame(1, "ESCALA")])
        transformacoes3D.add_command(label='Rotação', command=lambda:[limpa_frame(self.formaFrame),
                                                                         self.Transformation3DFrame(2, "ROTAÇÃO")])
        transformacoes3D.add_separator()
        transformacoes3D.add_command(label='Reflexão', command=lambda:[limpa_frame(self.formaFrame),
                                                                         self.Transformation3DFrame(3, "REFLEXÃO")])
        transformacoes3D.add_command(label='Cisalhamento', command=lambda:[limpa_frame(self.formaFrame),
                                                                         self.Transformation3DFrame(4, "CISALHAMENTO")])
        
        #Widgets da Reta
        valorX1Reta = IntVar()
        valorY1Reta = IntVar()
        valorX2Reta = IntVar()
        valorY2Reta = IntVar()
        
        self.labelX1Reta = Label(self.formaFrame,text="X1", bg="grey", font=("Segoe UI Black", 17))
        self.entryX1Reta = Entry(self.formaFrame,textvariable=valorX1Reta, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelY1Reta = Label(self.formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Reta = Entry(self.formaFrame,textvariable=valorY1Reta, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelX2Reta = Label(self.formaFrame,text="X2", bg="grey", font=("Segoe UI Black", 17))
        self.entryX2Reta = Entry(self.formaFrame,textvariable=valorX2Reta, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelY2Reta = Label(self.formaFrame,text="Y2", bg="grey", font=("Segoe UI Black", 17))
        self.entryY2Reta = Entry(self.formaFrame,textvariable=valorY2Reta, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.buttonDesenharReta = Button(self.formaFrame, text="Desenhar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame.dadosFornecidos(x1=int(self.entryX1Reta.get()),
                                         y1=int(self.entryY1Reta.get()),
                                         x2=int(self.entryX2Reta.get()),
                                         y2=int(self.entryY2Reta.get())),
            LIMPA_CT([self.entryX1Reta,self.entryY1Reta,self.entryX2Reta,self.entryY2Reta])
        ])
        
        #Widgets da Circunferencia       
        valorX1Circ = IntVar()
        valorY1Circ = IntVar()
        
        valorRaio = IntVar()
        
        self.labelX1Circ = Label(self.formaFrame,text="X1", bg="grey", font=("Segoe UI Black", 17))
        self.entryX1Circ = Entry(self.formaFrame,textvariable=valorX1Circ, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelY1Circ = Label(self.formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Circ = Entry(self.formaFrame,textvariable=valorY1Circ, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelRaioCirc = Label(self.formaFrame,text="Raio", bg="grey", font=("Segoe UI Black", 17))
        self.entryRaioCirc = Entry(self.formaFrame,textvariable=valorRaio, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.buttonDesenharCirc = Button(self.formaFrame, text="Desenhar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame.dadosFornecidos(x1=int(self.entryX1Circ.get()),
                                         y1=int(self.entryY1Circ.get()),
                                         raio=int(self.entryRaioCirc.get())),
            LIMPA_CT([self.entryX1Circ,self.entryY1Circ,self.entryRaioCirc])
        ])
        
        #Página das Transformações 2D
        valorXTrans = IntVar()
        valorYTrans = IntVar()
        valorRotacao = IntVar()
        
        self.labelX1Trans = Label(self.formaFrame,text="X", bg="grey", font=("Segoe UI Black", 17))
        self.entryX1Trans = Entry(self.formaFrame,textvariable=valorXTrans, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelY1Trans = Label(self.formaFrame,text="Y", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Trans = Entry(self.formaFrame,textvariable=valorYTrans, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelRotacao = Label(self.formaFrame,text="Angulo", bg="grey", font=("Segoe UI Black", 17))
        self.entryRotacao = Entry(self.formaFrame,textvariable=valorRotacao, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        #Página das Transformações 3D
        valorXTrans3D = IntVar()
        valorYTrans3D = IntVar()
        valorZTrans3D = IntVar()
        
        self.labelX1Trans3D = Label(self.formaFrame,text="X", bg="grey", font=("Segoe UI Black", 17))
        self.entryX1Trans3D = Entry(self.formaFrame,textvariable=valorXTrans3D, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelY1Trans3D = Label(self.formaFrame,text="Y", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Trans3D = Entry(self.formaFrame,textvariable=valorYTrans3D, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        self.labelZ1Trans3D = Label(self.formaFrame,text="Z", bg="grey", font=("Segoe UI Black", 17))
        self.entryZ1Trans3D = Entry(self.formaFrame,textvariable=valorZTrans3D, validatecommand=self.vald2, font=("Segoe UI Black", 17))
        
        #Botão de Desenhar o quadrado
        self.buttonDesenharQuadrado = Button(self.formaFrame, text="Desenhar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame.dadosFornecidos(figura=self.quadrado)
        ])
        
        #Botões das transformações 2D
        self.buttonTranslation = Button(self.formaFrame, text="Transladar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.transposition(self.quadrado.getPoints(), [int(self.entryX1Trans.get()),int(self.entryY1Trans.get())])),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
        
        self.buttonScale = Button(self.formaFrame, text="Escalar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.scale(self.quadrado.getPoints(), [int(self.entryX1Trans.get()),int(self.entryY1Trans.get())])),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
        
        self.buttonRotation = Button(self.formaFrame, text="Rotacionar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.rotation(self.quadrado.getPoints(), 
                                                         int(self.entryRotacao.get()),
                                                         int(self.entryY1Trans.get()),
                                                         int(self.entryY1Trans.get()))),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
        
        self.buttonReflexX = Button(self.formaFrame, text="em X", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.reflectionX(self.quadrado.getPoints())),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
                
        self.buttonReflexY = Button(self.formaFrame, text="em Y", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.reflectionY(self.quadrado.getPoints())),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
        
        self.buttonSchear = Button(self.formaFrame, text="Cisalhamento", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.quadrado.setPoints(self.transform2D.schear(self.quadrado.getPoints(),x=float(self.entryX1Trans.get()),y=float(self.entryY1Trans.get()))),
            self.glFrame.clearScreen(),
            self.glFrame.dadosFornecidos(figura=self.quadrado),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform2D.getExplanationText())
        ])
        
        #Botões das transformações 3d
        self.buttonTranslation3D = Button(self.formaFrame, text="Transladar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.transposition(self.glFrame3D.vertices, 
                                                              [int(self.entryX1Trans3D.get()),
                                                               int(self.entryY1Trans3D.get()),
                                                               int(self.entryZ1Trans3D.get())])),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        self.buttonScale3D = Button(self.formaFrame, text="Escalar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.scale(self.glFrame3D.vertices, 
                                                              [int(self.entryX1Trans3D.get()),
                                                               int(self.entryY1Trans3D.get()),
                                                               int(self.entryZ1Trans3D.get())])),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
                
        self.buttonRotation3D = Button(self.formaFrame, text="Rotacionar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.rotation(self.glFrame3D.vertices, 
            int(self.entryX1Trans3D.get()),int(self.entryY1Trans3D.get()),int(self.entryZ1Trans3D.get()))),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        self.buttonReflexXY = Button(self.formaFrame, text="XY", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.reflectionXY(self.glFrame3D.vertices)),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        self.buttonReflexXZ = Button(self.formaFrame, text="XZ", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda: [
            self.glFrame3D.setVertices(self.transform3D.reflectionXZ(self.glFrame3D.vertices)),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        self.buttonReflexYZ = Button(self.formaFrame, text="YZ", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.reflectionYZ(self.glFrame3D.vertices)),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        self.buttonSchear3D = Button(self.formaFrame, text="Cisalhar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame3D.setVertices(self.transform3D.schear(self.glFrame3D.vertices, 
            float(self.entryX1Trans3D.get()),float(self.entryY1Trans3D.get()),float(self.entryZ1Trans3D.get()))),
            self.glFrame.clearScreen(),
            self.glFrame3D.redraw(),
            LIMPA_CT([self.processoDeTrasform]),
            insertText(self.processoDeTrasform, self.transform3D.getExplanationText())
        ])
        
        #Treeview das coordenadas (Utilizado por todos os widgets acima)
        self.coordinateFrame = Frame(self.formaFrame, bg="red")
        
        self.treeCoordinates = ttk.Treeview(self.coordinateFrame)
        self.treeCoordinates['columns'] = ("X","Y")
        self.treeCoordinates.column("#0",width=0, minwidth=25)
        self.treeCoordinates.column("X",width=130, minwidth=25)
        self.treeCoordinates.column("Y",width=130, minwidth=25)
        
        self.treeCoordinates.heading("#0",text="")
        self.treeCoordinates.heading("X",text="X")
        self.treeCoordinates.heading("Y",text="Y")
        
        self.treeScroll = Scrollbar(self.treeCoordinates)
        self.treeScroll.pack(side=RIGHT,fill=Y)
        
        self.treeScroll.config(command=self.treeCoordinates.yview)
        
        self.coordMundo = Button(self.formaFrame, text="Mundo", font=("Segoe UI Black", 17),bg="#999999", 
                                 command=lambda: [insertDataTreeview(self.treeCoordinates,self.glFrame.coordenadas_Mundo),
                                                  self.focusTable(self.coordMundo, [self.coordTela, self.coordOpenGL])])
        
        self.coordOpenGL = Button(self.formaFrame, text="OpenGL", font=("Segoe UI Black", 17),bg="#999999", 
                                  command=lambda: [insertDataTreeview(self.treeCoordinates,self.glFrame.coordenadas_OpenGL),
                                                   self.focusTable(self.coordOpenGL, [self.coordMundo, self.coordTela])])
        
        self.coordTela = Button(self.formaFrame, text="Tela", font=("Segoe UI Black", 17),bg="#999999", 
                                command=lambda: [insertDataTreeview(self.treeCoordinates,self.glFrame.coordenadas_Tela), 
                                                 self.focusTable(self.coordTela, [self.coordMundo, self.coordOpenGL])])
        
        #Bidings Adicionais
        self.root.bind("t", lambda _: LIMPA_CT([self.processoDeTrasform]))
        self.root.bind("c", lambda _: self.glFrame.clearScreen(), self.shortcut())
        self.root.bind("r", lambda _: self.glFrame3D.clearScreen())
        self.root.bind("b", lambda _: self.glFrame3D.resetCamera())
        
    def frameReta(self):
        self.labelForma.config(text="RETA")
        self.labelForma.place(relx=0.05,rely=0.02)
        
        self.labelX1Reta.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryX1Reta.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelY1Reta.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryY1Reta.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelX2Reta.place(relx=0.1,rely=0.2,relheight=0.1,relwidth=0.1)
        self.entryX2Reta.place(relx=0.25,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.labelY2Reta.place(relx=0.5,rely=0.2,relheight=0.1,relwidth=0.1)
        self.entryY2Reta.place(relx=0.65,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.buttonDesenharReta.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
        
        self.setTreeViewLoc()
        
    def frameCircunferencia(self):
        self.labelForma.config(text="CIRCUNFERENCIA")
        self.labelForma.place(relx=0.05,rely=0.02)
        
        self.labelX1Circ.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryX1Circ.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelY1Circ.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryY1Circ.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelRaioCirc.place(relx=0.25,rely=0.2,relheight=0.1,relwidth=0.2)
        self.entryRaioCirc.place(relx=0.50,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.buttonDesenharCirc.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
        
        self.setTreeViewLoc()
        
    def Transformation2DFrame(self, typeT, txt):
        self.labelForma.config(text=txt)
        self.labelForma.place(relx=0.05,rely=0.02)
        
        self.buttonDesenharQuadrado.place(relx=0.260,rely=0.25,relheight=0.08,relwidth=0.5)
        
        self.labelX1Trans.place(relx=0.1,rely=0.075,relheight=0.1,relwidth=0.1)
        self.entryX1Trans.place(relx=0.25,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.labelY1Trans.place(relx=0.5,rely=0.075,relheight=0.1,relwidth=0.1)
        self.entryY1Trans.place(relx=0.65,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.labelRotacao.place(relx=0.2,rely=0.150,relheight=0.1,relwidth=0.3)
        self.entryRotacao.place(relx=0.525,rely=0.175,relheight=0.05,relwidth=0.2)
        self.entryRotacao.config(state="disabled")
        
        self.processoDeTrasform.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)
        
        if typeT == 0:
            self.buttonTranslation.place(relx=0.260,rely=0.35,relheight=0.08,relwidth=0.5)
        elif typeT == 1:
            self.buttonScale.place(relx=0.260,rely=0.35,relheight=0.08,relwidth=0.5)
        elif typeT == 2:
            self.buttonRotation.place(relx=0.260,rely=0.35,relheight=0.08,relwidth=0.5)
            self.entryRotacao.config(state='normal')
        elif typeT == 3:
            self.buttonReflexX.place(relx=0.15,rely=0.35,relheight=0.08,relwidth=0.3)
            self.buttonReflexY.place(relx=0.6,rely=0.35,relheight=0.08,relwidth=0.3)
        elif typeT == 4:
            self.buttonSchear.place(relx=0.260,rely=0.35,relheight=0.08,relwidth=0.5)
        
    def Transformation3DFrame(self, typeT, txt):
        self.labelForma.config(text=txt)
        self.labelForma.place(relx=0.05,rely=0.02)
        
        self.labelX1Trans3D.place(relx=0.05,rely=0.075,relheight=0.1,relwidth=0.1)
        self.entryX1Trans3D.place(relx=0.15,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.labelY1Trans3D.place(relx=0.35,rely=0.075,relheight=0.1,relwidth=0.1)
        self.entryY1Trans3D.place(relx=0.45,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.labelZ1Trans3D.place(relx=0.65,rely=0.075,relheight=0.1,relwidth=0.1)
        self.entryZ1Trans3D.place(relx=0.75,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.processoDeTrasform.place(relx=0, rely=0.3, relheight=0.7, relwidth=1)

        if typeT == 0:
            self.buttonTranslation3D.place(relx=0.260,rely=0.2,relheight=0.08,relwidth=0.5)
        elif typeT == 1:
            self.buttonScale3D.place(relx=0.260,rely=0.2,relheight=0.08,relwidth=0.5)
        elif typeT == 2:
            self.buttonRotation3D.place(relx=0.260,rely=0.2,relheight=0.08,relwidth=0.5)
        elif typeT == 3:
            self.buttonReflexXY.place(relx=0.1,rely=0.2,relheight=0.08,relwidth=0.2)
            self.buttonReflexXZ.place(relx=0.4,rely=0.2,relheight=0.08,relwidth=0.2)
            self.buttonReflexYZ.place(relx=0.7,rely=0.2,relheight=0.08,relwidth=0.2)
        elif typeT == 4:
            self.buttonSchear3D.place(relx=0.260,rely=0.2,relheight=0.08,relwidth=0.5)
    
    def setTreeViewLoc(self):
        self.coordinateFrame.place(relx=0.0,rely=0.5,relheight=0.5,relwidth=1)
        
        self.treeCoordinates.place(relx=0.0,rely=0.0,relheight=1,relwidth=1)
        
        self.coordMundo.place(relx=0.0,rely=0.425,relheight=0.08,relwidth=0.34)
        
        self.coordOpenGL.place(relx=0.34,rely=0.425,relheight=0.08,relwidth=0.33)
        
        self.coordTela.place(relx=0.67,rely=0.425,relheight=0.08,relwidth=0.33)
        
    def unbindEvents(self,widget):
        for event in widget.bind():
            widget.unbind(event)
                
    def focusTable(self, focused=Button, unfocus=Button):
        focused.config(bg="#000000", fg="white")
        
        for button in unfocus:
            button.config(bg="#999999", fg="black")
            
    def VALIDAÇÃO_FLOAT(self):
        self.vald2 = (self.root.register(VALIDAR_FLOAT), '%P')

    def treatReturnTransform(self, points, text):
        print(points)

        print(text)

        if len(points) == 4:
            self.quadrado.setPoints(points)
        else:
            self.glFrame3D.setVertices(points)
        self.processoString = text
        
    def shortcut(self):
        self.quadrado.setPoints(quadradoBase)
        self.glFrame3D.setVertices(cuboBase)
        self.transform2D.resetExplanationText()
        self.transform3D.resetExplanationText()
        
        LIMPA_CT([self.processoDeTrasform])
Main()