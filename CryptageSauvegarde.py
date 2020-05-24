# coding: utf8
from ChiffrementRSA import transformationChiffres, transformationCaratères
from hashlib import sha1


"""Dans ce programme on décrira les fonctions permetant la création d'une sauvegarde cryptée des messages"""


''''''''''''''''''''''''''''''' Message au lecteur ''''''''''''''''''''''''''''''
A écrire
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


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

    print("\n    Message crypté à la Vigenère : "+str(messageASauvegarderCrypté))

    return messageASauvegarderCrypté


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

def transformationMotDePasse(motDePasse) :

    a = list(str(sha1(bytes(motDePasse, encoding='utf-8')).hexdigest()))

    b = []

    for i in range(0, 9) :

        b.append(str(str(a[i*4])+str(a[i*4+1])+str(a[i*4+2])+str(a[i*4+3])))
        b[i]= chr(int(b[i], 16))
    
    b = "".join(b)

    return b


print("\nVotre message était : "+str(décryptageSauvegarde(cryptageSauvegarde(input("Entrez le message à crypter\n>>> ")))))
input("\n\nFIN\n\n")
