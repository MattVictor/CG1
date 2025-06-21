from tkinter import *
from tkinter import ttk
from customtkinter import CTk
from Frames.Frame2D import GLUTFrame2D
from Frames.Frame3D import GLUTFrame3D
from Frames.ecg import ECGFrame
from Forms.Reta import Reta
from Forms.Circunferencia import Circunferencia
from Forms.PoligonoRegular import Quadrado
from Transform.Transform2D import Transform2D
from Transform.Transform3D import Transform3D

quadradoBase = [(50,50),
                (250,150),
                (200,250),
                (0,150)]

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
        print(widget)
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

        self.root = CTk()
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
        filemenu.add_command(label='2D', command= lambda: [self.changeFrameType(0)])
        filemenu.add_command(label='3D', command= lambda: [self.changeFrameType(1)])
        filemenu.add_command(label='ECG', command= lambda: [self.changeFrameType(2)])
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
        
    def changeFrameType(self, opt):
        if(opt == 0):
            self.glFrame = GLUTFrame2D(self.root,width=self.window_width,height=self.window_height,forma=self.reta)
        elif(opt == 1):
            self.glFrame = GLUTFrame3D(self.root,width=self.window_width,height=self.window_height,forma=self.reta)
        elif(opt == 2):
            self.glFrame = ECGFrame(self.root, width=800, height=680)
            
        self.glFrame.place(x=350,y=10)
        
    def shortcut(self):
        self.quadrado.setPoints(quadradoBase)
        self.glFrame3D.setVertices(cuboBase)
        self.transform2D.resetExplanationText()
        self.transform3D.resetExplanationText()
        
        LIMPA_CT([self.processoDeTrasform])
Main()