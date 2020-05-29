# coding: utf8
import time
import codecs
import hashlib
from os import makedirs


#TODO - J'ai supprimé le message au lecteur car jugé inutile par monsieur Germant


#TODO - J'ai aussi supprimer ce genre de commentaires pour la même raison
### Définition de la fonction de chiffrement ### 


def transformationChiffres(chaine):

    """Fonction qui renvoi sous forme de la liste d'entiers correspont chacun à la valeur
    unicode des caratères de la chaine précisée en arguments """ 
    #TODO - Chiffré ne veut pas dire transformer en chiffres 
    #TODO - Lis ce lien : https://chiffrer.info/

    liste = list(chaine) #TODO - Fonction évidente, pas besoin d'expliquer

    for index in range(len(liste)):
    #On récupere chaque caratères de la liste

        liste[index] = ord(liste[index])
        # ord(x) est la fonction qui pour tout charactère Unicode (sous type str) x renvoie sa valeur Unicode
        # Cette fonction transforme donc le message en une suite de chiffres qui correspond à leur valeur Unicode

    #TODO, Bravo, appart l'utilisation de i au lieu d'index c'est une partie bien commentée
        
    return liste
    #On renvoi la liste des caractères au format 



def transformationCaratères(ListeUnicode):

    """Fonction qui convertit la liste de numéros Unicode en une chaine de caractères
    correspondant à chacun des numéros convertis et mis bout à bout""" 

    for index in range(len(ListeUnicode)):

        #Boucle de sécurité : Si jamais on doit convertir des nombres 
        #ne rentrant pas dans la table de caractères Unicode
        
        if ListeUnicode[index] > 1114111 :

            ListeUnicode[index] = ListeUnicode[index] - 1114111 #TODO expliquer pourquoi ce chiffre ?

        elif ListeUnicode[index] < 0 :

            ListeUnicode[index] = ListeUnicode[index] + 1114111

        ListeUnicode[index] = chr(ListeUnicode[index])
        # chr(x) est la fonction qui pour toute valeur Unicode x nous renvoie son charactère Unicode (sous type str)
        # Cette fonction transforme donc la suite de charactère chiffrés sous forme Unicode en message
        #TODO Bien commenté, GG :)


    return "".join(ListeUnicode)



def ChiffrementVignère(MotDePasse, chaine) :

    """Fonction qui chiffre une chaine avec un mot de passe comme clef de chiffrement,
    selon la méthode de Vignère"""

    chaine = transformationChiffres(chaine)
    #On transforme la chaine en chiffres

    MotDePasse = GénérationMotDePasseSécurisé(MotDePasse)
    MotDePasse = transformationChiffres(MotDePasse)
    #On hash le mot de passe, afin d'obtenir un nombre plus élévé de caractères

    nombreItérationsVigenère = (len(chaine) // len(MotDePasse))+ 1
    #TODO Expliquer cette ligne

    longueurItérationVigenère = len(MotDePasse)
    #TODO Explique cette ligne

    for x in range(0, nombreItérationsVigenère) :
    #TODO Expliquer ce qu'est X

        for y in range(0, longueurItérationVigenère) :
        #TODO Expliquer ce qu'est y

            try :
                chaine[x*longueurItérationVigenère+y] = chaine[x*longueurItérationVigenère+y] + MotDePasse[y]
            except :

            #TODO MonsieurGermant n'aime pas du tout les except sans execeptions
            # Exemple except ValueError: OK - except: NON

                a=1 #TODO ????

    

    return transformationCaratères(chaine)
    #On retourne le message chiffré, sous forme de caratères



def DéchiffrementVignère(MotDePasse, chaine):

    """ Fonction qui déchiffre une chaine avec un de mot de passe, 
    selon la méthode de Vignère """


    chaine = transformationChiffres(chaine)
    #On transforme la chaine à chiffrer en liste d'entiers

    MotDePasse = GénérationMotDePasseSécurisé(MotDePasse)
    MotDePasse = transformationChiffres(MotDePasse)
    #On hashe le mot le mot de passe, et on le transforme en liste d'entiers

    nombreItérationsVigenère = len(chaine) // len(MotDePasse) + 1
    #TODO Expliquer

    longueurItérationVigenère = len(MotDePasse)
    #TODO Expliquer

    for x in range(0, nombreItérationsVigenère) :
    #TODO Expliquer x et utiliter nom plus équivoque

        for y in range(0, longueurItérationVigenère):
        #TODO Expliquer y et utiliter nom plus équivoque

            try:
                chaine[x*longueurItérationVigenère+y] = chaine[x*longueurItérationVigenère+y] - MotDePasse[y]
            except:
            #TODO MonsieurGermant n'aime pas du tout les except sans execeptions
            # Exemple except ValueError: OK - except: NON
                a=1 #TODO ?????

     

    return transformationCaratères(chaine)
    #On renvoie la chaine sous formes de caractères




def GénérationMotDePasseSécurisé(MotDePasse):

    motDePasseUser = hashlib.sha224(bytes(MotDePasse, "utf-8")).hexdigest()
    motDePasseConstant = hashlib.sha224(b"q55|R,~gS2.m)RD5d^5N8KcS6?v7Lhb<").hexdigest()
    #On hashe le mot de passe de l'utilisateur + un mot de passe constant pour obtenir un mot bien plus sécurisé

    motDePasseFinal = motDePasseUser + motDePasseConstant
     
    résultat = []

    for caractère in motDePasseFinal:
    #Pour chaque caratère du hash

        try:
        #On essaie de convertir en entier pour vérifier si le caractère est un chiffre
            caractère = int(caractère)

        except ValueError:
        #En cas d'erreur de valeur, c'est une lettre, on ne fait rien
            pass

        else:
        #On transforme en lettre le chiffre en ajoutant 100 pour éviter d'avoir les tabulations de la table ascii
            caractère = chr(caractère + 100)

        finally:
        #On finit par ajout le caractère, converti ou non au résultat
            résultat.append(caractère)

    return "".join(résultat)



def InitialisationSauvegarde(motDePasse):

    """ Qui créé un fichier de sauvegarde au bon emplacement """

    try :
    #On essie de créé un dossier pour stocker les fichiers de sauvegardes
        makedirs("Messages sauvegardés")
    except FileExistsError :
    #Si le fichier existe déja
        pass

    NomFichier = "Messages sauvegardés/" + time.strftime("%A-%d-%B-%H.%M.%S")+".mcr"
    #On défini le nom du fichier avec le jour, la date, le mois et l'heure de début de la conversation

    DateDébutConversation = time.strftime("%A %d %B")
    HeureDébutConversation = time.strftime("%H:%M:%S")
    #On récupere l'heure et la début de la conversation 

    Annonce = ChiffrementVignère(motDePasse, str(f"Début de la conversation le {DateDébutConversation} à {HeureDébutConversation}."))
    #On chiffre l'annonce du début du fichier

    fichier = open(NomFichier, "wb")
    #On crée le fichier en mot écriture binaire

    fichier.write(bytes(Annonce, "utf-8"))
    fichier.write(bytes("\n", "utf-8"))
    fichier.close()
    #On écrit l'annonce de façon chiffrée puis on saute une ligne
    #On convertir en bytes pour faciliter la lecture

    

    return NomFichier



def NouvelleLigne(NomFichier, MotDePasse, chaine):

    """ Fichier qui ajoute une ligne chiffrée au fichier demandé """

    ChaineChiffré = ChiffrementVignère(MotDePasse, chaine)

    fichier = open(NomFichier, "ab")
    #On ouvre le fichier ne mode ajout à la ligne binaire

    fichier.write(bytes(ChaineChiffré, "utf-8"))
    fichier.write(bytes("\n", "utf-8"))
    fichier.close()
    #On ouvre le fichier de de sauvegarde, on écrit le message chiffré 
    #Puis on retourne à ligne
    #On convertir en bytes pour faciliter la lecture




def lectureSauvegarde(NomFichier, MDP):


    """ Fonction qui lit, déchiffre et retourne sous forme de liste 
    chaque ligne du fichier demandé """

    ListeLignes = []

    with codecs.open(NomFichier, "rb") as fichier :
    #On ouvrer le fichier en mode lecture binaire avec le module codec

        for ligne in fichier :
        #On lit une à une les lignes du fichier
            ListeLignes.append(ligne.decode("utf-8"))

    fichier.close()

    for index in range(len(ListeLignes)):
    #Pour chaque ligne

        ListeLignes[index] = DéchiffrementVignère(MDP, ListeLignes[index])
        #On déchiffre la ligne

        ListeLignes[index] = list(ListeLignes[index])
        ListeLignes[index].pop(-1)
        #On transforme la ligne en liste et on retire le derniere caratères "\U0010ffa2"

        ListeLignes[index] = "".join(ListeLignes[index])
        #On retransforme la ligne en texte

    return ListeLignes


#TODO Regarde la démo


if __name__ == "__main__":
#Si on execute le fichier en lui même, ces lignes ne seront pas lues en cas d'import

    """ Démonstration du module de sauvegarde chiffré """

    mdp = input("Veuillez saisir un mot de passe pour chiffrer votre sauvegarde\n>>> ")

    confirmationMDP = input("\nVeuillez saisir une seconde fois votre mot de passe\n>>> ")

    while confirmationMDP != mdp:

        confirmationMDP = input("\n Le mot de passe n'est confirmé. Veuillez saisir la confirmation du mot de passe\n>>> ")

    FichierSauvegarde = InitialisationSauvegarde(mdp)
    #On initialisae le fichier de sauvegarde au début de la conversations

    print(f"Un fichier de sauvegarde \"{FichierSauvegarde} à bien été crée")

    NouvelleLigne(FichierSauvegarde, mdp, "Bonjour, je suis la nouvelle ligne")
    #A chaque nouveau message, on ajoute une ligne

    NouvelleLigne(FichierSauvegarde, mdp, "Salut ligne 2, moi c'est ligne 3 !")

    print()
    print(f"Voici les lignes contenus dans {FichierSauvegarde}")
    print(lectureSauvegarde(FichierSauvegarde, mdp))
    #Fonction qui retourne chaque lignes déchiffrés du fichier
