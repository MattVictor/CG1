from tkinter import *
from tkinter import ttk
from OpenGL.GL import *
from OpenGL.GLUT import *
from pyopengltk import OpenGLFrame
from Reta import Reta
from Circunferencia import Circunferencia

coordenadas_Mundo = []
coordenadas_OpenGL = []
coordenadas_Tela = []

def LIMPA_CT(array):
    for objeto in array:
        if isinstance(objeto,Text):
            objeto.delete("1.0",END)
        else:
            objeto.delete(0,END)

#LIMPA O FRAME E COMPORTA CADA ABA
def limpa_frame(frame:Widget):
    for widget in frame.winfo_children():
        widget.place_forget()

def insertDataTreeview(tree=ttk.Treeview, data=[]):
    tree.delete(*tree.get_children())
    
    for x, y in data:
        tree.insert(parent='', index='end', text='', values=(x,y))

def converter_coordenadas_mouse(windowSize, coords):

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

def converter_coordenadas_tela(screenSize, coords):

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

def mostrar_coordenadas(window,state,coords):
    normalized_x, normalized_y = converter_coordenadas_mouse([window[0],window[1]],coords)
    coord_tela = converter_coordenadas_tela([1920,1080],[normalized_x,normalized_y])

    global coordenadas_Mundo
    coordenadas_Mundo.append(converter_coordenadas_tela([1920,1080],[normalized_x,normalized_y]))
    global coordenadas_Tela
    coordenadas_Tela.append((round(coords[0]),round(coords[1])))

class GLUTFrame(OpenGLFrame):
    def __init__(self, master, forma, **kwargs):
        super().__init__(master,**kwargs)
        self.bind("<Button>", self.mouseClick)
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

    def retaDadosFornecidos(self, x1, y1, x2, y2):
        clicked_points = self.forma.drawFunction([x1,y1,x2,y2])
        
                
        global coordenadas_Mundo
        coordenadas_Mundo = []
        global coordenadas_OpenGL
        coordenadas_OpenGL = []
        global coordenadas_Tela
        coordenadas_Tela = []

        for x1, y1 in clicked_points:
            mostrar_coordenadas([window_width,window_height],state=0,coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
        
        self.redraw()
        insertDataTreeview(treeCoordinates,coordenadas_Mundo)
        
    def circunferenciaDadosFornecidos(self,x1,y1,raio):
        clicked_points = self.forma.drawFunction(self.clicked_points_line,[x1,y1], raio)
        
        global coordenadas_Mundo
        coordenadas_Mundo = []
        global coordenadas_OpenGL
        coordenadas_OpenGL = []
        global coordenadas_Tela
        coordenadas_Tela = []

        for x1, y1 in clicked_points:
            mostrar_coordenadas([window_width,window_height],state=0,coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
        
        self.redraw()
        insertDataTreeview(treeCoordinates,coordenadas_Mundo)
    
    def mouseClick(self, event):
        """ Captura cliques do mouse e converte para coordenadas normalizadas"""
        global window_width, window_height

        x,y = event.x, event.y
        
        if event.num == 1:
            # Converte as coordenadas da tela para coordenadas normalizadas OpenGL
            self.normalizeAndAddPoints(event.x,event.y)
            mostrar_coordenadas(window=[int(window_width),int(window_height)],state=0,coords=[x,y])
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
        
        global coordenadas_Mundo
        coordenadas_Mundo = []
        global coordenadas_OpenGL
        coordenadas_OpenGL = []
        global coordenadas_Tela
        coordenadas_Tela = []

        for x1, y1 in clicked_points:
            mostrar_coordenadas([window_width,window_height],state=0,coords=[x1,y1])
            self.normalizeAndAddPoints(x1,y1)
        
        insertDataTreeview(treeCoordinates,coordenadas_Mundo)
            
    def normalizeAndAddPoints(self,x,y):
        normalized_x = (x / window_width) * 2 - 1
        normalized_y = -((y / window_height) * 2 - 1)

        # Armazena o ponto clicado
        global coordenadas_OpenGL
        coordenadas_OpenGL.append((f"{normalized_x:.3f}",f"{normalized_y:.3f}"))
        self.clicked_points.append((normalized_x, normalized_y))
    
    def setForma(self,novaForma):
        self.forma = novaForma
    
    def setAlgoritmo(self,novoAlgoritmo):
        self.forma.setAlgoritmo(novoAlgoritmo)
    
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

# Criação das formas:
reta = Reta()
circunferencia = Circunferencia()

# Tamanho inicial do GL
window_width = 800
window_height = 680

# Tamanho da janela TK
tkwindow_width = 1200
tkwindow_height = 700

root = Tk()
root.geometry(f"{tkwindow_width}x{tkwindow_height}")
root.resizable = False
root.title("Computação Gráfica")

formaFrame = Frame(root,bg="gray", width=300,height=680)
formaFrame.place(x=25,y=10)

def frameReta(glut=GLUTFrame):
    labelForma = Label(formaFrame, text="RETA", bg="grey", font=("Segoe UI Black", 17))
    labelForma.place(relx=0.40,rely=0.01)
    
    valorX1 = IntVar()
    valorY1 = IntVar()
    valorX2 = IntVar()
    valorY2 = IntVar()
    
    labelX1 = Label(formaFrame,text="X1", bg="grey", font=("Segoe UI Black", 17))
    labelX1.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
    entryX1 = Entry(formaFrame,textvariable=valorX1, font=("Segoe UI Black", 17))
    entryX1.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
    
    labelY1 = Label(formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
    labelY1.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
    entryY1 = Entry(formaFrame,textvariable=valorY1, font=("Segoe UI Black", 17))
    entryY1.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
    
    labelX2 = Label(formaFrame,text="X2", bg="grey", font=("Segoe UI Black", 17))
    labelX2.place(relx=0.1,rely=0.2,relheight=0.1,relwidth=0.1)
    entryX2 = Entry(formaFrame,textvariable=valorX2, font=("Segoe UI Black", 17))
    entryX2.place(relx=0.25,rely=0.225,relheight=0.05,relwidth=0.2)
    
    labelY2 = Label(formaFrame,text="Y2", bg="grey", font=("Segoe UI Black", 17))
    labelY2.place(relx=0.5,rely=0.2,relheight=0.1,relwidth=0.1)
    entryY2 = Entry(formaFrame,textvariable=valorY2, font=("Segoe UI Black", 17))
    entryY2.place(relx=0.65,rely=0.225,relheight=0.05,relwidth=0.2)
    
    buttonDesenhar = Button(formaFrame, text="Desenhar", font=("Segoe UI Black", 17), command=lambda:[
        glut.retaDadosFornecidos(int(entryX1.get()),int(entryY1.get()),int(entryX2.get()),int(entryY2.get())),LIMPA_CT([entryX1,entryY1,entryX2,entryY2])
    ])
    buttonDesenhar.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
    
    coordinateFrame = Frame(formaFrame, bg="red")
    coordinateFrame.place(relx=0.0,rely=0.5,relheight=0.5,relwidth=1)
    
    global treeCoordinates
    treeCoordinates = ttk.Treeview(coordinateFrame)
    treeCoordinates['columns'] = ("X","Y")
    treeCoordinates.column("#0",width=0, minwidth=25)
    treeCoordinates.column("X",width=130, minwidth=25)
    treeCoordinates.column("Y",width=130, minwidth=25)
    
    treeCoordinates.heading("#0",text="")
    treeCoordinates.heading("X",text="X")
    treeCoordinates.heading("Y",text="Y")
    
    treeScroll = Scrollbar(treeCoordinates)
    treeScroll.pack(side=RIGHT,fill=Y)
    
    treeScroll.config(command=treeCoordinates.yview)
    
    treeCoordinates.place(relx=0.0,rely=0.0,relheight=1,relwidth=1)
    
    coordMundo = Button(formaFrame, text="Mundo", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_Mundo))
    coordMundo.place(relx=0.0,rely=0.425,relheight=0.08,relwidth=0.34)
    
    coordOpenGL = Button(formaFrame, text="OpenGL", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_OpenGL))
    coordOpenGL.place(relx=0.34,rely=0.425,relheight=0.08,relwidth=0.33)
    
    coordTela = Button(formaFrame, text="Tela", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_Tela))
    coordTela.place(relx=0.67,rely=0.425,relheight=0.08,relwidth=0.33)
    
def frameCircunferencia(glut=GLUTFrame):
    labelForma = Label(formaFrame, text="CIRCUNFERENCIA", bg="grey", font=("Segoe UI Black", 17))
    labelForma.place(relx=0.150,rely=0.01)
    
    valorX1 = IntVar()
    valorY1 = IntVar()
    valorRaio = IntVar()
    
    labelX1 = Label(formaFrame,text="X1", bg="grey", font=("Segoe UI Black", 17))
    labelX1.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.1)
    entryX1 = Entry(formaFrame,textvariable=valorX1, font=("Segoe UI Black", 17))
    entryX1.place(relx=0.25,rely=0.125,relheight=0.05,relwidth=0.2)
    
    labelY1 = Label(formaFrame,text="Y1", bg="grey", font=("Segoe UI Black", 17))
    labelY1.place(relx=0.5,rely=0.1,relheight=0.1,relwidth=0.1)
    entryY1 = Entry(formaFrame,textvariable=valorY1, font=("Segoe UI Black", 17))
    entryY1.place(relx=0.65,rely=0.125,relheight=0.05,relwidth=0.2)
    
    labelRaio = Label(formaFrame,text="Raio", bg="grey", font=("Segoe UI Black", 17))
    labelRaio.place(relx=0.25,rely=0.2,relheight=0.1,relwidth=0.2)
    entryRaio = Entry(formaFrame,textvariable=valorRaio, font=("Segoe UI Black", 17))
    entryRaio.place(relx=0.50,rely=0.225,relheight=0.05,relwidth=0.2)
    
    buttonDesenhar = Button(formaFrame, text="Desenhar", font=("Segoe UI Black", 17), command=lambda:[
        glut.circunferenciaDadosFornecidos(int(entryX1.get()),int(entryY1.get()),int(entryRaio.get())), LIMPA_CT([entryX1,entryY1,entryRaio])
    ])
    buttonDesenhar.place(relx=0.260,rely=0.325,relheight=0.08,relwidth=0.5)
    
    coordinateFrame = Frame(formaFrame, bg="red")
    coordinateFrame.place(relx=0.0,rely=0.5,relheight=0.5,relwidth=1)
    
    treeCoordinates = ttk.Treeview(coordinateFrame)
    treeCoordinates['columns'] = ("X","Y")
    treeCoordinates.column("#0",width=0, minwidth=25)
    treeCoordinates.column("X",width=130, minwidth=25)
    treeCoordinates.column("Y",width=130, minwidth=25)
    
    treeCoordinates.heading("#0",text="")
    treeCoordinates.heading("X",text="X")
    treeCoordinates.heading("Y",text="Y")
    
    treeScroll = Scrollbar(treeCoordinates)
    treeScroll.pack(side=RIGHT,fill=Y)
    
    treeScroll.config(command=treeCoordinates.yview)
    
    treeCoordinates.place(relx=0.0,rely=0.0,relheight=1,relwidth=1)
    
    coordMundo = Button(formaFrame, text="Mundo", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_Mundo))
    coordMundo.place(relx=0.0,rely=0.425,relheight=0.08,relwidth=0.34)
    
    coordOpenGL = Button(formaFrame, text="OpenGL", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_OpenGL))
    coordOpenGL.place(relx=0.34,rely=0.425,relheight=0.08,relwidth=0.33)
    
    coordTela = Button(formaFrame, text="Tela", font=("Segoe UI Black", 17), command=lambda: insertDataTreeview(treeCoordinates,coordenadas_Tela))
    coordTela.place(relx=0.67,rely=0.425,relheight=0.08,relwidth=0.33)
    

glFrame = GLUTFrame(root,width=window_width,height=window_height,forma=reta)
glFrame.place(x=350,y=10)

frameReta(glFrame)

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='Menu', menu=filemenu)
filemenu.add_command(label='Limpar GL', command= lambda: [glFrame.clearScreen()])
filemenu.add_command(label='Inverter Cores', command=lambda: [glFrame.invertColors()])
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
formas = Menu(menu)
menu.add_cascade(label='Formas', menu=formas)
formas.add_command(label='Reta', command= lambda: [glFrame.setForma(reta),limpa_frame(formaFrame), frameReta(glFrame)])
formas.add_command(label="Circunferência", command= lambda: [glFrame.setForma(circunferencia), limpa_frame(formaFrame), frameCircunferencia(glFrame)])
Graphic2D = Menu(menu)
menu.add_cascade(label='Algoritmo', menu=Graphic2D)
Graphic2D.add_command(label='DDA', command=lambda:[reta.setAlgoritmo(reta.DDA)])
Graphic2D.add_command(label="Ponto Medio", command=lambda:[reta.setAlgoritmo(reta.pontoMedio)])
Graphic2D.add_separator()

Graphic2D.add_command(label='Equação Explicita', command=lambda:[circunferencia.setAlgoritmo(circunferencia.metodo_equacao_explicita)])
Graphic2D.add_command(label='Ponto Medio', command=lambda:[circunferencia.setAlgoritmo(circunferencia.pontoMedio)])
Graphic2D.add_command(label='Metodo Polinomial', command=lambda:[circunferencia.setAlgoritmo(circunferencia.metodo_polinomial)])
Graphic2D.add_command(label='Metodo Trigonometrico', command=lambda:[circunferencia.setAlgoritmo(circunferencia.metodo_trigonometrico)])

root.mainloop()