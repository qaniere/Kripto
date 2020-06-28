import os
import json
import html

def RécupererIdentifiants():


    """ Renvoi les identfiants de Kripiti 
    Si le mode est sur Développement, les idenfiants sont lus depuis le fichier identifiants.txt)
    Si le mode est production, il doivent être contenu dans les variables """

    Mode = "Développement"

    if Mode == "Production":

        NomUtilisateur = "METTRE_USERNAMEICI"
        MotDePasseKripti = "MDPLA"
        #Une fois transformé en exe, impossible de relire le code source

    else:

        fichier = open("Identifiants.txt", "r")
        contenu = fichier.read()
        contenu = contenu.split("\n")

        NomUtilisateur = contenu[0]
        MotDePasseKripti = contenu[1]

    return NomUtilisateur, MotDePasseKripti

    
def CréerUneIssue(Titre, Message, Plateforme):

    import requests

    #On importe le module requets car il pose problème au niveau de l'installation chez certain utilisateur
    #Donc il n'est importé que si un bug est signalé

    NomUtilisateur, MotDePasseKripti = RécupererIdentifiants()

    PropriétaireDuRépertoire = "qaniere"
    NomDuRépetoire = "Kripto"

    url = f"https://api.github.com/repos/{PropriétaireDuRépertoire}/{NomDuRépetoire}/issues"

    session = requests.Session()
    session.auth = (NomUtilisateur, MotDePasseKripti)

    Issue = {"title": Titre,
             "body": Message + "\r\n" + Plateforme ,
             "labels": [""]}

    Requête = session.post(url, json.dumps(Issue))

    if Requête.status_code == 201:
        return True

    else:

        print (f"Erreur => {Requête.content}")
        return False

def ChuckNorrisFacts():

    import requests

    réponse = requests.get("https://www.chucknorrisfacts.fr/api/get?data=tri:alea;nb:1;")
    #Récupération d'une fact aléatoire encodé avec les caractères HTML

    RéponseDécodé = html_decoded_string =  html.unescape(réponse.json()[0]["fact"])
    #On décode les caractères HTML => &quot devient ' par exemple    
    
    return RéponseDécodé.replace("\r\n", " ") #On supprime les éventuels sauts de lignes