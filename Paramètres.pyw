import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from Sauvegarde import *
from tkinter import messagebox

ListeParamètres = ["NomUserDéfaut", "Sauvegarde"]
DicoParamètres = {}


def EnregistrerParamètres():

    """ Fonction qui récupére les paramètres dans l'interface et les enregistre dans 
    un fichier """

    global DicoParamètres, fen, NomUser, ValeurCase

    # Récupération du nom d'utilisateur
    
    ValeurNomUser = NomUser.get()

    if ValeurNomUser != "":
        DicoParamètres["NomUserDéfaut"] = ValeurNomUser
    else:
        DicoParamètres["NomUserDéfaut"] = "Inconnu"

    #####

    # Récupération de l'activation de la sauvegarde

    if ValeurCase.get() == True:

        DicoParamètres["Sauvegarde"] = "Activée"
    
    else: 
        DicoParamètres["Sauvegarde"] = "Non"
    

    FichierParamètres = open("Paramètres", "w", encoding="utf-8")

    for Paramètre in ListeParamètres:
    # On récupere chaque paramètres

        FichierParamètres.write(DicoParamètres[Paramètre] + "/-;-/")
        # On utilise un séparateur peu commun pour éviter tout problème

    FichierParamètres.close()

    fen.withdraw()
    tk.messagebox.showinfo(title="Succès !", message="Vos paramètres ont étés enregistrés avec succès !")
    fen.destroy()
    # On cache la fenêtre, ensuite on affiche un message de succès puis on supprime la fenêtre afin d'avoir un meilleure rendu visuel

def LectureParamètres():

    """ Fonction qui lit les paramètres sauvegardés sur la machine """

    if os.path.exists("Paramètres"):
    # Si le fichier de paramètre existe déja

        FichierParamètres = open("Paramètres", "r", encoding="utf-8")
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

    global NomUser, ValeurCase, fen

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

    # Partie nom d'utilisateur par défaut

    Label(CadreGénéral, text="Votre nom d'utilisateur par défaut :", bg="grey").grid(pady=15, padx=15, row=0, column=0)
    # On ne stocke pas le label dans une variable car on n'aura pas besoin le réutiliser
    
    NomUser = Entry(CadreGénéral)
    NomUser.grid(row=0, column=1)

    if DicoParamètres["NomUserDéfaut"] != "Inconnu":
        NomUser.insert(0, DicoParamètres["NomUserDéfaut"])
    #####

    #Partie activation de la sauvegarde

    def changementValeur():

        """ Cette fonction permet de changer la valeur de la variable Tkinter "ValeurCase. 
        On n'utilise pas le paramètres var sur le Checkbutton car ce dernier ce fonction pas
        quand le fichier est appellée comme module"""

        global ValeurCase

        if ValeurCase.get() == True:
            ValeurCase.set(False)  
        else:
            ValeurCase.set(True)

    
    ValeurCase = tk.BooleanVar() 

    BouttonActivationSauv = Checkbutton(CadreGénéral, bg="grey", activebackground="grey", command= changementValeur)
    BouttonActivationSauv.grid(pady=15, padx=10, row=1, column=0)

    if DicoParamètres["Sauvegarde"] == "Activée":
        BouttonActivationSauv.select()
        ValeurCase.set(True)
    else:
        ValeurCase.set(False)

    Label(CadreGénéral, text="Activation de la sauvegarde", bg="grey").grid(row=1, column=1)
    #####

    Enregistrer = Button(CadreGénéral, text="Enregistrer", command=EnregistrerParamètres)
    Enregistrer.grid(pady=15, padx=15, row=2, column=1)

    """ Widgets de l'onglet son """

    
    notebook.grid(row=0, column=0, sticky="n")
    # On ajout les boutton pour changer d'onglets
    
    fen.mainloop()

if __name__ == "__main__":
# Si le fichier est executé et non importé comme un module

    LectureParamètres()
    InterfaceParamètres()
