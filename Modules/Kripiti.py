import os
import json
import html

def CréerUneIssue(Titre, Message, Plateforme):

    import requests

    #On importe le module requets car il pose problème au niveau de l'installation chez certain utilisateur
    #Donc il n'est importé que si un bug est signalé

    NomUtilisteur = "Kripiti"
    MotDePasseKripti = "Pass_Word_0"

    PropriétaireDuRépertoire = "qaniere"
    NomDuRépetoire = "Kripto"

    url = f"https://api.github.com/repos/{PropriétaireDuRépertoire}/{NomDuRépetoire}/issues"

    session = requests.Session()
    session.auth = (NomUtilisteur, MotDePasseKripti)

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
