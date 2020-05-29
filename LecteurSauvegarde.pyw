# coding: utf8
import os
from tkinter import *
from Sauvegarde import *
import tkinter.simpledialog


def LecteurSauvegarde():

    fen = Tk()
    fen.geometry("550x460")
    fen.configure(bg="grey")
    fen.resizable(width=False, height=False)
    fen.iconbitmap(bitmap="Médias/icone.ico")
    fen.title("Kripto - Lecture sécurisée des sauvegardes")
    #Configuration de la fenêtre

    def ouverture():

        try:
            Fichier = "Messages sauvegardés/" + Interface.get(Interface.curselection())
            #On récupere le fichier sélectioné
        except:
        #Si jamais aucun fichier n'est sélectioné, cela produit une exception
            return
            #On stoppe la fonction

        MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show='*')

        if MotDePasse == "":
        #Aucun mot de passe rentré, on anule tout

            return #Mot clé qui stoppe l'exécution de la fonction

        Terminer.configure(state=ACTIVE)
        Valider.configure(state=DISABLED)
        #On change l'état des bouttons

        Interface.delete(0,"end")
        #On supprime tout les fichiers dans l'interface

        Disscusion = lectureSauvegarde(Fichier, MotDePasse)
        #On lis la sauvegarde et on récupere sous forme de liste tout les messages

        for message in Disscusion:

            Interface.insert("end", message)

            
        
    def terminer():

        Terminer.configure(state=DISABLED)
        Valider.configure(state=ACTIVE)
        #On change l'état des bouttons

        Interface.delete(0,"end")
        #On supprime tout les fichiers dans l'interface

        for fichier in ListeSauvegardes:

            Interface.insert("end", fichier)
            #On insére dans l'interface chaque fichier de sauvegarde existant


    try:
        ListeSauvegardes = os.listdir("Messages Sauvegardés")
        #On liste chaque fichier du répertoire Messages Sauvegardés
    except OSError:
    #Si le dossier de sauvegarde n'existe pas

        fen.withdraw()
        tkinter.messagebox.showerror(title="Aïe...", message="Vous n'avez pas de sauvegardes")
        #On cache la fenêtre et on affiche un message d'erreur
        exit()

    Interface = Listbox(fen, width="70", height="20")
    Interface.pack(pady=15)

    for fichier in ListeSauvegardes:

        Interface.insert("end", fichier)
        #On insére dans l'interface chaque fichier de sauvegarde existant

    cadreBouttons = Frame(fen, bg="grey")
    cadreBouttons.pack(pady=40)

    Valider = Button(cadreBouttons, text="Ouvrir ce fichier", command=ouverture, width="20")
    Valider.pack(side=LEFT, padx=7)

    Terminer = Button(cadreBouttons, text="Terminer", command=terminer, state=DISABLED, width="20")
    Terminer.pack(side=LEFT, padx=7)

    fen.mainloop()

if __name__ == "__main__":
#Si le fichier est executé et non importé comme un module
    LecteurSauvegarde()