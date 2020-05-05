# coding: utf8
import sys
import time
import socket
import tkinter
from tkinter import *
from ChiffrementRSA import *
from tkinter import messagebox

fen = Tk()
fen.withdraw()
#On crée une fenêtre qu'on affiche pas pour éviter qu'une fenêtre se génère lors de message d'erreurs

global Module, CléPublique, CléPrivée
Module, CléPublique, CléPrivée = génération(16)
#On génère notre jeu de clés Privée et Publique, ainsi que notre module qu'on rend accesible à tout le programme avec Global


listeClient = []
listeDesPseudos = []
#On initialise la liste qui contient les objets clients, ainsi que la liste de toute des pseudos de 
# tout les clients connectés pour éviter les doublons

nomClient = {}
RoleClient= {}
CléPubliqueClient = {}
ModuleClient = {}
#On initialise des dictionnaires vides qui serviront à récuperer les informations de chaque objet client.
#Exemple, Marc est un objet client, quand veut récuperer son nom d'utilisateur, on utilise la syntaxe "nonClient[Marc}"


IP = sys.argv[1]
Port = int(sys.argv[2])
#On récuperer les arguments de lancement du script sous forme de liste
#Par exemple => "script.py", un seul argument, "script.py argument2, argument3" 3 arguments

def envoi(message, type):
        
    """ Cette fonction sert à envoyer des messages au clients connectés"""

    global listeClient
    #On récupere la liste de toute les clients connectés

    for destinataire in listeClient:
    #On désigne les destinaires du message, à savoir tout les clients connectés
    
        if destinataire != client:
        #Si le destinaire n'est pas l'expéditeur

            messageEnvoi = transformationChiffres(message)
            messageEnvoi = cryptage(messageEnvoi, CléPubliqueClient[destinataire], ModuleClient[destinataire])
            #On transforme les caractéres du message en chiffre selon leur ID Ascii, puis ensuite on chiffre le message
            #Avec la clé publique et le module de chaque client

            #On récupere alors un liste d'entiers
            
            ChaineMessage = ""

            for index in messageEnvoi:
            #On récupere tour à tour chaque index de la liste messageEnvoi
                ChaineMessage += str(index) + "/"
                #On ajoute à la variable vide chaque index qu'on converti en texte et on insére un / pour pouvoir les redécouper
            
            messageEnvoi = ChaineMessage.encode('utf-8')
            destinataire.send(bytes(messageEnvoi))
            #On encode le tout en UTF8 et on l'envoi au client

        elif type == "Annonce":
        #Si on veut envoyer une annonce, on utilise cette boucle car tout le monde est concerné
            
            messageEnvoi = transformationChiffres(message)
            messageEnvoi = cryptage(messageEnvoi, CléPubliqueClient[destinataire], ModuleClient[destinataire])
            #On transforme les caractéres du message en chiffre selon leur ID Ascii, puis ensuite on chiffre le message
            #Avec la clé publique et le module de chaque client
            
            ChaineMessage = ""

            #On récupere alors un liste d'entiers

            for index in messageEnvoi:
            #On récupere tour à tour chaque index de la liste messageEnvoi
                ChaineMessage += str(index) + "/"
                #On ajoute à la variable vide chaque index qu'on converti en texte et on insére un / pour pouvoir les redécouper
            
            messageEnvoi = ChaineMessage.encode('utf-8')
            destinataire.send(bytes(messageEnvoi))
            #On encode le tout en UTF8 et on l'envoi au client

#On défini les paramêtres du socket 

Serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    Serveur.bind((IP, Port))

except OSError:
#Si jamais le lancement du serveur échoue (IP Invalide), on affiche un message d'erreur
    tkinter.messagebox.showerror(title="Aïe...", message="IL semblerait que votre IP ne soit pas valide. Réferez vous à l'aide pour régler ce problème.")
else:
    #On configure le serveur en mode non-bloquant : Au lieu d'attendre une réponse et de bloquer le programme, l'instruction retourne
    #une exeception si jamais aucune données n'est envoyée, ce qui empecherait la gestion de plusieurs clients
    Serveur.setblocking(0)

    #Démarrage du serveur
    Serveur.listen()
    print("Serveur démarré à", time.strftime("%H:%M:%S"), "sur le port", Port)

    while True:
    #Si il y'a une nouvelle connnexion, on traite la connexion
        try:
            objetClient, IPClient = Serveur.accept()
            #On accepte chaque connexion et on récupere les infos du client dans "objetClient"
            #Et son IP et son port dans IPClient
            

            données = objetClient.recv(2048)
            données = données.decode("utf-8")
            #On recoit et on convertir les données du client	

            données = données.split("|")
            #On transforme ces données en liste

            if données[0] not in listeDesPseudos:
            #Si un autre utilisateur est déja connecté avec le même nom d'utilisateur
                    
                objetClient.send(bytes(f"{str(CléPublique)}|{str(Module)}", "utf-8"))
                #On envoi au client les informations de chiffremment du serveur
                
                nomClient[objetClient] = données[0]
                CléPubliqueClient[objetClient] = int(données[1])
                ModuleClient[objetClient] = int(données[2])
                #On récupere les informations du client dans les dictionnaires adéquats

                listeDesPseudos.append(données[0])
                #On ajoute son pseudo à la liste

                if listeClient == []:
                #Si c'est la première connexion, on précise que c,'est l'hôte
                    RoleClient[objetClient] = "Hôte"
                    print(f"[{time.strftime('%H:%M:%S')}] L'hôte vient de se connecter")

                else:
                #Sinon c'est un client

                    RoleClient[objetClient] = "Client"
                    annonce = f"[{time.strftime('%H:%M:%S')}] {nomClient[objetClient]} vient de rejoindre le chat"
                    print(annonce)
                    envoi(annonce, "Annonce")

                listeClient.append(objetClient) 
                #On stocke l'objet client
            else:
                objetClient.send(bytes("False", "utf-8"))
                #Sinon on envoi au client l'interdeiction de se connecter
            
        except IOError:
        #Si personne n'essaie de se connecter, on ne fait rien et on ralenti le programme pour préserver les ressources de la machine
            time.sleep(0.1)
    
        for client in listeClient:
        #On récupere chaque client dans la liste des clients connectés
        
            
            try:
            #Si un message est envoyé, on le récupere, sinon l'instruction génére une exception

                message = client.recv(2048)
                message = message.decode("utf-8")
                #On recoit le message et on le décode

                message = message.split("/")
                message.remove("")
                #On le transforme en liste et on enleve le dernier index vide

                for index in range (len(message)):
                #Pour chaque index de la liste, on le transforme en entier
                    message[index] = int(message[index])

                message = décryptage(message, CléPrivée, Module)
                message = transformationCaratères(message)
                #On déchiffre le message puis on le retransforme en caractéres

                if message == "":
                    print("Message vide")

                else:
                #Si le message n'est pas vide

                    MessageListe = message.split("|")
                    Type = MessageListe[0]
                    #On récupere le message sous forme de liste afin de déterminer son type

                    if Type == "Message":
                            LongueurMessage =  MessageListe[1]
                            HeureMessage = MessageListe[2]
                            Expediteur = MessageListe[3]
                            Contenu = MessageListe[4]
                            #On récupere les information du message

                            messageFormaté = f"[{HeureMessage}] {Expediteur} → {Contenu}"
                            print(messageFormaté)
                            envoi(messageFormaté, "Message")

                    else:
                    #Si le message recu ne respecte aucune forme de message, il est invalide
                    #Cela peut être du a un client pas à jour

                        print(f"Message invalide recu ! => {message} - Expéditeur => {IPClient} ")

            except BlockingIOError:
            #Si aucun message n'a été envoyé
                pass

            except ConnectionResetError:
            #Si jamais un des clients s'est déconnecté

                annonce = f"[{time.strftime('%H:%M:%S')}] {nomClient[client]} vient de se déconnecter"
                print(annonce)

                listeClient.remove(client)
                listeDesPseudos.remove(nomClient[client])
                del nomClient[client]
                del CléPubliqueClient[client]
                del RoleClient[client]
                #On supprime les informations du client déconnecté

                envoi(annonce, "Annonce")
                #On envoi l'annonce aprés avoir supprimé les infos du client car sinon il serait sur la liste d'envoi