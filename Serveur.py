import sys
import time
import socket
import tkinter
from tkinter import *
from tkinter import messagebox

fen = Tk()
fen.withdraw()

#Constantes d'application
IP = sys.argv[1]
Port = int(sys.argv[2])
NbrMessageVides = 0

def envoi(message):
	global listeClient
	for destinataire in listeClient:
	#On désigne les destinaires du message, à savoir tout les clients connectés
	
		if destinataire != client:
		#Si le destinaire n'est pas l'expéditeur
			destinataire.send(bytes(message, "utf-8"))

#On défini les paramêtres du socket 
Serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	Serveur.bind((IP, Port))
except OSError:
	tkinter.messagebox.showerror(title="Aïe...", message="IL semblerait que votre IP ne soit pas valide. Réferez vous à l'aide pour régler ce problème.")
else:
	#On configure le serveur en mode non-bloquant : Au lieu d'attendre une réponse et de bloquer le programme, l'instruction retourne
	#une exeception si jamais aucune données n'est envoyée, ce qui empecherait la gestion de plusieurs clients
	Serveur.setblocking(0)

	#Démarrage du serveur
	Serveur.listen()
	print("Serveur démarré à", time.strftime("%H:%M:%S"), "sur le port", Port)

	#On initialise la liste qui contient les coordonnées des clients connectés
	listeClient = []

	while True:
	#Si il y'a une nouvelle connnexion, on traite la connexion
		try:
			infosClients, IPClient = Serveur.accept()
			listeClient.append(infosClients) #On stocke les infos du client dans la liste dédiées
			print(f"[{time.strftime('%H:%M:%S')}] Nouveau client connecté ! IP => {IPClient}")
		except IOError:
		#Si personne n'essaie de se connecter, on ralenti le programme pour préserver les ressources de la machine
			time.sleep(0.1)
	
		for client in listeClient:
		#On récupere chaque clients dans la variable
		
			#Si un message est envoyé, on le récupere, sinon l'instruction génére une exception
			try:
				message = client.recv(2048)
				message = message.decode("utf-8")

				if message == "":
					NbrMessageVides += 1

				else:
					MessageListe = message.split("|")
					Type = MessageListe[0]
					if Type == "Message":
							LongueurMessage =  MessageListe[1]
							HeureMessage = MessageListe[2]
							Expediteur = MessageListe[3]
							Contenu = MessageListe[4]
							messageFormaté = f"[{HeureMessage}] {Expediteur} : {Contenu}"
							print(messageFormaté)
							envoi(messageFormaté)

					else:
						print(f"Message recu invalide ! => {message} ")

			except:
				#Si aucun message n'a été envoyé
				time.sleep(0.1)