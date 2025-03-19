from tkinter import *
from pyopengltk import OpenGLFrame

#Ainda não pronto
# Tamanho inicial da janela
window_width = "1000"
window_height = "700"

root = Tk()
root.geometry(window_width+"x"+window_height)
root.title("Computação Gráfica")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='Menu', menu=filemenu)
filemenu.add_command(label='Limpar GL')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
Graphic2D = Menu(menu)
menu.add_cascade(label='Gráficos 2D', menu=Graphic2D)
Graphic2D.add_command(label='DDA')
Graphic2D.add_command(label="Ponto Medio")
Graphic2D.add_separator()
Graphic2D.add_command(label='Circunferencia', command=root.quit)

Graphics3D = Menu(menu)
menu.add_cascade(label='Gráficos 3D', menu=Graphics3D)
Graphics3D.add_command(label='About')


newFrame = Frame(root, bg="#000000")
newFrame.place(relx=0.1,rely=0.1,relheight=0.8,relwidth=0.8)

root.mainloop()