import os
import winsound
import tkinter as tk
from tkinter import *
from tkinter import ttk
from shutil import copy2
from Modules import Sauvegarde
from tkinter import filedialog
from tkinter import messagebox


ListeParamètres = ["NomUserDéfaut", "Sauvegarde", "PortPréféré", "SonEnvoi"]
DicoParamètres = {}


def EnregistrerParamètres():

    """ Fonction qui récupére les paramètres dans l'interface et les enregistre dans 
    un fichier """

    global DicoParamètres, fen, NomUser, ValeurCase, EntréPort, Sélection

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

    ####

    # Récupération du port préféré

    ValeurPort = EntréPort.get()

    if ValeurPort == "":

        DicoParamètres["PortPréféré"] = "Inconnu"

    else:
        DicoParamètres["PortPréféré"] = ValeurPort

    if Sélection == None:

        DicoParamètres["SonEnvoi"] = "Inconnu"

    else:

        DicoParamètres["SonEnvoi"] = Sélection

    

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

    global fen, NomUser, ValeurCase, EntréPort, Sélection

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
    
    notebook = ttk.Notebook(fen, width=550, height=460)
    
    CadreGénéral = tk.Frame(notebook, bg="grey", width=550, height=460)
    CadreSon = tk.Frame(notebook, bg="grey", width=550, height=460)
    # On définit les cadres, qui seront en fait les onglets
    
    notebook.add(CadreGénéral, text="Général")
    notebook.add(CadreSon, text="Son")

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

    # Partie Port préféré

    Label(CadreGénéral, text="Votre port d'hôte préféré : ", bg="grey").grid(pady=15, padx=15, row=2, column=0)
    
    EntréPort = Entry(CadreGénéral)
    EntréPort.grid(row=2, column=1)

    if DicoParamètres["PortPréféré"] != "Inconnu":
        EntréPort.insert(0, DicoParamètres["PortPréféré"])

    #####


    Enregistrer = Button(CadreGénéral, text="Enregistrer", command=EnregistrerParamètres)
    Enregistrer.grid(pady=15, padx=15, row=3, column=1)

    """ Widgets de l'onglet son """

    Sélection = None

    def Upload():
        
        fichier = filedialog.askopenfilename(title = "Choisisez le son")
        copy2(fichier, "Sons/")
        # On demande à l'utilisateur de sélectioner le son qu'il veut uploader 
        # et on copie le son dans le répertoiré dédié

        if fichier.split(".")[1] != "wav":
            tk.messagebox.showerror(title="Mauvais format", message="Le son doit être au format wav")
        else:

            ListeFichierSon.delete(0,"end")
            # On efface tout les sons affichés
            ListeFichiers = os.listdir("Sons")
            # On récupere dans une liste chaque fichier du dossier Sons

            for fichier in ListeFichiers:
                if fichier.split(".")[1] == "wav":
                # On coupe le nom du fichier pour vérifier l'extension
                # son.wav devient ["son", "wav"]

                    ListeFichierSon.insert(END, fichier)


    def CallbackClicSon():

        global Sélection

        """ Fonction appellé au clic sur un son, qui permet de récuperer le son sélectioné """

        if ListeFichierSon.curselection() != ():
        # Le premier clic n'est pas pris en compte par tkinter

            Sélection  = ListeFichierSon.get(ListeFichierSon.curselection())
            winsound.PlaySound("Sons/" + Sélection, winsound.SND_ASYNC)
            Titre.configure(text="Son d'envoi actuel : " + Sélection)


    if DicoParamètres["SonEnvoi"] == "Inconnu":
        son = "pop.waw"
    else:
        son = DicoParamètres["SonEnvoi"] 

    Titre = Label(CadreSon, text="Son d'envoi actuel : " + son, bg="grey")
    Titre.pack(pady=10)

    Label(CadreSon, text="Double-cliquez sur un son pour le sélectioner", bg="grey").pack(pady=5)

    ListeFichierSon = Listbox(CadreSon, width="60", height="17")
    ListeFichierSon.pack()

    ListeFichierSon.bind("<Button-1>", lambda x: CallbackClicSon())

    ListeFichiers = os.listdir("Sons")
    # On récupere dans une liste chaque fichier du dossier Sons

    for fichier in ListeFichiers:

        if fichier.split(".")[1] == "wav":
        # On coupe le nom du fichier pour vérifier l'extension
        # son.wav devient ["son", "wav"]
    
            ListeFichierSon.insert(END, fichier)



    cadreBouttons = Frame(CadreSon, bg="grey")
    cadreBouttons.pack(pady=40)

    ChoisirRéception = Button(cadreBouttons, text="Choisir le son de réception", width="21")
    ChoisirRéception.pack(side=LEFT, padx=7)

    NouveauSon = Button(cadreBouttons, text="Uploader un nouveau son", width="21", command=Upload)
    NouveauSon.pack(side=LEFT, padx=7)

    Enregistrer = Button(cadreBouttons, text="Enregistrer", width="21", command=EnregistrerParamètres)
    Enregistrer.pack(side=LEFT, padx=7)
    ####
    
    notebook.grid(row=0, column=0, sticky="n")
    # On ajout les boutton pour changer d'onglets
    
    fen.mainloop()

if __name__ == "__main__":
# Si le fichier est executé et non importé comme un module

    # LectureParamètres()
    # InterfaceParamètres()
    # Zone à décommenter durant le développement sur les paramétres
    pass