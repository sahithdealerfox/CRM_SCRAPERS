from tkinter import *
import tkinter
top = tkinter.Tk()

var = StringVar()
label = Label( top, textvariable =var, relief = RAISED )
var.set("Please enter the Credentials")
label.pack()
top.mainloop()
top.close()