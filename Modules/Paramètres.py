# coding: utf8
import os
import winsound
import tkinter as tk
from tkinter import *
from tkinter import ttk
from shutil import copy2
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox


ListeParamètres = ["NomUserDéfaut", "Sauvegarde", "PortPréféré", "SonEnvoi", "SonRéception", "NombreUsersMax", "MotDePasse"]
DicoParamètres = {}


def EnregistrerParamètres():

    """ Fonction qui récupére les paramètres dans l'interface et les enregistre dans 
    un fichier """

    global DicoParamètres, fen, NomUser, ValeurCase, EntréPort, Sélection, SélectionRéception, NombreUsersMax, MotDePasse

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
    ####

    # Récupération du son d'envoi
    if Sélection != None:

        DicoParamètres["SonEnvoi"] = Sélection
         
    ####    

    # Récupération du son de réception
    if SélectionRéception != None:

        DicoParamètres["SonRéception"] = SélectionRéception

    FichierParamètres = open("Paramètres", "w", encoding="utf-8")

    # Récupération du nombre maximums de clients connectés au serveur

    if NombreUsersMax.get() != "":

        DicoParamètres["NombreUsersMax"] = NombreUsersMax.get()

    else:
        DicoParamètres["NombreUsersMax"] = "0"

    # Récuperation du mot de passe du serveur

    if MotDePasse.get() != "":

        DicoParamètres["MotDePasse"] = MotDePasse.get()

    else:
        DicoParamètres["MotDePasse"] = "Inconnu"

    for Paramètre in ListeParamètres:
    # On récupere chaque paramètres

        FichierParamètres.write(DicoParamètres[Paramètre] + "\n")

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

        ValeursParamètres = Contenu.split("\n")

        for index in range(len(ListeParamètres)):
        # Pour chaque paramètres

            DicoParamètres[ListeParamètres[index]] = ValeursParamètres[index]
    
    else:

        for index in range(len(ListeParamètres)):
        # Pour chaque paramètres

            DicoParamètres[ListeParamètres[index]] = "Inconnu"



def InterfaceParamètres():

    """ Fonction qui affiche les paramètres """

    global fen, NomUser, ValeurCase, EntréPort, Sélection, SélectionRéception, NombreUsersMax, MotDePasse, AffichageMDP, MontrerMDP

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
    CadreSonEnvoi = tk.Frame(notebook, bg="grey", width=550, height=460)
    CadreSonRéception = tk.Frame(notebook, bg="grey", width=550, height=460)
    CadreServeur = tk.Frame(notebook, bg="grey", width=550, height=460)
    # On définit les cadres, qui seront en fait les onglets
    
    notebook.add(CadreGénéral, text=" Général ")
    notebook.add(CadreSonEnvoi, text=" Son d'envoi ")
    notebook.add(CadreSonRéception, text=" Son de réception ")
    notebook.add(CadreServeur, text=" Serveur ")

    """ Widgets de l'onglet général """

    PoliceTitre = tkFont.Font(family="Verdanna",size=16)
    Label(CadreGénéral, text="Paramètres généraux", bg="grey", font=PoliceTitre).pack(pady=15)

    PoliceSousTitre = tkFont.Font()
    Label(CadreGénéral, font=PoliceSousTitre, text="Notez bien que vous devrez rédémarrer Kripto,\n ou au moins la conversation en cours pour que\nles changements s'appliquent.", bg="grey").pack()

    # Partie nom d'utilisateur par défaut

    ConteneurNomUser = Frame(CadreGénéral, bg="grey")
    ConteneurNomUser.pack(pady=10)

    Label(ConteneurNomUser, text="Votre nom d'utilisateur par défaut :", bg="grey").pack(pady=15, padx=15, side="left")
    # On ne stocke pas le label dans une variable car on n'aura pas besoin le réutiliser
    
    NomUser = Entry(ConteneurNomUser)
    NomUser.pack(side="left")

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

    ConteneurSauvegarde = Frame(CadreGénéral, bg="grey")
    ConteneurSauvegarde.pack()

    BouttonActivationSauv = Checkbutton(ConteneurSauvegarde, bg="grey", activebackground="grey", command= changementValeur)
    BouttonActivationSauv.pack(pady=15, padx=10, side="left")

    if DicoParamètres["Sauvegarde"] == "Activée":
        BouttonActivationSauv.select()
        ValeurCase.set(True)
    else:
        ValeurCase.set(False)

    Label(ConteneurSauvegarde, text="Activation de la sauvegarde", bg="grey").pack(side="left")
    #####

    # Partie Port préféré

    ConteneurPort = Frame(CadreGénéral, bg="grey")
    ConteneurPort.pack()

    Label(ConteneurPort, text="Votre port d'hôte préféré : ", bg="grey").pack(pady=15, padx=15, side="left")
    
    EntréPort = Entry(ConteneurPort)
    EntréPort.pack(side="left")

    if DicoParamètres["PortPréféré"] != "Inconnu":
        EntréPort.insert(0, DicoParamètres["PortPréféré"])

    #####


    Enregistrer = Button(CadreGénéral, text="Enregistrer", command=EnregistrerParamètres)
    Enregistrer.pack(side="bottom", pady=50)

    """ Widgets de l'onglet son d'envoi """

    Sélection = None

    def UploadSonEnvoi():
        
        fichier = filedialog.askopenfilename(title = "Choisisez le son")
        # On demande à l'utilisateur de sélectioner le son qu'il veut uploader 

        if fichier.split(".")[1] != "wav":
            tk.messagebox.showerror(title="Mauvais format", message="Le son doit être au format wav")
        else:
            copy2(fichier, "Sons/")
            # et on copie le son dans le répertoiré dédié

            ListeFichierSonEnvoi.delete(0,"end")
            # On efface tout les sons affichés
            ListeFichiers = os.listdir("Sons")
            # On récupere dans une liste chaque fichier du dossier Sons

            for fichier in ListeFichiers:
                if fichier.split(".")[1] == "wav":
                # On coupe le nom du fichier pour vérifier l'extension
                # son.wav devient ["son", "wav"]

                    ListeFichierSonEnvoi.insert(END, fichier)


    def CallbackClicSonEnvoi():

        global Sélection

        """ Fonction appellé au clic sur un son, qui permet de récuperer le son sélectioné """

        if ListeFichierSonEnvoi.curselection() != ():
        # Le premier clic n'est pas pris en compte par tkinter

            Sélection  = ListeFichierSonEnvoi.get(ListeFichierSonEnvoi.curselection())
            winsound.PlaySound("Sons/" + Sélection, winsound.SND_ASYNC)
            TitreSonEnvoi.configure(text="Son d'envoi actuel : " + Sélection)


    if DicoParamètres["SonEnvoi"] == "Inconnu":
        son = "Pop.wav"
    else:
        son = DicoParamètres["SonEnvoi"] 

    PoliceTitreSon = tkFont.Font(family="Verdanna", size=14)
    TitreSonEnvoi = Label(CadreSonEnvoi, text="Son d'envoi actuel : " + son, bg="grey", font=PoliceTitreSon)
    TitreSonEnvoi.pack(pady=10)

    Label(CadreSonEnvoi, text="Double-cliquez sur un son pour le sélectioner", bg="grey").pack(pady=5)

    ListeFichierSonEnvoi = Listbox(CadreSonEnvoi, width="60", height="17")
    ListeFichierSonEnvoi.pack()

    ListeFichierSonEnvoi.bind("<Button-1>", lambda x: CallbackClicSonEnvoi())

    ListeFichiers = os.listdir("Sons")
    # On récupere dans une liste chaque fichier du dossier Sons

    for fichier in ListeFichiers:

        if fichier.split(".")[1] == "wav":
        # On coupe le nom du fichier pour vérifier l'extension
        # son.wav devient ["son", "wav"]
    
            ListeFichierSonEnvoi.insert(END, fichier)



    cadreBouttons = Frame(CadreSonEnvoi, bg="grey")
    cadreBouttons.pack(pady=40)

    NouveauSon = Button(cadreBouttons, text="Uploader un nouveau son", width="20", command=UploadSonEnvoi)
    NouveauSon.pack(side=LEFT, padx=7)

    Enregistrer = Button(cadreBouttons, text="Enregistrer", width="20", command=EnregistrerParamètres)
    Enregistrer.pack(side=LEFT, padx=7)
    ####
    
    """ Widgets de l'onglet son de réception """

    SélectionRéception = None

    def UploadSonRéception():
        
        fichier = filedialog.askopenfilename(title = "Choisisez le son")
        # On demande à l'utilisateur de sélectioner le son qu'il veut uploader 

        if fichier.split(".")[1] != "wav":
            tk.messagebox.showerror(title="Mauvais format", message="Le son doit être au format wav")
        else:
            copy2(fichier, "Sons/")
            # et on copie le son dans le répertoiré dédié

            ListeFichierSonRéception.delete(0,"end")
            # On efface tout les sons affichés
            ListeFichiers = os.listdir("Sons")
            # On récupere dans une liste chaque fichier du dossier Sons

            for fichier in ListeFichiers:
                if fichier.split(".")[1] == "wav":
                # On coupe le nom du fichier pour vérifier l'extension
                # son.wav devient ["son", "wav"]

                    ListeFichierSonRéception.insert(END, fichier)


    def CallbackClicSonRéception():

        global SélectionRéception

        """ Fonction appellé au clic sur un son, qui permet de récuperer le son sélectioné """

        if ListeFichierSonRéception.curselection() != ():
        # Le premier clic n'est pas pris en compte par tkinter

            SélectionRéception  = ListeFichierSonRéception.get(ListeFichierSonRéception.curselection())
            winsound.PlaySound("Sons/" + SélectionRéception, winsound.SND_ASYNC)
            TitreSonRéception.configure(text="Son de réception actuel : " + SélectionRéception)


    if DicoParamètres["SonRéception"] == "Inconnu":
        SonRéception = "Dong.waw"
    else:
        SonRéception = DicoParamètres["SonRéception"] 

    PoliceTitreSon = tkFont.Font(family="Verdanna", size=14)
    TitreSonRéception = Label(CadreSonRéception, text="Son de réception actuel : " + SonRéception, bg="grey", font=PoliceTitreSon)
    TitreSonRéception.pack(pady=10)

    Label(CadreSonRéception, text="Double-cliquez sur un son pour le sélectioner", bg="grey").pack(pady=5)

    ListeFichierSonRéception = Listbox(CadreSonRéception, width="60", height="17")
    ListeFichierSonRéception.pack()

    ListeFichierSonRéception.bind("<Button-1>", lambda x: CallbackClicSonRéception())

    ListeFichiers = os.listdir("Sons")
    # On récupere dans une liste chaque fichier du dossier Sons

    for fichier in ListeFichiers:

        if fichier.split(".")[1] == "wav":
        # On coupe le nom du fichier pour vérifier l'extension
        # son.wav devient ["son", "wav"]
    
            ListeFichierSonRéception.insert(END, fichier)

    cadreBouttons2 = Frame(CadreSonRéception, bg="grey")
    cadreBouttons2.pack(pady=40)

    NouveauSon = Button(cadreBouttons2, text="Uploader un nouveau son", width="20", command=UploadSonRéception)
    NouveauSon.pack(side=LEFT, padx=7)

    Enregistrer = Button(cadreBouttons2, text="Enregistrer", width="20", command=EnregistrerParamètres)
    Enregistrer.pack(side=LEFT, padx=7)
    ####

    """ Widgets de l'onglets serveur """

    Label(CadreServeur, text="Nombre de clients maximum (0 = Infini) :", bg="grey").grid(row=0, column=0, padx=15, pady=20)

    NombreUsersMax = Spinbox(CadreServeur, from_=0, to=999)
    NombreUsersMax.grid(row=0, column=1)

    if DicoParamètres["NombreUsersMax"] != "Inconnu":
        NombreUsersMax.delete(0, 'end')
        NombreUsersMax.insert(0, DicoParamètres["NombreUsersMax"])

    Label(CadreServeur, text="Mot de passe du serveur :", bg="grey").grid(row=1, column=0, padx=15, pady=20)

    MotDePasse = Entry(CadreServeur, show="•")
    MotDePasse.grid(row=1, column=1)

    if DicoParamètres["MotDePasse"] != "Inconnu":
        MotDePasse.insert(0, DicoParamètres["MotDePasse"])

    def AfficherMDP():

        global AffichageMDP, MotDePasse, MontrerMDP

        if AffichageMDP == False:

            MotDePasse.configure(show="")
            MontrerMDP.configure(text="Cacher")
            AffichageMDP = True
        
        else:

            MotDePasse.configure(show="•")
            MontrerMDP.configure(text="Afficher")
            AffichageMDP = False


    AffichageMDP = False

    MontrerMDP = Button(CadreServeur, text="Afficher", command= lambda: AfficherMDP())
    MontrerMDP.grid(row=1, column=2)

    Enregistrer = Button(CadreServeur, text="Enregistrer", width="20", command=EnregistrerParamètres)
    Enregistrer.grid(row=2, column=1)
    
    notebook.grid(row=0, column=0, sticky="n")
    # On place les onglets dans la fenêtre
    
    fen.mainloop()
