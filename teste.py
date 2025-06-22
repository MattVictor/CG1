import tkinter as tk

master = tk.Tk()
master.resizable(0, 0)  # prevent resizing
master.wait_visibility()  # wait for the window
master.state('zoomed')  # maximize the window


# this guard clause isn't strictly necessary,
# but it's a 'best practice' kind of thing
if __name__ == '__main__':
    master.mainloop()  # run
