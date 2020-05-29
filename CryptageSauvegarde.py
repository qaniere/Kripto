# coding: utf8
from hashlib import sha1
from os import makedirs
import codecs


"""Dans ce programme on décrira les fonctions permetant la création d'une sauvegarde cryptée des messages"""


''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Message au lecteur ''''''''''''''''''''''''''''''''''''''''''''''''''''''

Ce programme contient différentes fonctions, décrites ci-dessous :

    - Une fonction de chiffrement, nécessaire aux fonctions de cryptage et de décryptage (fonctionnelle)
    - Une fonction de déchiffrement, nécessaire aux fonctions de cryptage et de décryptage (fonctionnelle)
    - Une fonction de cryptage pour préparer sauvegarde (fonctionnelle)
    - Une fonction de décryptage de sauvegarde (fonctionnelle)
    - Une fonction de cryptage de mot de passe, qui aide les fonctions de cryptage et de décryptage de sauvegarde (fonctionnelle)
    - Une fonction de sauvegarde (fonctionnelle)
    - Une fonction de chargement de sauvegarde (fonctionnelle)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


### Définition de la fonction de chiffrement ###


def transformationChiffres(messageClair):

    """Fonction de chiffrement : transforme le message clair en message chiffré"""

    messageChiffré = list(messageClair)
    for i in range(len(messageChiffré)):
        messageChiffré[i] = ord(messageChiffré[i])
        # ord(x) est la fonction qui pour tout charactère Unicode (sous type str) x renvoie sa valeur Unicode
        # Cette fonction transforme donc le message en une suite de charactère chiffrés sous forme Unicode
    return messageChiffré


### Définition de la fonction de déchiffrement ###


def transformationCaratères(messageChiffré):

    """Fonction de déchiffrement : transforme le message chiffré en message clair"""

    messageClair = messageChiffré
    for j in range(len(messageClair)):

        ## Boucle de sécurité si jamais le cryptage donnerait à convertir des nombres ne rentrant pas dans la table de caractères Unicode ##
        
        if messageClair[j] > 1114111 :
            messageClair[j] = messageClair[j] - 1114111
        elif messageClair[j] < 0 :
            messageClair[j] = messageClair[j] + 1114111

        messageClair[j] = chr(messageClair[j])
        # chr(x) est la fonction qui pour toute valeur Unicode x nous renvoie son charactère Unicode (sous type str)
        # Cette fonction transforme donc la suite de charactère chiffrés sous forme Unicode en message
    messageClair = "".join(messageClair)
    return messageClair


### Définition de la fonction de cryptage ###


def cryptageSauvegarde(messageASauvegarder) :

    """Fonction de cryptage pour la sauvegarde : transforme les messages clairs à enregistrer en messages cryptés, à l'aide d'un mot de passe"""

    bonMotDePasseVérifié = 0

    while bonMotDePasseVérifié != 1 :

        motDePasse = input("\nMot de passe ?\n>>> ")
        # A remettre sous forme Tkinter

        vérificationMotDePasse = input("\nVérification mot de passe\n>>> ")
        # A remettre sous forme Tkinter

        if motDePasse == vérificationMotDePasse :

            bonMotDePasseVérifié = 1

        else :
            print("\nVeuillez rentrez deux fois le même mot de passe")


    messageASauvegarderChiffré = transformationChiffres(messageASauvegarder)

    motDePasseChiffré = transformationChiffres(transformationMotDePasse(motDePasse))
    print("\n  Mot de passe hashé maison : "+str(transformationMotDePasse(motDePasse)))

    nombreItérationsVigenère = (len(messageASauvegarderChiffré) // len(motDePasseChiffré))+ 1

    longueurItérationVigenère = len(motDePasseChiffré)

    for x in range(0, nombreItérationsVigenère) :
        for y in range(0, longueurItérationVigenère) :
            try :
                messageASauvegarderChiffré[x*longueurItérationVigenère+y] = messageASauvegarderChiffré[x*longueurItérationVigenère+y] + motDePasseChiffré[y]
            except :
                a=1

    messageASauvegarderCrypté = transformationCaratères(messageASauvegarderChiffré)

    print("\n    Message crypté à la Vigenère : "+str(messageASauvegarderCrypté)+"\n\n")

    return messageASauvegarderCrypté


### Définition de la fonction de décryptage ###


def décryptageSauvegarde(messageSauvegardéCrypté):

    """Fonction de décryptage pour la sauvegarde : transforme les messages cryptés enregistrés en messages clairs, à l'aide d'un mot de passe"""

    bonMotDePasseVérifié = 0

    while bonMotDePasseVérifié != 1:

        motDePasse = input("\nMot de passe ?\n>>> ")
        # A remettre sous forme Tkinter

        vérificationMotDePasse = input("\nVérification mot de passe\n>>> ")
        # A remettre sous forme Tkinter

        if motDePasse == vérificationMotDePasse :
            bonMotDePasseVérifié = 1

        else :
            print("\nVeuillez rentrez deux fois le même mot de passe")

    print()

    messageSauvegardéCryptéChiffré = transformationChiffres(messageSauvegardéCrypté)

    motDePasseChiffré = transformationChiffres(transformationMotDePasse(motDePasse))
    print("\n  Mot de passe hashé maison : "+str(transformationMotDePasse(motDePasse)))

    nombreItérationsVigenère = len(messageSauvegardéCryptéChiffré) // len(motDePasseChiffré) + 1

    longueurItérationVigenère = len(motDePasseChiffré)

    for x in range(0, nombreItérationsVigenère) :
        for y in range(0, longueurItérationVigenère):
            try :
                messageSauvegardéCryptéChiffré[x*longueurItérationVigenère+y] = messageSauvegardéCryptéChiffré[x*longueurItérationVigenère+y] - motDePasseChiffré[y]
            except:
                a=1

    messageSauvegardé = transformationCaratères(messageSauvegardéCryptéChiffré)

    return messageSauvegardé


### Définition de la fonction de transformation de mot de passe ###


def transformationMotDePasse(motDePasse) :

    """Fonction de décryptage pour la sauvegarde : transforme les messages cryptés enregistrés en messages clairs, à l'aide d'un mot de passe"""

    motDePasseHashé = list(str(sha1(bytes(motDePasse, encoding='utf-8')).hexdigest()))

    motDePasseHashéMaison = []

    for i in range(0, 9) :

        motDePasseHashéMaison.append(str(str(motDePasseHashé[i*4])+str(motDePasseHashé[i*4+1])+str(motDePasseHashé[i*4+2])+str(motDePasseHashé[i*4+3])))
        motDePasseHashéMaison[i]= chr(int(motDePasseHashéMaison[i], 16))

    motDePasseHashéMaison = "".join(motDePasseHashéMaison)

    return motDePasseHashéMaison


### Définition de la fonction de sauvegarde ###


def sauvegarde(messageASauvegarderCrypté) :

    """Fonction de sauvegarde : Enregistrer les messages les cryptés"""

    nomDeLaSauvegarde = str(input("Quel nom voulez-vous donner à votre sauvegarde ?\n>>> "))

    try :
        makedirs("Messages sauvegardés")
    except FileExistsError :
        # directory already exists
        pass

    nomDuFichierDeLaSauvegarde = str("Messages sauvegardés/"+str(nomDeLaSauvegarde)+".mcr")

    fichier = open(nomDuFichierDeLaSauvegarde, "a", encoding = "utf-8")
    fichier.write(messageASauvegarderCrypté)
    fichier.close()


### Définition de la fonction de lecture de sauvegarde ###


def chargerSauvegarde() :

    """Fonction de chargement de sauvegarde : Charger les messages sauvegardés cryptés"""

    nomDeLaSauvegarde = str(input("\nQuelle sauvegarde voulez-vous charger ?\n>>> "))

    nomDuFichierDeLaSauvegarde = str("Messages sauvegardés/"+str(nomDeLaSauvegarde)+".mcr")

    sauvegardeEnCoursDeChargement = []

    try :
        with codecs.open(nomDuFichierDeLaSauvegarde, encoding="utf-8") as fichier :
            for line in fichier :
                sauvegardeEnCoursDeChargement.append(line)
        fichier.close()

        sauvegardeChargée = str("".join(sauvegardeEnCoursDeChargement))

        return sauvegardeChargée

    except :

        print("Erreur fatale : assurez vous que ce soit le bon nom de fichier (sans l'extension mcr), et qu'il soit dans le bon dossier.")


### Partie de sauvegarde ###


#sauvegarde(cryptageSauvegarde(input("Entrez le message à crypter\n>>> ")))

#print("\nVotre message a bien été enregistré !")


### Partie de chargement de sauvegarde ###


print("\nVotre message était : "+str(décryptageSauvegarde(chargerSauvegarde())))


# Pause pour pouvoir observer le code :
input("\n\nFIN\n\n")
