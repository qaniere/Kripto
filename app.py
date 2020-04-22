import os
import time
import socket
import platform

#Fonction qui efface l'écran, elle est compatible avec Windows et Linux
def cls():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
#La commande varie selon les os

#On affiche un message de bienvenue
print(" ____  _                                        _ ")
print("|  _ \(_)                                      | |")
print("| |_) |_  ___ _ ____   _____ _ __  _   _  ___  | |")
print("|  _ <| |/ _ \ '_ \ \ / / _ \ '_ \| | | |/ _ \ | |")
print("| |_) | |  __/ | | \ V /  __/ | | | |_| |  __/ |_|")
print("| |_) | |  __/ | | \ V /  __/ | | | |_| |  __/ |_|")
print("|____/|_|\___|_| |_|\_/ \___|_| |_|\__,_|\___| (_)")

time.sleep(1.5)
cls()
#On attend une demie seconde puis on efface l'écran
