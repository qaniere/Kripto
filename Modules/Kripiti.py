import os
import json
import requests

def CréerUneIssue(Titre, Message, Plateforme):

    print(f"Titre de l'issue => {Titre}")
    print(f"Détail du bug => {Message}")
    print(f"Plateforme => {Plateforme}")

    NomUtilisteur = "Kripiti"
    MotDePasseKripti = "Pass_Word_0"

    PropriétaireDuRépertoire = "qaniere"
    NomDuRépetoire = "Kripto"

    url = f"https://api.github.com/repos/{PropriétaireDuRépertoire}/{NomDuRépetoire}/issues"
    print(url)

    session = requests.Session()
    session.auth = (NomUtilisteur, MotDePasseKripti)

    Issue = {"title": Titre,
             "body": Message + "\r\n" + Plateforme ,
             "labels": [""]}

    Requête = session.post(url, json.dumps(Issue))

    if Requête.status_code == 201:
        print ("Issue créée avec succès !")
        return True

    else:

        print (f"Erreur => {Requête.content}")
        return False