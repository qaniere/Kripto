import time
import random
from tkinter import *

fen = Tk()
fen.geometry("700x500")
fen.title("Chat Python RSA")
fen.configure(bg="#60a3bc")

filMessages = Listbox(fen, width="100")
filMessages.pack()

entre = Entry(fen)
entre.pack()

def envoyer():
    print(entre.get())

envoyer = Button(fen, text="Envoyer", command=envoyer)
envoyer.pack()

fen.mainloop()