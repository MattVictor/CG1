from tkinter import *
from tkinter import ttk
from OpenGL.GL import *
from pyopengltk import OpenGLFrame
from Reta import Reta
from Circunferencia import Circunferencia

def LIMPA_CT(array):
    for objeto in array:
        objeto.delete(0,END)

def limpa_frame(frame:Widget):
    for widget in frame.winfo_children():
        widget.place_forget()

def insertDataTreeview(tree=ttk.Treeview, data=[]):
    tree.delete(*tree.get_children())
    
    for x, y in data:
        tree.insert(parent='', index='end', text='', values=(x,y))

class GLUTFrame(OpenGLFrame):
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
    
    def reshape(width, height):
        """ Ajusta a projeção ao redimensionar a janela """
        global window_width, window_height
        window_width = width
        window_height = height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)  # Mantém coordenadas normalizadas
        glMatrixMode(GL_MODELVIEW)
        
    def redraw(self):
        """ Função para desenhar os pontos na tela """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        GL_PIXEL = GL_POINTS
        glLoadIdentity()

        # Desenha os pontos clicados
        glColor3f(*self.point_color)

        # Primitiva
        glBegin(GL_PIXEL)
        for x, y in self.clicked_points:
            glVertex2f(x, y)
        glEnd()

        self.tkSwapBuffers()
        
    def dadosFornecidos(self,x1,y1,x2=False,y2=False,raio=False):
        if raio:
            clicked_points = self.forma.drawFunction(self.clicked_points_line,[x1,y1], raio)
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
            
            self.clicked_points_line.append(x)
            self.clicked_points_line.append(y)
            
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
        normalized_x = (x / self.width) * 2 - 1
        normalized_y = -((y / self.height) * 2 - 1)

        # Armazena o ponto clicado
        self.coordenadas_OpenGL.append((f"{normalized_x:.3f}",f"{normalized_y:.3f}"))
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

        self.coordenadas_Mundo.append(self.converter_coordenadas_tela([1920,1080],[normalized_x,normalized_y]))
        self.coordenadas_Tela.append((round(coords[0]),round(coords[1])))
    
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

class Main():
    def __init__(self):
        self.reta = Reta()
        self.circunferencia = Circunferencia()

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
                
        self.generateWidgets()
        
        self.frameReta()
        
        self.root.mainloop()
        
    def generateWidgets(self):
        self.glFrame = GLUTFrame(self.root,width=self.window_width,height=self.window_height,forma=self.reta)
        self.glFrame.place(x=350,y=10)

        self.labelAlgoritmoUsado = Label(self.formaFrame, text="DDA", bg="grey", font=("Segoe UI Black", 13))

        self.labelForma = Label(self.formaFrame, text="RETA", bg="grey", font=("Segoe UI Black", 17))

        #Criando Menus
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label='Menu', menu=filemenu)
        filemenu.add_command(label='Limpar GL', command= lambda: [self.glFrame.clearScreen()])
        filemenu.add_command(label='Inverter Cores', command=lambda: [self.glFrame.invertColors()])
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
        
        transformacoes = Menu(self.menu)
        self.menu.add_cascade(label='Transformações', menu=transformacoes)
        transformacoes.add_command(label='Translação', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        transformacoes.add_command(label='Escala', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        transformacoes.add_command(label='Rotação', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        transformacoes.add_separator()
        transformacoes.add_command(label='Reflexão', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        transformacoes.add_command(label='Cisalhamento', command=lambda:[self.reta.setAlgoritmo(self.reta.DDA)])
        
        #Widgets da Reta
        valorX1Reta = IntVar()
        valorY1Reta = IntVar()
        valorX2Reta = IntVar()
        valorY2Reta = IntVar()
        
        self.labelX1Reta = Label(self.formaFrame,text="X1", bg="grey", font=("Segoe UI Black", 17))
        self.entryX1Reta = Entry(self.formaFrame,textvariable=valorX1Reta, font=("Segoe UI Black", 17))
        
        self.labelY1Reta = Label(self.formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Reta = Entry(self.formaFrame,textvariable=valorY1Reta, font=("Segoe UI Black", 17))
        
        self.labelX2Reta = Label(self.formaFrame,text="X2", bg="grey", font=("Segoe UI Black", 17))
        self.entryX2Reta = Entry(self.formaFrame,textvariable=valorX2Reta, font=("Segoe UI Black", 17))
        
        self.labelY2Reta = Label(self.formaFrame,text="Y2", bg="grey", font=("Segoe UI Black", 17))
        self.entryY2Reta = Entry(self.formaFrame,textvariable=valorY2Reta, font=("Segoe UI Black", 17))
        
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
        self.entryX1Circ = Entry(self.formaFrame,textvariable=valorX1Circ, font=("Segoe UI Black", 17))
        
        self.labelY1Circ = Label(self.formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
        self.entryY1Circ = Entry(self.formaFrame,textvariable=valorY1Circ, font=("Segoe UI Black", 17))
        
        self.labelRaioCirc = Label(self.formaFrame,text="Raio", bg="grey", font=("Segoe UI Black", 17))
        self.entryRaioCirc = Entry(self.formaFrame,textvariable=valorRaio, font=("Segoe UI Black", 17))
        
        self.buttonDesenharCirc = Button(self.formaFrame, text="Desenhar", font=("Segoe UI Black", 17),
                                         bg='#000000',fg="white", command=lambda:[
            self.glFrame.dadosFornecidos(x1=int(self.entryX1Circ.get()),
                                         y1=int(self.entryY1Circ.get()),
                                         raio=int(self.entryRaioCirc.get())),
            LIMPA_CT([self.entryX1Circ,self.entryY1Circ,self.entryRaioCirc])
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
        self.root.bind("r", lambda _: self.glFrame.clearScreen())
        
    def frameReta(self):
        self.labelAlgoritmoUsado.place(relx=0.01,rely=0.01)
        
        self.labelForma.config(text="RETA")
        self.labelForma.place(relx=0.40,rely=0.05)
        
        self.labelX1Reta.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryX1Reta.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelY1Reta.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryY1Reta.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelX2Reta.place(relx=0.1,rely=0.2,relheight=0.1,relwidth=0.1)
        self.entryX2Reta.place(relx=0.25,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.labelY2Reta.place(relx=0.5,rely=0.2,relheight=0.1,relwidth=0.1)
        self.entryY2Reta.place(relx=0.65,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.buttonDesenharReta.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
        
        # self.unbindEvents(self.formaFrame)
            
        # self.formaFrame.bind("<Enter>", func=lambda _: self.glFrame.dadosFornecidos(
        #     x1=int(self.entryX1Reta.get()),
        #     y1=int(self.entryY1Reta.get()),
        #                                  x2=int(self.entryX2Reta.get()),
        #                                  y2=int(self.entryY2Reta.get())))
        
        self.setTreeViewLoc()
        
    def frameCircunferencia(self):
        self.labelAlgoritmoUsado.place(relx=0.01,rely=0.01)
        
        self.labelForma.config(text="CIRCUNFERENCIA")
        self.labelForma.place(relx=0.150,rely=0.05)
        
        self.labelX1Circ.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryX1Circ.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelY1Circ.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
        self.entryY1Circ.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
        
        self.labelRaioCirc.place(relx=0.25,rely=0.2,relheight=0.1,relwidth=0.2)
        self.entryRaioCirc.place(relx=0.50,rely=0.225,relheight=0.05,relwidth=0.2)
        
        self.buttonDesenharCirc.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
        
        # self.unbindEvents(self.formaFrame)
        
        # self.formaFrame.bind("<Enter>", lambda _: self.glFrame.dadosFornecidos(x1=int(self.entryX1Circ.get()),
        #                                  y1=int(self.entryY1Circ.get()),
        #                                  raio=int(self.entryRaioCirc.get())))
        
        self.setTreeViewLoc()
    
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

Main()