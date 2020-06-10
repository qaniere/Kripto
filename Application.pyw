# coding: utf8
import sys
import time
import socket
import tkinter
import winsound
import threading
from tkinter import *
import tkinter.simpledialog
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint, choices
from Modules import ChiffrementRSA, Fonctions, LecteurSauvegarde, Paramètres, Sauvegarde, Serveur

Paramètres.LectureParamètres()
# On lit les paramètres

listeNoms = ["Autruche", "JeanBon", "AmiralBenson", "TomNook", "Karamazov", "OdileDeray", "PatéEnCroute", "Risitas", "Clown"]
#La liste des noms qui seront suggérés à l'utilisateur.

FichierSauvegarde = None
MotDePasse = None
#Initilisation du mot de passe de la sauvegarde et le fichier de sauvegarde

Module, CléPublique, CléPrivée = ChiffrementRSA.génération(16)
#On génére une clé publique et une clé publique et on garde en mémoire le module de chiffrement

NombreErreurs = 0
#On initialise le compte d'erreurs

EnvoiOK = True
SonActivé = True
#Par défault, on considére que le son est activé et que l'utilisateur peut envoyer des messages

def envoyer():

    """Fonction qui chiffre et envoi les message au serveur. Les messages sont chiffrés en fonction du serveur"""

    global saisieMessage, nomUser, filMessages, ConnexionSocket, NombreErreurs, CléPubliqueServeur, ModuleServeur, SonActivé, EnvoiOK
    #On récuper toutes les variables et objets nécésssaires au fonctionnement de la fonction

    message = saisieMessage.get()
    #On récupere le message dans l'entrée où il a été saisi

    if len(message) > 1000:

        tkinter.messagebox.showerror(title="Attention au spam !", message="Afin d'éviter de surcharger le serveur, les messages de plus de 1000 caractères sont interdits")
        return
        #On stoppe l'éxeuction de la fonction

    elif message == "/stop":
        
        RetournerMenu()
    
    elif len(message) != 0 and EnvoiOK:

        EnvoiOK = False
        #On rend impossible l'envoi de nouveaux messages
            
        messageInterface = f"[{time.strftime('%H:%M:%S')}] {nomUser} → {message}"
        #On garde de coté un message avec un formaté spécialement pour l'interface, mais on ne l'utilise que si l'envoi est réussi.

        message = Fonctions.formaterPaquet("Message", message)
        #On formate le paquet

        message = ChiffrementRSA.chiffrement(message, CléPubliqueServeur, ModuleServeur)
        #On transforme le message en liste de chiffres, correspondant à leur identifiant Ascii, puis on chiffre le message
        #On récupere alors une liste d'entiers
        
        messageFinal = f"{len(message)}-{message}"
        #On rajoute un en tête avec la longueur totale du message
        messageFinal = messageFinal.encode("utf-8")
        #On encode le tout en UTF8

        try:
            ConnexionSocket.send(bytes(messageFinal))
            #On essaie d'envoyer le message au serveur.

        except (ConnectionResetError, ConnectionAbortedError):
        #Si le serveur ne répond pas
    
            if NombreErreurs < 3:
                tkinter.messagebox.showerror(title="Aïe...", message="Impossible de joindre le serveur. Veuillez réessayer.")
                NombreErreurs += 1
            else:
            #Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

                messsageErreur = "Le serveur est injoignable pour le moment. Veuillez vous reconnecter ou bien référez vous à l'aide"
                #On stocke le message dans un variable pour diminuer la taille de la ligne d'en dessous
                tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
                exit() #TODO => Remplacer par retour au menu

        else:
        #Si il n'a pas eu d'execeptions

            if len(messageInterface) > 70:
            #Si le message à afficher fait plus de 70 caratères

                listeLignes = Fonctions.couperPhrases(messageInterface)
                #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                for ligne in listeLignes:
                #On insere chaque ligne
                    filMessages.insert(END, ligne)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)
                        #On sauvegarde la ligne
            else:
                filMessages.insert(END, messageInterface)

                if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                    Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, messageInterface)
                    #On sauvegarde le message

            filMessages.yview(END)
            #On défile tout en bas cette dernière, vers le message le plus récent

            if SonActivé == True:

                if Paramètres.DicoParamètres["SonEnvoi"] != "Inconnu":
                    winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonEnvoi"], winsound.SND_ASYNC)
                
                else:
                    winsound.PlaySound("Sons/Pop.wav", winsound.SND_ASYNC)
            
            saisieMessage.delete(0, "end")
            #On vide la zone de saisie du message

            def RéactivationEnvoi():

                global EnvoiOK

                EnvoiOK = True

            fen.after(500, RéactivationEnvoi)
            #Au bout de 500ms en asynchrone, on appelle la fonction qui rendra possible l'envoi de messages



def reception():
        
    """ Fonction qui s'appelle elle même toutes les 10ms qui permet de vérifier
    la présence de nouveaux messages"""

    global filMessages, ConnexionSocket, CléPrivée, Module, SonActivé, Connexion
    #On récupere les variables nécéssaires au fonctionemment de la fonction

    while Connexion == True:
        try:
        #Cette partie du code est dans un bloc "try, except" car "ConnexionSocket.setblocking(0)" a été défini sur False
        #Au lieu d'attendre un message, si rien n'est envoyé cela va générer une exception, ce qui permet un fonctionnement asynchrone.

            messageRecu = ConnexionSocket.recv(32768)
            #2048 est la limite d'octets recevables
            messageRecu = messageRecu.decode("utf-8")

            if messageRecu != "":

                messageRecu = messageRecu.split("-")
                #Le message comporte un petit entête 
                #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message. Cela peut arriver que les très long messages (Fichiers) 
                #fassent plus de 2048 la taille taille du buffer

                LongeurMessage = int(messageRecu[0])

                while len(messageRecu[1]) < LongeurMessage:
                #Tant que le message recu est plus petit que la longueur totale du message

                    suite = ConnexionSocket.recv(32768)
                    suite = suite.decode("utf-8")

                    messageRecu[1] += suite
                    #On ajoute la suite du message recu

                messageRecu = ChiffrementRSA.déchiffrement(messageRecu[1], CléPrivée, Module)
                #On ne déchiffre que l'index 1 du message, qui est le messge en lui même
                #0 étant la longueur de ce message

                if len(messageRecu) > 70:
                #Si le message à afficher fait plus de 70 caratères
            
                    listeLignes = couperPhrases(messageRecu)
                    #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                    for ligne in listeLignes:
                    #On insere chaque ligne
                        filMessages.insert(END, ligne)

                        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                            NouvelleLigne(FichierSauvegarde, MotDePasse, ligne)
                            #On sauvegarde la ligne

                else:
                    filMessages.insert(END, messageRecu)

                    if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":
                        Sauvegarde.NouvelleLigne(FichierSauvegarde, MotDePasse, messageRecu)
                        #On sauvegarde le nouveau message
            
                filMessages.yview(END)
                #On insére le message dans la listbox des messages, puis on force le défilement tout en bas de cette dernière

                if SonActivé == True:
                    if Paramètres.DicoParamètres["SonRéception"] != "Inconnu":
                        winsound.PlaySound("Sons/" + Paramètres.DicoParamètres["SonRéception"], winsound.SND_ASYNC)
                    else:
                        winsound.PlaySound("Sons/Dong.wav", winsound.SND_ASYNC)
            else:
                input("message vide")

        except BlockingIOError:
        #Si aucun message n'a été envoyé, on ne fait rien et on attend pour préserver les ressources la machine
            time.sleep(0.1)

        except (ConnectionAbortedError, ConnectionResetError):
        #Le serveur a crashé

            tkinter.messagebox.showerror(title="Aïe...", message="Le serveur a crashé...")
            exit()



def deconnexion():

    global Connexion

    Connexion = False
    ConnexionSocket.close()



def CouperSon():
    global SonActivé

    SonActivé = False

    barreMenu.delete(2)
    barreMenu.insert_command(2, label="Activer Son", command=ActiverSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande ActiverSon à la même position



def ActiverSon():
    global SonActivé

    SonActivé = True

    barreMenu.delete(2)
    barreMenu.insert_command(2, label="Couper Son", command=CouperSon)
    #On supprime la commande à l'index 2 du menu pour y ajouter la commande CouperSon à la même position

def RetournerMenu():
    global filMessages, saisieMessage, bouttonEnvoyer

    Confirmation = messagebox.askquestion (f"Vous partez déja {nomUser} ?","Vous voulez vraiment retourner au menu ?",icon = "warning")
    if Confirmation == "yes":

        filMessages.pack_forget()
        saisieMessage.pack_forget()
        bouttonEnvoyer.pack_forget()
        #On efface l'interface de conversation

        fen.unbind_all(ALL)
        #On supprime tout les raccourcis
    
        barreMenu.delete(1)
        barreMenu.delete(1)
        barreMenu.delete(3)
        #On efface certaines commandes du menu : "Menu, Couper Son et Infos Serveur"

        deconnexion()
        #Lancement de la procédure de déconnexion

        AfficherMenu()
        #Affichage du menu



def affichageConversation():
        
    """ Cette fonction sert à générer l'interface de la conversation"""

    global cadreParametres, saisieMessage, nomUser, filMessages, bouttonEnvoyer, Connexion, threadRéception
    #On récuperer les objets et les variables nécéssaire au fonctionnement de la fonction

    logo.pack_forget()
    cadreParametres.pack_forget()
    #On efface les élements de connexion / paramétrage du serveur

    barreMenu.insert_command(1, label="Couper Son", command=CouperSon)
    barreMenu.insert_command(4, label="Infos du serveur", command=infosServeur)
    barreMenu.insert_command(0, label="Menu", command=RetournerMenu)
    #On insère les boutons dans le menu au index donnés

    filMessages = Listbox(fen, width="70", height="20")
    filMessages.pack(pady=15)

    saisieMessage = Entry(fen, width="60")
    saisieMessage.pack()

    bouttonEnvoyer = Button(fen, text="Envoyer", command=envoyer)
    bouttonEnvoyer.pack(pady=15)

    saisieMessage.bind("<Button-1>", lambda a: Fonctions.placeholder(saisieMessage, "", False))
    #On associe le clic gauche sur la zone de saisie du message à la fonction placeholder
    #On utilise une lambda pour appeler une fonction avec des arguments

    fen.bind_all("<Return>", lambda c: envoyer())
    #On associe l'appui a a fonction envoyer avec une fonction lambda afin de pouvoir envoyer aucun argument

    Connexion = True
    threadRéception = threading.Thread(target=reception)
    threadRéception.daemon = True #Ce flag signifie que quand il ne reste que ce thread, le programme s'arrête.
    threadRéception.start()
    #On commence à recevoir des messages

    Fonctions.placeholder(saisieMessage, "Saisissez votre message ici", True)
    #On affiche un placeholder dans le zone de saisie des messages


def connexion():
        
    """ Cette fonction sert à se connecter au serveur et à envoyer le nom d'utilisateur, la clé publique, le module de chiffrement au serveur,
    et on recoit les informations de chiffrement du serveur, la clé publique et le module de chiffrement"""

    global IP, Port, nomUser, entreNom, ConnexionSocket, entreIP, Role, CléPublique, CléPubliqueServeur, ModuleServeur
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

    IP = entreIP.get()
    nomUser = entreNom.get()

    ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini notre connexion socket
    # - AF_INET => Protocole IPV4
    # - SOCK_STREAM => Stream veut dire cours d'eau, comme un flot continu de donnés qui est envoyé

    ConnexionSocket.settimeout(5)
    #Si au bout de 5secondes, il n'y pas de réponse (Délai plus que nécéssaire pour des simples paquets TCP) une exception est générée

    try:
        ConnexionSocket.connect((IP, Port))
        #Le code après cette instruction est executé uniquement si la connection réussit

        données = f"{nomUser}|{CléPublique}|{Module}"
        données = données.encode("utf-8")

        ConnexionSocket.send(bytes(données))

        #On formate, puis on envoi les données de chiffrement au serveur

        AutorisationEtDonnées = ConnexionSocket.recv(2048)
        AutorisationEtDonnées = AutorisationEtDonnées.decode("utf-8")

        #On recoit de la part du serveur l'autorisation de se connecter, et les données de chiffrement du serveur

        if AutorisationEtDonnées != "False":
        #Si le serveur autorise la connexion

            AutorisationEtDonnées = AutorisationEtDonnées.split("|")
            #On récupere les données sous forme de le liste

            CléPubliqueServeur = int(AutorisationEtDonnées[0])
            ModuleServeur = int(AutorisationEtDonnées[1])

            #On converti les données en entiers, puis on les affectes au variables adaptées

            ConnexionSocket.setblocking(0)
            #On définit le mode de connexion sur non bloquant (Voir explications dans la fonction reception)

            
            return True
            #On retoune que la connexion a été validé 
        else:
        #Si le serveur ne donne pas son autorisation

            motif = ConnexionSocket.recv(4096)
            #On recoit du serveur le motif du refus de 
            
            tkinter.messagebox.showerror(title="Connexion refusée", message=motif.decode("utf-8"))	

    except (ConnectionRefusedError, socket.timeout):
    #Si on arrive pas à se connecter au serveur

        if Role == "Hote":
        #Si c'est l'hôte, il a déja recu l'erreur de la part du serveur donc affiche rien

            return False
            #On indique que la connexion est un échec
        else:
            messageErreur = "IL semblerait que les coordonées du serveur ne soit pas valides. Réferez vous à l'aide pour régler ce problème."
            #On raccourci la ligne du dessous avec cette variable
            tkinter.messagebox.showerror(title="Aïe...", message=messageErreur)
            return False



def démarrerServeur():
        
    """ Cette fonction sert à démarrez le serveur quand on est hôte"""

    global entreIP, entrePort, IP, Port, Role, FichierSauvegarde, MotDePasse, entreNom
    #On récupere les objets et les variables nécéssaire au fonctionnement de la fonction

    if len(entreNom.get()) > 16:

        tkinter.messagebox.showerror(title="Aie...", message="Votre nom d'utilisateur doit faire moins de 16 caractères")
        return 
        #On stoppe l'exécution de la fonction

    Role = "Hote"
    IP = entreIP.get()
    Port = int(entrePort.get())

    fen.after(10, Serveur.Démarrer(IP, Port, Paramètres.DicoParamètres["NombreUsersMax"]))
    #On lance de manière asynchrone le démarrage du serveur

    if connexion() == True:
    #Si la connexion est une réussite, on affiche les conversations

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show="*")
            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Veuillez confirmer le mot de passe", show="*")
            #On demande le mot et sa confirmation

            while ConfirmationMotDePasse != MotDePasse:
            #Tant que la confirmination n'est validée

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Confirmation erronée. Veuillez confirmer le mot de passe", show='*')
            
            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)
            #On initialise le fichier de sauvegarde
        
        affichageConversation()



def seConnecter():
        
    """ Fonction qui affiche l'interface de discusion si la connexion est une réussite"""

    global entreIP, entrePort, IP, Port, Role, FichierSauvegarde, MotDePasse
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction
    
    Role = "Client"
    Port = int(entrePort.get())
    IP = entreIP.get()

    if connexion() == True: 

        if Paramètres.DicoParamètres["Sauvegarde"] == "Activée":

            MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show="*")
            ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Veuillez confirmer le mot de passe", show="*")
            #On demande le mot et sa confirmation

            while ConfirmationMotDePasse != MotDePasse:
            #Tant que la confirmination n'est validée

                ConfirmationMotDePasse = tkinter.simpledialog.askstring("Confirmation", "Confirmation erronée. Veuillez confirmer le mot de passe", show='*')
            
            FichierSauvegarde = Sauvegarde.InitialisationSauvegarde(MotDePasse)
            #On initialise le fichier de sauvegarde
        affichageConversation()




def hote():
        
    """ Fonction qui affiche l'interface de création de serveur """

    global entrePort, IP, nomUser, cadreParametres, entreNom, entreIP, listeNoms
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

    messageBienvenue.pack_forget()
    cadreBouttons.pack_forget()
    #On efface le menu

    hote = socket.gethostname()
    IP = socket.gethostbyname(hote)
    #On récupere l'addresse IP de la machine

    cadreParametres = Frame(fen, bg="grey")
    cadreParametres.pack()       

    votreIP = Label(cadreParametres, text="Votre Adresse IP", bg="Grey")
    votreIP.pack(anchor=CENTER, pady=7)

    entreIP = Entry(cadreParametres)
    entreIP.insert("end", IP)
    entreIP.pack(anchor=CENTER)

    votrePort = Label(cadreParametres, text="Port", bg="Grey")
    votrePort.pack(anchor=CENTER, pady=7)


    entrePort = Entry(cadreParametres)
    entrePort.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["PortPréféré"] != "Inconnu":
    # Si l'utilisateur a définit un port par défaut
        Fonctions.placeholder(entrePort, Paramètres.DicoParamètres["PortPréféré"], True)

    else:
        portRecommande = randint(49152, 65535)
        #On recommande un port dans la plage de ceux les moins utilisés
        Fonctions.placeholder(entrePort, portRecommande, True)
        #On affiche la suggestion du nom, en envoyant le premier et le seul indice de la liste de la suggestions de nom
    

    votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
    votreNom.pack(anchor=CENTER, pady=7)

    entreNom = Entry(cadreParametres)
    entreNom.pack(anchor=CENTER)
    
    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut
        Fonctions.placeholder(entreNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)
    else:
        suggestionNom = choices(listeNoms)
        #On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms
        Fonctions.placeholder(entreNom, suggestionNom[0], True)
        #On affiche la suggestion du nom, en envoyant le premier et le seul indice de la liste de la suggestions de nom

    entreNom.bind("<Button-1>", lambda b: Fonctions.placeholder(entreNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir executer une fonction avec des arguments

    bouttonStart = Button(cadreParametres, text="Démarrer", command=démarrerServeur)
    bouttonStart.pack(pady=20)



def client():
        
    """ Cette fonction permet à un client de se connecter au serveur""" 

    global entreIP, entrePort, entreNom, cadreParametres, listeNoms
    #On récupere les objets et les variables nécéssaire au fonctionnement de la fonction

    messageBienvenue.pack_forget()
    cadreBouttons.pack_forget()
    #On efface le menu

    cadreParametres = Frame(fen, bg="grey")
    cadreParametres.pack()       

    IpduServeur = Label(cadreParametres, text="Adresse IP du serveur", bg="Grey")
    IpduServeur.pack(anchor=CENTER, pady=7)

    entreIP = Entry(cadreParametres)
    entreIP.insert("end", "192.168.1.")
    entreIP.pack(anchor=CENTER)

    PortduServeur = Label(cadreParametres, text="Port du serveur", bg="Grey")
    PortduServeur.pack(anchor=CENTER, pady=7)

    entrePort = Entry(cadreParametres)
    entrePort.pack(anchor=CENTER)

    votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
    votreNom.pack(anchor=CENTER, pady=7)

    entreNom = Entry(cadreParametres)
    entreNom.pack(anchor=CENTER)

    if Paramètres.DicoParamètres["NomUserDéfaut"] != "Inconnu":
    # Si l'utilisateur a définit un nom d'utilisateur par défaut

        Fonctions.placeholder(entreNom, Paramètres.DicoParamètres["NomUserDéfaut"], True)
    else:
        suggestionNom = choices(listeNoms)
        #On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms
        Fonctions.placeholder(entreNom, suggestionNom[0], True)
        #On affiche la suggestion du nom, en envoyant le premier et le seul indice de la liste de la suggestions de nom

    entreNom.bind("<Button-1>", lambda b: Fonctions.placeholder(entreNom, "", False))
    #On utilise une fonction anonyme lambda pour pouvoir executer une fonction avec des arguments

    bouttonStart = Button(cadreParametres, text="Se connecter",  command=seConnecter)
    bouttonStart.pack(pady=20)



def infosServeur():
    """ Cette fonction affiches les informations du serveur dans une fenêtre en top level"""

    global IP, Port
    #On récupere les variables d'adresse du serveur

    def QuitterInfos():
        """Fonction qui détruit la fenêtre des infos du serveur"""
        fenInfos.destroy()
        
    fenInfos = Toplevel()
    fenInfos.geometry("300x280")
    fenInfos.configure(bg="grey")
    fenInfos.resizable(width=False, height=False)
    fenInfos.iconbitmap(bitmap="Médias/information.ico")
    fenInfos.title("Infos du serveur")
    #Définition de l'apparence de la fenêtre

    TitreAdresseServeur = Label(fenInfos, text="Adresse du serveur", bg="Grey", font=policeTitre)
    TitreAdresseServeur.pack(pady=10)

    AdresseServeur = Label(fenInfos, text=IP, bg="Grey", font=policeSousTitre)
    AdresseServeur.pack()

    TitrePortServeur = Label(fenInfos, text="Port du serveur", bg="Grey", font=policeTitre)
    TitrePortServeur.pack(pady=10)

    PortServeur = Label(fenInfos, text=Port, bg="Grey", font=policeSousTitre)
    PortServeur.pack() 

    TitreUtilisateursCo = Label(fenInfos, text="Utiliseurs connectées", bg="Grey", font=policeTitre)
    TitreUtilisateursCo.pack(pady=10)

    UtilisateurCo = Label(fenInfos, text="N/C", bg="Grey", font=policeSousTitre)
    UtilisateurCo.pack()

    BouttonFermer = Button(fenInfos, text="Fermer", command=QuitterInfos)
    BouttonFermer.pack(pady=20, side=BOTTOM)

    fenInfos.focus_force()
    #On affiche la fenêtre au premier plan

    fenInfos.mainloop()

def fermeture():

    """ Fonction appellée quand l'utilisateur veut fermer la fenêtre """
    RéponseUser  = tkinter.messagebox.askokcancel("Kripto","Vous partez déja ?")
    
    if RéponseUser == True:

        sys.exit()
        #On utilise sys.exit() plutôt que exit() car cela éviter au threads de tourner en arrière plan
        


fen = Tk()
fen.geometry("550x460")
fen.title("Kripto - Un chat chiffré")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")
fen.protocol("WM_DELETE_WINDOW", fermeture)

barreMenu = Menu(fen)
barreMenu.add_command(label="Aide", command=Fonctions.pasCode)
barreMenu.add_command(label="Sauvegardes", command=LecteurSauvegarde.LecteurSauvegarde)
barreMenu.add_command(label="Paramètres", command=Paramètres.InterfaceParamètres)
barreMenu.add_command(label="Contact", command=Fonctions.pasCode)
fen.configure(menu=barreMenu)
#On configure la barre de menu

policeBienvenue = tkFont.Font(family="Verdanna",size=16,weight="bold")
policeBoutton = tkFont.Font(family="Arial",size=12,weight="bold")
policeTitre = tkFont.Font(size=14,weight="bold")
policeSousTitre = tkFont.Font(size=12)

imageLogo = PhotoImage(file="Médias/Logo.png")

def AfficherMenu():

    global messageBienvenue, cadreBouttons, logo

    logo = Label(fen, bg="grey", image=imageLogo)
    logo.pack() 

    messageBienvenue = Label(fen, text="Bienvenue dans Kripto. Pour démarrez, dites-nous \nsi vous voulez être hôte ou bien client.", bg="grey", font=policeBienvenue)
    messageBienvenue.pack()

    cadreBouttons = Frame(fen, bg="grey")
    cadreBouttons.pack(pady=60)

    bouttonHote = Button(cadreBouttons, text="Être hôte", font=policeBoutton, command=hote)
    bouttonHote.pack(side=LEFT, padx=7)

    bouttonClient = Button(cadreBouttons, text="Être client", font=policeBoutton, command=client)
    bouttonClient.pack(side=LEFT, padx=7)

AfficherMenu()
fen.mainloop()
