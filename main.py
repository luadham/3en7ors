from _tkinter import *
from cProfile import label
from cgitb import text
from logging import PlaceHolder
from sqlite3 import Row
from tkinter import *

# This is the root Window
root = Tk()
# create Label
# Add label to screen


def scanButtonOnClick():
    print("hello")


targetLabel = Label(root, text="Target")
targetInput = Entry(root)
scanButton = Button(root, text="Scan Port", command=scanButtonOnClick)

myText = Text(root)
targetLabel.place(x=10, y=13)
targetInput.place(x=80, y=13)
scanButton.place(x=250, y=10)
myText.place(x=20, y=60)
# Title of Window
root.title("3en7ors")
# Size of Window
root.geometry("690x500")
# INIT Window
root.mainloop()
