# coding: utf8
import time
import socket
import tkinter
import winsound
import subprocess	
from tkinter import *
from Fonctions import *
from ChiffrementRSA import *
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint, choices

#Variables d'applications
global listeNoms, Module,CléPublique, CléPrivée, NombreErreurs, SonActivé

listeNoms = ["Autruche", "JeanBon", "AmiralBenson", "TomNook", "Karamazov", "OdileDeray", "PatéEnCroute", "Risitas", "Clown"]
#La liste des noms qui seront suggérés à l'utilisateur.

Module, CléPublique, CléPrivée = génération(16)
#On génére une clé publique et une clé publique et on garde en mémoire le module de chiffrement

NombreErreurs = 0
#On initialise le compte d'erreurs

SonActivé = True
#Par défault, on considére que le son est activé

def envoyer():

    """Fonction qui chiffre et envoi les message au serveur. Les messages sont chiffrés en fonction du serveur"""

    global saisieMessage, nomUser, filMessages, ConnexionSocket, NombreErreurs, CléPubliqueServeur, ModuleServeur, SonActivé
    #On récuper toutes les variables et objets nécésssaires au fonctionnement de la fonction

    message = saisieMessage.get()
    #On récupere le message dans l'entrée où il a été saisi

    if len(message) != 0:
            
        messageInterface = f"[{time.strftime('%H:%M:%S')}] {nomUser} → {message}"
        #On garde de coté un message avec un formaté spécialement pour l'interface, mais on ne l'utilise que si l'envoi est réussi.

        message = formaterPaquet("Message", message)
        #On formate le paquet

        message = transformationChiffres(message)
        message = cryptage(message, CléPubliqueServeur, ModuleServeur)
        #On transforme le message en liste de chiffres, correspondant à leur identifiant Ascii, puis on chiffre le message

        #On récupere alors une liste d'entiers

        ChaineMessage = ""

        for index in message:
        #On récupere tour à tour chaque index de la liste message
            ChaineMessage += str(index) + "/"
            #On ajoute à la variable vide chaque index qu'on converti en texte et on insére un / pour pouvoir les redécouper
        
        messageFinal = f"{len(ChaineMessage)}-{ChaineMessage}"
        #On rajoute un en tête avec la longueur totale du message
        messageFinal = messageFinal.encode('utf-8')
        #On encode le tout en UTF8

        try:
            ConnexionSocket.send(bytes(messageFinal))
            #On essaie d'envoyer le message au serveur.

        except ConnectionResetError:
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

                listeLignes = couperPhrases(messageInterface)
                #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                for ligne in listeLignes:
                #On insere chaque ligne
                    filMessages.insert(END, ligne)
            else:
                filMessages.insert(END, messageInterface)

            filMessages.yview(END)
            #On défile tout en bas cette dernière, vers le message le plus récent

            if SonActivé == True:
                winsound.PlaySound("Médias/SonEnvoi.wav", winsound.SND_ASYNC)
            
            saisieMessage.delete(0, 'end')
            #On vide la zone de saisie du message




def reception():
        
    """ Fonction récursive (Qui s'appelle elle même toutes les 10ms) qui permet de vérifier
    la présence de nouveaux messages"""

    global filMessages, ConnexionSocket, CléPrivée, Module, SonActivé, Connexion
    #On récupere les variables nécéssaires au fonctionemment de la fonction
    if Connexion == True:
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

                messageRecu = messageRecu[1].split("/")
                #On transforme le message recu en liste
                #Exemple => "234/23124/34142" donnera la liste ["234", "23124", "34142"]

                messageRecu.remove("")
                #On supprime le dernier index vide de la liste
        
                for index in range (len(messageRecu)):
                #Boucle qui sera executé autant de fois qu'il y'a d'index dans la liste messageRecu

                    messageRecu[index] = int(messageRecu[index])
                    #On transforme l'index de la liste en entier pour pouvoir le déchiffrer

                messageRecu = décryptage(messageRecu, CléPrivée, Module)
                messageRecu = transformationCaratères(messageRecu)
                #On décrypte le message recu, puis ensuite,  on le transforme en caractères

                if len(messageRecu) > 70:
                #Si le message à afficher fait plus de 70 caratères
            
                    listeLignes = couperPhrases(messageRecu)
                    #On recupere plusieurs lignes de moins de 70 caractères dans une liste

                    for ligne in listeLignes:
                    #On insere chaque ligne
                        filMessages.insert(END, ligne)

                else:
                    filMessages.insert(END, messageRecu)
            
                filMessages.yview(END)
                #On insére le message dans la listbox des messages, puis on force le défilement tout en bas de cette dernière

                if SonActivé == True:
                    winsound.PlaySound("Médias/SonMessage.wav", winsound.SND_ASYNC)
            else:
                input("message vide")

        except BlockingIOError:
        #Si aucun message n'a été envoyé, on ne fait rien
            pass

        except (ConnectionAbortedError, ConnectionResetError):
        #Le serveur a crashé

            tkinter.messagebox.showerror(title="Aïe...", message="Le serveur a crashé...")
            exit()
        finally:	
        #Bloc qui sera executé aprés le try ou l'except
            fen.after(10, reception)
            #La fonction s'appelle après 10ms




def placeholder(Provenance):
    
    """ Fonction qui reproduit l'atribut "placeholder" des input HTML. Un suggestions est affiché, quand l'utilisateur clique
    dessus elle disparait"""

    if Provenance == "AppelManuel":
    #Si la fonction a été appellé par une instruction 
        saisieMessage.insert(0, "Saisissez votre message ici")
    else:
    #La fonction a été appellé par un bind, on supprime alors le placeholder
        saisieMessage.delete(0, "end")


def deconnexion():

    global Connexion

    Connexion = False
    ConnexionSocket.close()




def toucheEntre(argumentUseless):
    
    """ Cette fonction sert simplement à contourner un défaut de conception de Tkinter : Les fonctions appellées avec bind le sont
    toujours avec argument qui contient la position de la souris, ce qui pose problème quand la fonction cible ne prend aucun 
    argument"""

    envoyer()

def pasCode():
        """ Fonction qui affiche un message come quoi j'ai eu la flemme de coder la fonction pour le moment"""
        tkinter.messagebox.showwarning(title="Aïe...", message="Cette fonction n'a pas encore été codée")


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

    Confirmation = messagebox.askquestion (f"Vous partez déja {nomUser} ?","Vous voulez vraiment retourner au menu ?",icon = 'warning')
    if Confirmation == 'yes':
        filMessages.pack_forget()
        saisieMessage.pack_forget()
        bouttonEnvoyer.pack_forget()

        fen.unbind_all(ALL)
    
        barreMenu.delete(1)
        barreMenu.delete(1)
        barreMenu.delete(3)

        deconnexion()

        AfficherMenu()



def affichageConversation():
        
    """ Cette fonction sert à générer l'interface de la conversation"""

    global cadreParametres, saisieMessage, nomUser, filMessages, bouttonEnvoyer, Connexion
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

    saisieMessage.bind("<Button-1>", placeholder)
    #On associe le clic gauche sur la zone de saisie du message à la fonction placeholder
    fen.bind_all('<Return>', toucheEntre)
    #On associe l'appui sur la toucheEntre à la fonction toucheEntre

    Connexion = True
    reception()
    #On commence à recevoir des messages
    placeholder("AppelManuel")



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
        données = données.encode('utf-8')

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

            MessageErreur = "Un utilisateur avec le même nom d'utilisateur que le votre est déja connecté. Changez de nom d'utilisateur pour accéder à ce serveur."
            #On raccourci la ligne du dessous avec cette variable
            tkinter.messagebox.showerror(title="Aïe...", message=MessageErreur)	

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

    global entreIP, entrePort, IP, Port, Role
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

    Role = "Hote"
    IP = entreIP.get()
    Port = int(entrePort.get())

    subprocess.Popen(f"python Serveur.py {IP} {Port}")
    #On lance le serveur dans un processus parallèle.

    if connexion() == True:
    #Si la connexion est une réussite, on affiche les conversations
        affichageConversation()



def seConnecter():
        
    """ Fonction qui affiche l'interface de discusion si la connexion est une réussite"""

    global entreIP, entrePort, IP, Port, Role
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction
    
    Role = "Client"
    Port = int(entrePort.get())
    IP = entreIP.get()

    if connexion() == True: 
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

    portRecommande = randint(49152, 65535)
    #On recommande un port dans la plage de ceux les moins utilisés

    entrePort = Entry(cadreParametres)
    entrePort.insert("end", portRecommande)
    entrePort.pack(anchor=CENTER)

    suggestionNom = choices(listeNoms)
    #On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms

    votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
    votreNom.pack(anchor=CENTER, pady=7)

    entreNom = Entry(cadreParametres)
    entreNom.insert("end", suggestionNom)
    entreNom.pack(anchor=CENTER)

    bouttonStart = Button(cadreParametres, text="Démarrer", command=démarrerServeur)
    bouttonStart.pack(pady=20)



def client():
        
    """ Cette fonction permet à un client de se connecter au serveur""" 

    global entreIP, entrePort, entreNom, cadreParametres, listeNoms
    #On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

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

    suggestionNom = choices(listeNoms)
    #On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms

    votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
    votreNom.pack(anchor=CENTER, pady=7)

    entreNom = Entry(cadreParametres)
    entreNom.insert("end", suggestionNom)
    entreNom.pack(anchor=CENTER)

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



fen = Tk()
fen.geometry("550x460")
fen.title("Kripto - Un chat chiffré")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")

barreMenu = Menu(fen)
barreMenu.add_command(label="Aide", command=pasCode)
barreMenu.add_command(label="Paramètres", command=pasCode)
barreMenu.add_command(label="Contact", command=pasCode)
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