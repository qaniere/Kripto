# coding: utf8
import time
import math
import socket
import tkinter
import threading
from tkinter import *
from tkinter import messagebox
from Modules import ChiffrementRSA


Débug = True

def log(message):

    """ Fonction qui logge dans un fichier "logs.txt" """

    if Débug:

        fichier = open("logs.txt", "a", encoding="utf-8")
        fichier.write(str(message) + "\n")
        fichier.close()
    return


def Démarrer(IP, Port, NombreClientsMax, MotDePasse):

    global Module, CléPublique, CléPrivée, ClientsMax, listeClient, listeDesPseudos, HoteConnecté, nomClient, RoleClient, CléPubliqueClient, ModuleClient, nombreErreurs, MDP, PrésenceMDP, Statut

    fen = Tk()
    fen.withdraw()
    #On crée une fenêtre qu'on affiche pas pour éviter qu'une fenêtre se génère lors de message d'erreurs

    Module, CléPublique, CléPrivée = ChiffrementRSA.génération(16)
    #On génère notre jeu de clés Privée et Publique, ainsi que notre module de chiffrement

    if NombreClientsMax == "0" or NombreClientsMax == "Inconnu":
        ClientsMax = math.inf

    else:
        ClientsMax = int(NombreClientsMax)
    # On passe par une variable intérmédiaire car on ne peut modifier la portée d'un paramètre

    if MotDePasse != "Inconnu":  
        PrésenceMDP = True     
        MDP = MotDePasse

    else:
        PrésenceMDP = False
        MDP = None


    listeClient = []
    listeDesPseudos = []
    #On initialise la liste qui contient les objets clients, ainsi que la liste de tous les pseudos de
    # tous les clients connectés pour éviter les doublons

    HoteConnecté = False

    nomClient = {}
    RoleClient= {}
    CléPubliqueClient = {}
    ModuleClient = {}
    nombreErreurs = {}
    Statut = {}
    #On initialise des dictionnaires vides qui serviront à récuperer les informations de chaque objet client.
    #Exemple, Marc est un objet client, quand veut récuperer son nom d'utilisateur, on utilise la syntaxe "nomClient[Marc}"

    def arretServeur():

        Serveur.close()
        # Fermeture de la connexion

        exit()


    def envoi(message, type, Envoyeur=None):
    #On rend l'argument Envoyeur facultatif

        """ Cette fonction sert à envoyer des messages au clients connectés"""

        global listeClient
        #On récupere la liste de toute les clients connectés

        for destinataire in listeClient:
        #On désigne les destinaires du message, à savoir tout les clients connectés

            if destinataire != Envoyeur:
            #Si le destinaire n'est pas l'expéditeur

                messageEnvoi = ChiffrementRSA.chiffrement(message, CléPubliqueClient[destinataire], ModuleClient[destinataire])
                #On transforme les caractéres du message en chiffre selon leur ID Unicode, puis ensuite on chiffre le message
                #Avec la clé publiq ue et le module de chaque client

                ChaineMessage = f"{len(messageEnvoi)}-{messageEnvoi}"
                messageEnvoi = ChaineMessage.encode('utf-8')
                destinataire.send(bytes(messageEnvoi))
                #On encode le tout en UTF8 et on l'envoi au client


    def Déconnexion(Client):

        """ Fonction qui supprimme des variables du serveur les infos d'un client qui vient de se déconnecter """

        if RoleClient[Client] == "Client":
            annonce = f"[{time.strftime('%H:%M:%S')}] {nomClient[Client]} vient de se déconnecter"
            print(annonce)
            log(annonce)

            listeClient.remove(Client)
            listeDesPseudos.remove(nomClient[Client])
            del nomClient[Client]
            del CléPubliqueClient[Client]
            del RoleClient[Client]
            #On supprime les informations du client déconnecté
            #On utilise le mot clé del plutot que d'affecter une valeur vide car sinon la clé resterait conservée en mémoire

            envoi(annonce, "Annonce")
            #On envoi l'annonce aprés avoir supprimé les infos du client car sinon il serait sur la liste d'envoi
        else:
            annonce = f"[{time.strftime('%H:%M:%S')}] {nomClient[Client]} vient d'arrêter le serveur."
            log(annonce)

            listeClient.remove(Client)
            listeDesPseudos.remove(nomClient[Client])
            del nomClient[Client]
            del CléPubliqueClient[Client]
            del RoleClient[Client]
            del nombreErreurs[Client]
            #On vide tout les données de l'hôte

            envoi(annonce, "Annonce")

            arretServeur()



    Serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini les paramêtres du socket

    try:
        Serveur.bind((IP, Port))
    except OSError:
    #Si jamais le lancement du serveur échoue (IP Invalide), on affiche un message d'erreur
        tkinter.messagebox.showerror(title="Aïe...", message="IL semblerait que votre IP ne soit pas valide. Réferez vous à l'aide pour régler ce problème.")
        log("Erreur - IP invalide")
    else:
        #On configure le serveur en mode non-bloquant : Au lieu d'attendre une réponse et de bloquer le programme, l'instruction retourne
        #une exeception si jamais aucune données n'est envoyée, ce qui empecherait la gestion de plusieurs clients
        Serveur.setblocking(0)

        #Démarrage du serveur
        Serveur.listen()
        annonce = "Serveur démarré à " + time.strftime("%H:%M:%S") + " sur le port " + str(Port)
        print(annonce)
        log(annonce)
        

        def FonctionServeur():

            global HoteConnecté, listeClient, listeDesPseudos, nomClient, RoleClient, CléPubliqueClient, ModuleClient, nombreErreurs, ClientsMax, MDP, PrésenceMDP, Statut
            
            while True:
                try:
                    objetClient, IPClient = Serveur.accept()
                    #On accepte chaque connexion et on récupere les infos du client dans "objetClient"
                    #Et son IP et son port dans IPClient

                    données = objetClient.recv(32768)
                    données = données.decode("utf-8")
                    #On recoit et on convertir les données du client
                    log("Données recues ==> " + données)

                    données = données.split("|")
                    #On transforme ces données en liste

                    if données[0] not in listeDesPseudos and ClientsMax >= len(listeClient) +1:
                        
                        objetClient.send(bytes(f"{str(CléPublique)}|{str(Module)}|{str(PrésenceMDP)}", "utf-8"))
                        #On envoi au client les informations de chiffremment du serveur

                        nomClient[objetClient] = données[0]
                        CléPubliqueClient[objetClient] = int(données[1])
                        ModuleClient[objetClient] = int(données[2])
                        #On récupere les informations du client dans les dictionnaires adéquats

                        nombreErreurs[objetClient] = 0
                        #On initialise le nombre d'erreurs

                        listeDesPseudos.append(données[0])
                        #On ajoute son pseudo à la liste

                        if PrésenceMDP == None:
                            Statut[objetClient] = "Connecté"

                        else:
                            Statut[objetClient] = "Attente"


                        if HoteConnecté == False:
                        #Si c'est la première connexion, on précise que c,'est l'hôte
                            RoleClient[objetClient] = "Hôte"
                            print(f"[{time.strftime('%H:%M:%S')}] L'hôte vient de se connecter")
                            log(f"[{time.strftime('%H:%M:%S')}] L'hôte vient de se connecter")
                            HoteConnecté = True

                        else:
                        #Sinon c'est un client

                            RoleClient[objetClient] = "Client"
                            annonce = f"[{time.strftime('%H:%M:%S')}] {nomClient[objetClient]} vient de rejoindre le chat"
                            log(annonce)
                            print(annonce)
                            envoi(annonce, "Annonce")

                        listeClient.append(objetClient)
                        #On stocke l'objet client
                    elif données[0] in listeDesPseudos:
                    #Si le nom est déja pris

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.4) #Le délai évite que les message de mélangent
                        objetClient.send(bytes("Votre nom d'utilisateur est déja utilisé dans ce serveur, veuillez en changer.", "utf-8"))
  
                    elif ClientsMax < len(listeClient) + 1:
                    #Si le serveur est complet

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.4)
                        objetClient.send(bytes("Le serveur a atteint sa capacité maximale", "utf-8"))


                except IOError:
                #Si personne n'essaie de se connecter, on ne fait rien
                    pass

                for client in listeClient:
                #On récupere chaque client dans la liste des clients connectés

                    try:
                    #Si un message est envoyé, on le récupere, sinon l'instruction génére une exception

                        if Statut[client] == "Connecté":

                            message = client.recv(32768) #L'argument dans la fonction recv définit combien de caractères on reçoit
                            message = message.decode("utf-8")
                            #On recoit le message et on le décode
                            log("Message recu ==> " + message)

                            message = message.split("-")
                            #Le message comporte un petit entête
                            #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message. Cela peut arriver que les très long messages (Fichiers) fassent plus
                            #de 2048 la taille taille du buffer


                            LongeurMessage = int(message[0])

                            while len(message[1]) < LongeurMessage:
                            #Tant que le message recu est plus petit que la longueur totale du message

                                suite = client.recv(32768)
                                suite = suite.decode("utf-8")

                                message[1] += suite
                                #On ajoute la suite du message recu

                            #A ce stade le message est complet

                            message = ChiffrementRSA.déchiffrement(message[1], CléPrivée, Module)
                            #On ne déchiffre que l'index 1 du message, qui est le messge en lui même
                            #0 étant la longueur de ce message
                            log("Message déchiffré = " + message)

                            if message == "":
                            #Le message recu vide, la connexion à été temporairement perdue
                            #Au bout d'un nombre défini d'exceptions, on déconnecte le client

                                if nombreErreurs[client] < 5:
                                    log("Une erreur pour " + nomClient[client])
                                    nombreErreurs[client] += 1
                                else:
                                    log("Lancement de la procédure de déconnexion pour " + nomClient[client])
                                    Déconnexion(client)

                            else:
                            #Si le message n'est pas vide

                                nombreErreurs[client] = 0
                                #On remet à zéro le nombre d'erreurs

                                MessageListe = message.split("|")
                                Type = MessageListe[0]
                                #On récupere le message sous forme de liste afin de déterminer son type

                                if Type == "Message":
                                        HeureMessage = MessageListe[1]
                                        Contenu = MessageListe[2]
                                        #On récupere les information du message

                                        messageFormaté = f"[{HeureMessage}] {nomClient[client]} → {Contenu}"
                                        print(messageFormaté)
                                        envoi(messageFormaté, "Message", client)

                                else:
                                #Si le message recu ne respecte aucune forme de message, il est invalide
                                #Cela peut être du a un client pas à jour, ou bien une tentative de connexion frauduleuse

                                    print(f"Message invalide recu ! => {message} - Expéditeur => {IPClient[0]} ")
                                    log(f"Message invalide recu ! => {message} - Expéditeur => {IPClient[0]} ")

                        else:
                        #Si le client doit rentrer son mot de passe

                            MotDePasseClient = client.recv(4096)
                            MotDePasseClient = MotDePasseClient.decode("utf-8")

                            if MotDePasseClient == MDP:

                                client.send(bytes("OK", "utf-8"))         
                                Statut[client] = "Connecté"

                            else:
                                client.send(bytes("Nan", "utf-8")) 
                                

                    except BlockingIOError:
                    # Si aucun message n'a été envoyé, on temporise pour éviter de trop consommer des ressources
                    # Exemple, sans temporisation, 38% du processeur, on passe à peine 1% avec un délai non ressenti
                
                        time.sleep(0.1)

                    except ConnectionResetError:
                    #Si jamais un des clients s'est déconnecté
                        log("Déconnexion de " + nomClient[client])
                        Déconnexion(client)

                
        threadServeur = threading.Thread(target=FonctionServeur)
        threadServeur.daemon = True #Ce flag signifie que quand il ne reste que ce thread, le programme s'arrête.
        threadServeur.start()
