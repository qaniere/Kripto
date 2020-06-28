# coding: utf8
import time
import tkinter
import platform
import webbrowser
from tkinter import *
from tkinter import messagebox

TrouverOS = lambda : platform.system() + " " + platform.release()

if TrouverOS() == "Windows 10":
#L'utilisateur est éligibles au notifications

    from win10toast import ToastNotifier
    toaster = ToastNotifier()

    NotificationActivées = True


""" Certains fonctions sont définies ici pour alléger le code de l'application """

def formaterPaquet(TypePaquet, Contenu):
        
    """
    Fonction qui permer de formater les messages selon des régles spécifiques pour optimiser le traitement coté 
    serveur.

        - Message : TypeDePaquet|HeureEnvoi|ContenuDuMessage
        - Commande : TypeDePaquet|HeureExecution|Commande

    """

    if TypePaquet == "Message":
    
        Paquet = f"Message|{time.strftime('%H:%M:%S')}|{Contenu}"

    elif TypePaquet == "Commande":
        
        Contenu = Contenu.replace("/", "")
        Paquet = f"Commande|{time.strftime('%H:%M:%S')}|{Contenu}"

    return Paquet


def traitementPhrase(chaine):
    
    """Cette fonction traite une chaine en la coupant en deux au 
    bout de 50 caractéres. Elle retourne deux variables, la premiere
    la chaine de moins de 51 caracteres et le reste. Il convient donc
    d'executer la fonction autant que nécéssaire"""
    
    listeMots = chaine.split(" ")
    #On transforme la chaine en liste 
    #Exemple => "Hello World !" ==> ["Hello", "World", "!"]

    Ligne = ""
    while len(Ligne) < 70:
    #Tant qu'il y a de la place dans la variable Ligne
        if Ligne == "":
            Ligne += listeMots.pop(0)
        else:
            Ligne += " " + listeMots.pop(0)
    #On ajout le premier index de chaque ligne avec la méthode pop,
    #ce qui le supprime de la liste

    chaine = ""
    #On vide la variable chaine
    Ligne = Ligne.split(" ")
    #On retransorme la chaine en liste pour retire le dernier mot

    listeMots.insert(0, Ligne.pop(-1))
    #On supprime ce mot et on l'insére dans le reste

    for index in range(len(Ligne)):
    #On transforme la liste en chaine
        if chaine == "":
            chaine += Ligne.pop(0)
        else:
            chaine += " " + Ligne.pop(0)

    MotsRestants = ""

    for index in range(len(listeMots)):
    #On transforme la liste des mots en restant en chaine
        if MotsRestants == "":
            MotsRestants += listeMots.pop(0)
        else:
            MotsRestants += " " + listeMots.pop(0)
 
    return chaine, MotsRestants


def couperPhrases(chaine):

    """ Cette fonction sert à appeller la fonction "TraitementPhrase"
    autant de fois que nécéssaire"""

    def SeparerCara(chaine):
        """ Fonction retourne un liste de tout les caractères d'une chaine """
        return [ch for ch in chaine]

    chaineSéparé = chaine.split("→")
    #On sépare la chaine pour vérifier le message contient des espaces, sans prendre en compte le header
    #Header => "[12:04:23] Auteur du message →"

    résultat = []

    if " " in chaineSéparé:
    #Si le texte contient des espaces et que c'est pas "fzjkrzkfpozeijfoijfpofjzeoif"
    
        NonTraité = chaine
        #On initialise la variable

        while len(NonTraité) > 70:
        #Tant qu'il reste un ligne de plus de 50 caractéres

            Ligne, NonTraité = traitementPhrase(NonTraité)
            #On récupere un ligne de 50 caractères maximums et un autre
            #ligne qu'on va retraitre si elle fait plus de 50 caratères

            résultat.append(Ligne)
            #On ajoute la ligne de moins de 50 caratères à un liste
            #résulat qu'on retournera
     
        résultat.append(NonTraité)
        #On ajoute le reste de moins de 50
    else:
        chaine = SeparerCara(chaine)
        #Transforme le message liste en séparant chaque caractères

        ligne = ""
        
        while chaine != []:

            ligne += chaine.pop(0)
            #On ajoute à la nouvelle ligne le premier index de la liste qu'on supprime de cette dernière

            if len(ligne) == 70:
            #Un fois que la nouvelle ligne fait la bonne taille

                résultat.append(ligne)
                ligne = ""
                #On ajoute la ligne au résultat et on la remet à zéro
        
        résultat.append(ligne)
        #On ajoute la ligne même si elle fait pas 70 caratères une fois sorti du while

    return résultat

def placeholder(zone, nouveauTexte, premiereFois):

    if premiereFois == True:
        #Si c'est le message de base, on le sauvegarde et ensuite on l'insére

        texteDeBase[zone] = nouveauTexte
        zone.insert("0", nouveauTexte)

    else:
        texteActuel = zone.get()
        #On récupere le texte de la zone de saisie

        if texteActuel == texteDeBase[zone]:
        #Si le texte présent actuelement dans la zone de saisie est le texte défini lors de la création du placeholder
            zone.delete("0", END)

            zone.unbind("<Button-1>")
            #On supprime le bind de la zone d'entrée afin que l'utilisateur puisse saisir le texte initial du placeholder
            #si il le souhaite

def callback(url):
    """ Fonction qui permet de suivre un url """
    webbrowser.open_new(url)


def AfficherNotification(Titre, Message):

    if NotificationActivées:

        toaster.show_toast(
            Titre,
            Message,
            icon_path = "Médias/icone.ico",
            duration = 6,
            threaded = True #Non bloquant
        ) 

def ParserCommande(Commande):

    """ Retourne la commande et son deuxième argument. Exemple /ban Jean Michel retourne "/ban", "Jean Michel """

    Commande = Commande.split(" ")
    PremierArgument = Commande.pop(0)
    DeuxièmeArgument = " ".join(Commande)

    return PremierArgument, DeuxièmeArgument

texteDeBase = {}
#Initialision du dico néccessaire pour la fonction placeholder
