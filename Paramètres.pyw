import tkinter as tk
from tkinter import *
from tkinter import ttk

fen = tk.Tk()
fen.geometry("550x460")
fen.title("Kripto -Paramètres")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
#Configuraton de la fenêtre
 
style = ttk.Style(fen)
style.configure("top.TNotebook")
#On configure notre fenêtre comme étant un "notebook", le widget qui permet de faire des onglets
 
notebook = ttk.Notebook(fen)
 
CadreGénéral = tk.Frame(notebook, bg="grey", width=550, height=460)
CadreSauvegarde = tk.Frame(notebook, bg="grey", width=550, height=460)
#On définit les cadres, qui seront en fait les onglets
 
notebook.add(CadreGénéral, text="Général")
notebook.add(CadreSauvegarde, text="Sauvegarde")

""" Widgets de l'onglets Sauvegarde """

def EnregistrementSauv():

    print(ValeurCase.get())


Explications = Label(CadreSauvegarde, text="Quand les logs sont activés, chaque message envoyé\n\
et reçu est enregistré dans un fichier de sauvegarde chiffré. Vous pourrez lire ce fichier très prochainement.\n\
La clé de chiffrement est le mot de passe ci-dessous, veuillez ne pas le perdre")
Explications.pack()


ValeurCase = tk.BooleanVar() 
ValeurCase.set(False)

ActivationLogs = Checkbutton(CadreSauvegarde, text="Activer les logs", var=ValeurCase, bg="Grey")
ActivationLogs.pack(pady="20")


MotDePasse = Entry(CadreSauvegarde, show="*")
MotDePasse.pack()

Enregistrer = Button(CadreSauvegarde, text="Enregistrer les paramètres", command= EnregistrementSauv)
Enregistrer.pack()

notebook.grid(row=0, column=0, sticky="n")
#On ajout les boutton pour changer d'onglets
 
fen.mainloop()
