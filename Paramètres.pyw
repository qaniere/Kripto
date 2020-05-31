import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

ListeParamètres = ["NomUserDéfaut"]
DicoParamètres = {}


def EnregistrerParamètres():

    """ Fonction qui récupére les paramètres dans l'interface et les enregistre dans 
    un fichier """

    global NomUser
    
    ValeurNomUser = NomUser.get()

    if ValeurNomUser != "":
        DicoParamètres["NomUserDéfaut"] = ValeurNomUser
    else:
        DicoParamètres["NomUserDéfaut"] = "Inconnu"

    FichierParamètres = open("Paramètres", "w")

    for Paramètres in ListeParamètres:
    # On récupere chaque paramètres

        FichierParamètres.write(DicoParamètres[Paramètres] + "/-;-/")

    FichierParamètres.close()

    tk.messagebox.showinfo(title="Succès !", message="Vos paramètres ont étés enregistrés avec succès !")


def LectureParamètres():

    """ Fonction qui lit les paramètres sauvegardés sur la machine """

    if os.path.exists("Paramètres"):
    # Si le fichier de paramètre existe déja

        FichierParamètres = open("Paramètres", "r")
        Contenu = FichierParamètres.read()

        ValeursParamètres = Contenu.split("/-;-/")

        for index in range(len(ListeParamètres)):
        # Pour chaque paramètres

            DicoParamètres[ListeParamètres[index]] = ValeursParamètres[index]
    
    else:

        for index in range(len(ListeParamètres)):
        # Pour chaque paramètres

            DicoParamètres[ListeParamètres[index]] = "Inconnu"



def InterfaceParamètres():

    """ Fonction qui affiche les paramètres """

    global NomUser

    fen = tk.Tk()
    fen.geometry("550x460")
    fen.title("Kripto -Paramètres")
    fen.configure(bg="grey")
    fen.resizable(width=False, height=False)
    fen.iconbitmap(bitmap="Médias/Paramètres.ico")
    # Configuraton de la fenêtre
    
    style = ttk.Style(fen)
    style.configure("top.TNotebook")
    # On configure notre fenêtre comme étant un "notebook", le widget qui permet de faire des onglets
    
    notebook = ttk.Notebook(fen)
    
    CadreGénéral = tk.Frame(notebook, bg="grey", width=550, height=460)
    CadreSauvegarde = tk.Frame(notebook, bg="grey", width=550, height=460)
    # On définit les cadres, qui seront en fait les onglets
    
    notebook.add(CadreGénéral, text="Général")
    notebook.add(CadreSauvegarde, text="Son")

    """ Widgets de l'onglet général """

    Label(CadreGénéral, text="Votre nom d'utilisateur par défaut :", bg="grey").grid(pady=15, padx=15, row=0, column=0)
    # On ne stocke pas le label dans une variable car on n'aura pas besoin le réutiliser
    
    NomUser = Entry(CadreGénéral)
    NomUser.grid(row=0, column=1)

    if DicoParamètres["NomUserDéfaut"] != "Inconnu":
        NomUser.insert(0, DicoParamètres["NomUserDéfaut"])

    Enregistrer = Button(CadreGénéral, text="Enregistrer", command=EnregistrerParamètres)
    Enregistrer.grid(pady=15, padx=15, row=1, column=1)

    """ Widgets de l'onglet son """


    notebook.grid(row=0, column=0, sticky="n")
    # On ajout les boutton pour changer d'onglets
    
    fen.mainloop()

if __name__ == "__main__":
# Si le fichier est executé et non importé comme un module

    LectureParamètres()
    InterfaceParamètres()
