# coding: utf8
import os
from tkinter import *
import tkinter.simpledialog
from Modules import Sauvegarde

def LecteurSauvegarde():

    global ListeSauvegardes

    FenLecteurSauv = Tk()
    FenLecteurSauv.geometry("550x460")
    FenLecteurSauv.configure(bg="grey")
    FenLecteurSauv.resizable(width=False, height=False)
    FenLecteurSauv.iconbitmap(bitmap="Médias/icone.ico")
    FenLecteurSauv.title("Kripto - Lecture sécurisée des sauvegardes")
    # Configuration de la fenêtre

    def ouverture():

        try:
            Fichier = "Messages sauvegardés/" + Interface.get(Interface.curselection())
            # On récupere le fichier sélectioné
        except:
        # Si jamais aucun fichier n'est sélectioné, cela produit une exception
            return
            # On stoppe la fonction

        MotDePasse = tkinter.simpledialog.askstring("Mot de passe", "Veuillez saisir le mot de passe de la sauvegarde", show="•")

        if MotDePasse == "":
        # Aucun mot de passe rentré, on anule tout

            return # Mot clé qui stoppe l'exécution de la fonction

        Terminer.configure(state=ACTIVE)
        Valider.configure(state=DISABLED)
        Supprimer.configure(state=DISABLED)
        # On change l'état des bouttons

        Interface.delete(0,"end")
        # On supprime tout les fichiers dans l'interface

        Disscusion = Sauvegarde.LectureSauvegarde(Fichier, MotDePasse)
        # On lis la sauvegarde et on récupere sous forme de liste tout les messages

        if Disscusion.pop(0) == "Fichier déchiffré !":

            for message in Disscusion:

                Interface.insert("end", message)

        else: 
            tkinter.messagebox.showerror(title = "Mauvais mot de passe", message = "Le mot passe de cette sauvegarde n'est pas correct")
            terminer()

    def supprimer():

        global ListeSauvegardes

        try: Fichier = Interface.get(Interface.curselection())
        #Si rien n'est sélectioné, cela génére toujours une exeception
        except: pass

        else:

            RéponseUser  = tkinter.messagebox.askokcancel("Suppresion", f"Voulez vraiment supprimer la {Fichier} ? Cette action est irréversible !")

            if RéponseUser == True: 
                os.remove("Messages Sauvegardés/" + Fichier)
                ListeSauvegardes.remove(Fichier)
                terminer()

    def terminer():

        Terminer.configure(state=DISABLED)
        Supprimer.configure(state=ACTIVE)
        Valider.configure(state=ACTIVE)
        # On change l'état des bouttons

        Interface.delete(0,"end")
        # On supprime tout les fichiers dans l'interface

        for fichier in ListeSauvegardes:

            Interface.insert("end", fichier)
            # On insère dans l'interface chaque fichier de sauvegarde existant


    try: ListeSauvegardes = os.listdir("Messages Sauvegardés")
        # On liste chaque fichier du répertoire Messages Sauvegardés
    except OSError:
    # Si le dossier de sauvegarde n'existe pas

        FenLecteurSauv.withdraw()
        tkinter.messagebox.showwarning(title="Erreur de sauvegarde", message="Vous n'avez pas de sauvegardes")
        FenLecteurSauv.destroy()
        return False

    if len(ListeSauvegardes) == 0:

        FenLecteurSauv.withdraw()
        tkinter.messagebox.showwarning(title="Erreur de sauvegarde", message="Vous n'avez pas de sauvegardes")
        FenLecteurSauv.destroy()
        return False

    Interface = Listbox(FenLecteurSauv, width="70", height="20")
    Interface.pack(pady=15)

    for fichier in ListeSauvegardes:

        Interface.insert("end", fichier)
        # On insére dans l'interface chaque fichier de sauvegarde existant


    cadreBouttons = Frame(FenLecteurSauv, bg="grey")
    cadreBouttons.pack(pady=40)

    Valider = Button(cadreBouttons, text="Ouvrir ce fichier", command=ouverture, width="20")
    Valider.pack(side=LEFT, padx=7)

    Terminer = Button(cadreBouttons, text="Terminer", command=terminer, state=DISABLED, width="20")
    Terminer.pack(side=LEFT, padx=7)

    Supprimer = Button(cadreBouttons, text="Supprimer", command=supprimer, width="20")
    Supprimer.pack(side=LEFT, padx=7)

    FenLecteurSauv.mainloop()
