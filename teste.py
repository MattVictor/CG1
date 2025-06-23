from customtkinter import *
from customtkinter import CTkFont

root = CTk()
root.title('Font Families')
fonts=list(CTkFont.families())
fonts.sort()

def populate(frame):
    '''Put in the fonts'''
    listnumber = 1
    for i, item in enumerate(fonts):
        label = "listlabel" + str(listnumber)
        label = CTkLabel(frame,text=item,font=(item, 16))
        label.grid(row=i)
        label.bind("<Button-1>",lambda e,item=item:copy_to_clipboard(item))
        listnumber += 1

def copy_to_clipboard(item):
    root.clipboard_clear()
    root.clipboard_append("font=('" + item.lstrip('@') + "', 12)")

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = CTkCanvas(root, borderwidth=0, background="#ffffff")
frame = CTkFrame(canvas, background="#ffffff")
vsb = CTkScrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

populate(frame)

root.mainloop()