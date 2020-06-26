# coding: utf8
import sys
import time
import socket
import tkinter
import threading
from math import inf
from tkinter import *
from tkinter import messagebox
from Modules import ChiffrementRSA



def ArrêtServeur():

    ConnexionSocket.close()
    # Fermeture de la connexion
    sys.exit()


def Démarrer(IP, Port, NombreClientsMax, MotDePasse):

    def Déconnexion(Client, Silencieux = False):

        """ Fonction qui supprimme des variables du serveur les infos d'un client qui vient de se déconnecter. Quand le paramètre 
        silencieux est égal à true, aucune annonce n'est faite """

        #global ListeDesClientsConnectés, ListeDesPseudos, Nom, CléPublique, ModuleDeChiffrement, Rôle, Statut

        if Rôle[Client] == "Hôte": HôteVientDePartir = True
        else: HôteVientDePartir = False

        if Rôle[Client] == "Client" and Silencieux == False:
            annonce = f"[{time.strftime('%H:%M:%S')}] {Nom[Client]} vient de se déconnecter"
            print(annonce)

        elif Silencieux == False:
            annonce = f"[{time.strftime('%H:%M:%S')}] {Nom[Client]} vient d'arrêter le serveur."

        ListeDesClientsConnectés.remove(Client)
        ListeDesPseudos.remove(Nom[Client])
        del Nom[Client]
        del CléPublique[Client]
        del ModuleDeChiffrement[Client]
        del Rôle[Client]
        del Statut[Client]
        #On supprime les informations du client déconnecté
        #On utilise le mot clé del plutot que d'affecter une valeur vide car sinon la clé resterait conservée en mémoire

        if Silencieux == False: Envoi(annonce, "Annonce")
        #On envoi l'annonce aprés avoir supprimé les infos du client car sinon il serait sur la liste d'envoi

        if HôteVientDePartir: ArrêtServeur()


    def Envoi(message, type, Envoyeur = None):
        #On rend l'argument Envoyeur facultatif pour que les annonces soit envoyées à tout le monde

        """ Cette fonction sert à envoyer des messages au clients connectés"""

        global ListeDesClientsConnectés
        #On récupere la liste de toute les clients connectés

        for destinataire in ListeDesClientsConnectés:
        #On désigne les destinaires du message, à savoir tout les clients connectés

            if destinataire != Envoyeur:
            #Si le destinaire n'est pas l'expéditeur

                messageEnvoi = ChiffrementRSA.chiffrement(message, CléPublique[destinataire], ModuleDeChiffrement[destinataire])
                #On transforme les caractéres du message en chiffre selon leur ID Unicode, puis ensuite on chiffre le message
                #Avec la clé publiq ue et le module de chaque client

                ChaineMessage = f"{len(messageEnvoi)}-{messageEnvoi}"
                messageEnvoi = ChaineMessage.encode('utf-8')
                destinataire.send(bytes(messageEnvoi))
                #On encode le tout en UTF8 et on l'envoi au client

    #Début du code de la fonction démarrer serveur
    global Module, CléPubliqueServeur, CléPrivée, ClientsMax, ListeDesClientsConnectés, ListeDesPseudos, HôteConnecté, Nom, Rôle
    global CléPublique, ModuleDeChiffrement, MDP, PrésenceMDP, Statut, ConnexionSocket, ServeurVerrouilé

    fen = Tk()
    fen.withdraw()
    #On crée une fenêtre qu'on affiche pas pour éviter qu'une fenêtre se génère lors de message d'erreurs

    Module, CléPubliqueServeur, CléPrivée = ChiffrementRSA.génération(16)
    #On génère notre jeu de clés Privée et Publique, ainsi que notre module de chiffrement

    if NombreClientsMax == "0" or NombreClientsMax == "Inconnu":
        ClientsMax = inf
        #On utilise l'infini car si on cherche à vérifier si la limite à été dépassée, le résultat sera toujours 
        
    else: ClientsMax = int(NombreClientsMax)
    # On passe par une variable intérmédiaire car on ne peut modifier la portée d'un paramètre

    HôteConnecté = False
    ServeurVerrouilé = False

    if MotDePasse != "Inconnu":  
        PrésenceMDP = True     
        MDP = MotDePasse

    else:
        PrésenceMDP = False
        MDP = None


    ListeDesClientsConnectés = []
    ListeDesPseudos = []
    #On initialise la liste qui contient les objets clients, ainsi que la liste de tous les pseudos de
    #tous les clients connectés pour éviter les doublons

    Nom = {} #Le nom d'utilisateur
    Rôle= {} #Hôte ou admin
    CléPublique = {} #Sa clé de chiffrement RSA
    ModuleDeChiffrement = {}
    Statut = {}
    #On initialise des dictionnaires vides qui serviront à récuperer les informations de chaque objet client.
    #Exemple, Marc est un objet client, quand veut récuperer son nom d'utilisateur, on utilise la syntaxe "Nom[Marc}"


    ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On défini les paramêtres du socket

    try: ConnexionSocket.bind((IP, Port))
    except OSError:
    #Si jamais le lancement du serveur échoue (IP Invalide), on affiche un message d'erreur
        tkinter.messagebox.showerror(title="Aïe...", message="IL semblerait que votre IP ne soit pas valide. Réferez vous à l'aide pour régler ce problème.")

    else:
        #On configure le serveur en mode non-bloquant : Au lieu d'attendre une réponse et de bloquer le programme, l'instruction retourne
        #une exeception si jamais aucune DonnéesDuClient n'est envoyée, ce qui empecherait la gestion de plusieurs clients
        ConnexionSocket.setblocking(0)

        #Démarrage du serveur
        ConnexionSocket.listen()
        print("Serveur démarré à " + time.strftime("%H:%M:%S") + " sur le port " + str(Port))        

        def FonctionServeur():
        #La fonction qui tourne en boucle tant que le serveur est démarré

            global HôteConnecté, ListeDesClientsConnectés, ListeDesPseudos, Nom, Rôle, CléPublique, ModuleDeChiffrement
            global ClientsMax, MDP, PrésenceMDP, Statut, ServeurVerrouilé
            
            while True:

                try: objetClient, IPClient = ConnexionSocket.accept()
                #On accepte chaque connexion et on récupere les infos du client dans "objetClient"
                #Et son IP et son port dans IPClient

                except IOError:
                #Si personne n'essaie de se connecter, on ne fait rien
                    pass
                
                else:
                #Connexion d'un client

                    DonnéesDuClient = objetClient.recv(32768)
                    DonnéesDuClient = DonnéesDuClient.decode("utf-8")
                    #On recoit et on convertir les données du client

                    DonnéesDuClient = DonnéesDuClient.split("|")
                    #On transforme ces données en liste

                    if DonnéesDuClient[0] not in ListeDesPseudos and ClientsMax >= len(ListeDesClientsConnectés) + 1 and ServeurVerrouilé == False:
                    #Si le pseudo n'est pas utilité et qu'il reste de la place dans le serveur
                        
                        objetClient.send(bytes(f"{str(CléPubliqueServeur)}|{str(Module)}|{str(PrésenceMDP)}", "utf-8"))
                        #On envoi au client les informations de chiffremment du serveur

                        Nom[objetClient] = DonnéesDuClient[0]
                        CléPublique[objetClient] = int(DonnéesDuClient[1])
                        ModuleDeChiffrement[objetClient] = int(DonnéesDuClient[2])

                        ListeDesPseudos.append(DonnéesDuClient[0])

                        if PrésenceMDP == False: Statut[objetClient] = "Connecté"

                        else: Statut[objetClient] = "Attente"

                        if HôteConnecté == False:
                        #Si c'est la première connexion, on précise que c'est l'hôte

                            HôteConnecté = True
                            Rôle[objetClient] = "Hôte"
                            Statut[objetClient] = "Connecté" #L'hôte est toujours connecté, pas besoin de mot de passe
                            print(f"[{time.strftime('%H:%M:%S')}] L'hôte {Nom[objetClient]} vient de se connecter")
                            
                        else:
                        #Sinon c'est un client

                            Rôle[objetClient] = "Client"

                            if PrésenceMDP == False:

                                annonce = f"[{time.strftime('%H:%M:%S')}] {Nom[objetClient]} vient de rejoindre le chat"
                                print(annonce)
                                Envoi(annonce, "Annonce")

                        ListeDesClientsConnectés.append(objetClient)

                    elif DonnéesDuClient[0] in ListeDesPseudos:
                    #Si le nom est déja pris

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.5) #Le délai évite que les paquets se mélangent
                        objetClient.send(bytes("Votre nom d'utilisateur est déja utilisé dans ce serveur, veuillez en changer.", "utf-8"))
  
                    elif ClientsMax < len(ListeDesClientsConnectés) + 1:
                    #Si le serveur est complet

                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.4)
                        objetClient.send(bytes("Le serveur a atteint sa capacité maximale", "utf-8"))

                    elif ServeurVerrouilé:
                        objetClient.send(bytes("False", "utf-8"))
                        time.sleep(0.4)
                        objetClient.send(bytes("Le serveur est verrouilé", "utf-8"))

                for client in ListeDesClientsConnectés:
                #On récupere chaque client dans la liste des clients connectés

                    try:
                    #Si un message est envoyé, on le récupere, sinon l'instruction génére une exception

                        if Statut[client] == "Connecté":

                            message = client.recv(32768) #L'argument dans la fonction recv définit combien de caractères on reçoit
                            message = message.decode("utf-8")
                            #On recoit le message et on le décode

                    except BlockingIOError:
                    # Si aucun message n'a été envoyé, on temporise pour éviter de trop consommer des ressources
                    # Exemple, sans temporisation, 38% du processeur, on passe à peine 1% avec un délai non ressenti
                
                        time.sleep(0.1)

                    except ConnectionResetError:
                    #Si jamais un des clients s'est déconnecté
                        Déconnexion(client)
                    else:
                    #Le serveur a recu un mesage

                            if Statut[client] == "Connecté":

                                message = message.split("-")
                                #Le message comporte un petit entête
                                #Exemple = 564-6646464/65656/4564564654, 564 est içi la longueur totale du message. Cela peut arriver que les très long messages (Fichiers) fassent plus
                                #de 2048 la taille taille du buffer

                                if message[0] == "":
                                #Si le message recu  est vide la connexion a été  perdue
                                    Déconnexion(client)

                                else:
                                #Si le message n'est pas vide
                        
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
     
                                    MessageListe = message.split("|")
                                    Type = MessageListe[0]
                                    #On récupere le message sous forme de liste afin de déterminer son type

                                    if Type == "Message":

                                            HeureMessage = MessageListe[1]
                                            Contenu = MessageListe[2]

                                            messageFormaté = f"[{HeureMessage}] {Nom[client]} → {Contenu}"
                                            print(messageFormaté)
                                            Envoi(messageFormaté, "Message", client)

                                    elif Type == "Commande":

                                        HeureCommande = MessageListe[1]
                                        Commande = MessageListe[2]

                                        if Commande == "stop":

                                            if Rôle[client] == "Hôte":
                                                
                                                Envoi(f"[{HeureCommande}] {Nom[client]} vient d'arrêter le serveur", "Annonce")
                                                ArrêtServeur()

                                        elif Commande == "lock":

                                            if Rôle[client] == "Hôte":
                                                
                                                Envoi(f"[{HeureCommande}] {Nom[client]} vient de verrouiler le serveur", "Annonce")
                                                ServeurVerrouilé = True

                                        elif Commande == "unlock":

                                            if Rôle[client] == "Hôte":
                                                
                                                Envoi(f"[{HeureCommande}] {Nom[client]} vient de déverrouiler le serveur", "Annonce")
                                                ServeurVerrouilé = False

                                    else:
                                    #Si le message recu ne respecte aucune forme de message, il est invalide
                                    #Cela peut être du a un client pas à jour, ou bien une tentative de connexion frauduleuse

                                        print(f"Message invalide recu ! => {message} - Expéditeur => {IPClient[0]} ")

                    try:
                        if Statut[client] == "Attente":
                        #Si le client doit rentrer le mot de passe du serveur
                            MotDePasseClient = client.recv(4096)

                    except BlockingIOError: pass
                    except ConnectionResetError: Déconnexion(client, Silencieux = True)
                    #Si jamais un des clients s'est déconnecté
        
                    except KeyError: pass
                    #Cette erreur se produit une seule fois, quand un client se déconnecte ses informations sont supprimées
                    #mais avec un délai, donc cela génére une erreur une fois par déconnexion
            
                    else:
                        if Statut[client] == "Attente":
                        #Si on recoit un mot de passe

                            MotDePasseClient = MotDePasseClient.decode("utf-8")

                            if MotDePasseClient == "": 
                            #Le client s'est déconnecté avant d'envoyer son mot d passe
                                Déconnexion(client, Silencieux = True)

                            else:

                                MotDePasseClient = ChiffrementRSA.déchiffrement(MotDePasseClient, CléPrivée, Module)

                                if MotDePasseClient == MDP:

                                    client.send(bytes("OK", "utf-8"))         
                                    Statut[client] = "Connecté"

                                    annonce = f"[{time.strftime('%H:%M:%S')}] {Nom[client]} vient de rejoindre le chat"
                                    print(annonce)
                                    Envoi(annonce, "Annonce")

                                else:
                                    client.send(bytes("Nan", "utf-8"))
                                
                
        threadServeur = threading.Thread(target=FonctionServeur)
        threadServeur.daemon = True #Ce flag signifie que quand il ne reste que ce thread, le programme s'arrête.
        threadServeur.start()
