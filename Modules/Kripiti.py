import os
import json

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