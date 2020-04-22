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

