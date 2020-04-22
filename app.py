import os
import time
import socket
import platform

#Fonction qui efface l'écran, elle est compatible avec Windows et Linux
def cls():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
#La commande varie selon les os

#On définit la fonction suite pour éviter de se répéter
def suite():
    input("Appuyez sur entrée pour continuer \n")

#La fonction d'aide
def aide():
    print("Bonzouére je suis la fonction d'aide")
    suite()

#La fonction qui parse et traite les commandes
def commandesParseur(commande):
    
    #On efface l'écran
    cls()

    listeCommande = commande.split(" ")
    #On récupere tout les mots séparés par un espace dans la commande dans une liste
    #Exemple : "Bonjour toi !" donnera ["Bonjour", "toi", "!"]
    
    if listeCommande[0] == "/?":
    #Commande d'aide
        aide()
    else:
        print('La commande "' + commande + '" est inconnue ! Aide => "/?"')
        suite()


#On demande à l'utilisateur la commande à exécuter, puis on la passe en paramétre de la fonction commandesParseur()
while True:
    commande = input("Bienvenue dans $_NOMPROJET ! Tapez /? pour obtenir de l'aide \n >>> ")
    commandesParseur(commande)
    cls()
