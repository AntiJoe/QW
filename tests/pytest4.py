# python3

from tkinter import *

root = Tk()


def printName():
    print("Hello Jogy")

bn1 = Button(root, text = "Hello", command = printName)
bn1.pack()

root.mainloop()