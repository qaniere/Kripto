import os
import json
import requests

def CréerUneIssue(Titre, Message, Plateforme):

    print(f"Titre de l'issue => {Titre}")
    print(f"Détail du bug => {Message}")
    print(f"Plateforme => {Plateforme}")

    NomUtilisteur = "Kripiti"
    MotDePasse = "Pass_Word_0"

    PropriétaireDuRépertoire = "qaniere"
    NomDuRépetoire = "Kripto"

    url = f"https://api.github.com/repos/{PropriétaireDuRépertoire}/{NomDuRépetoire}/issues"
    print(url)

    session = requests.Session()
    session.auth = (NomUtilisteur, MotDePasse)

    Issue = {"title": Titre,
             "body": Message + "\r\n" + Plateforme ,
             "labels": ""}

    Requête = session.post(url, json.dumps(Issue))

    if Requête.status_code == 201:
        print ("Issue créée avec succès !")
    else:
        print (f"Erreur => {Requête.content}")