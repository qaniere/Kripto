import sys
import time
import os.path
import subprocess

commande = " ".join(sys.argv[1:])
#On récupere la commande à effectuer

ListeFichier = []
DateModificationInitiale = {}

for fichier in os.listdir("."):
#Pour chaque fichiers, dossiers et sous-fichiers/dossiers

    ListeFichier.append(fichier)
    #On les ajoutes à la liste (Permettra d'en exclure certain à l'avenir)
    DateModificationInitiale[fichier] = time.ctime(os.path.getmtime(fichier))
    #On récuperé la data de la dernière modification

processus = subprocess.Popen(commande)
#On lance la commande demandée

while True:

    for fichier in ListeFichier:
    #Pour chaque fichier qu'on souhaite observer

        DernièreModif = time.ctime(os.path.getmtime(fichier))
        #On récupere la date de dernière modification

        if DateModificationInitiale[fichier] != DernièreModif:
        #Si il y'a eu une modification

            print(f"'{fichier}' a été modifié. Rédémarrage en cours.")
            #Log dans la console

            processus.kill()
            processus = subprocess.Popen(commande)
            #On ferme l'ancien proccesus et on relance le nouveau

            DateModificationInitiale[fichier] = DernièreModif
            #On met à jour la date de modification initiale
            
