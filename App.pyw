# coding: utf8
import time
import socket
import tkinter
import winsound
import subprocess	
from tkinter import *
from ChiffrementRSA import *
from random import randint, choices
import tkinter.font as tkFont
from tkinter import messagebox

#Variables d'applications
global listeNoms, Module,CléPublique, CléPrivée, NombreErreurs

listeNoms = ["Autruche", "JeanBon", "AmiralBenson", "TomNook", "Karamazov", "OdileDeray", "PatéEnCroute", "Risitas", "Nagui", "Shrek", "Clown"]
#La liste des noms qui seront suggérés à l'utilisateur.

Module, CléPublique, CléPrivée = génération(16)
#On génére une clé publique et une clé publique et on garde en mémoire le module de chiffrement

NombreErreurs = 0
#On initialise le compte d'erreurs

def formaterPaquet(TypePaquet, NomUser, Contenu):
    	
	"""
	Fonction qui permer de formater les messages selon des régles spécifiques pour optimiser le traitement coté 
	serveur.

		- Message : TypeDePaquet|Longueur|HeureEnvoi|AuteurDuMessage|ContenuDuMessage

	"""

	if TypePaquet == "Message":
    
		Paquet = f"Message|&|{time.strftime('%H:%M:%S')}|{NomUser}|{Contenu}"
		#La longueur du paquet est indéterminé à ce stade, alors on met un caractére facilement remplaçable à la place.

		longueurPaquet = len(Paquet) - 1 
		#Le -1 est le "&" qu'on enlevera
		longueurPaquet += len(str(longueurPaquet))
		#On ajoute à la longueur du paquet la longueur du paquet
		#Exemple : Le paquet fait 10 caractére, on ajouter deux caractéres pour le signifier donc la longueur sera de 12.

		Paquet = Paquet.replace("&", str(longueurPaquet))

	return Paquet



def envoyer():

	"""Fonction qui chiffre et envoi les message au serveur. Les messages sont chiffrés en fonction du serveur"""

	global saisieMessage, nomUser, filMessages, ConnexionSocket, NombreErreurs, CléPubliqueServeur, ModuleServeur
	#On récuper toutes les variables et objets nécésssaires au fonctionnement de la fonction

	message = saisieMessage.get()
	#On récupere le message dans l'entrée où il a été saisi

	if len(message) != 0:
    		
		messageInterface = f"[{time.strftime('%H:%M:%S')}] {nomUser} : {message}"
		#On garde de coté un message avec un formaté spécialement pour l'interface, mais on ne l'utilise que si l'envoi est réussi.

		message = formaterPaquet("Message", nomUser, message)
		#On formate le paquet

		message = transformationChiffres(message)
		message = cryptage(message, CléPubliqueServeur, ModuleServeur)
		#On transforme le message en liste de chiffres, correspondant à leur identifiant Ascii, puis on chiffre le message

		#On récupere alors un liste d'entiers

		ChaineMessage = ""

		for index in message:
    	#On récupere tour à tour chaque index de la liste message
			ChaineMessage += str(index) + "/"
			#On ajoute à la variable vide chaque index qu'on converti en texte et on insére un / pour pouvoir les redécouper
    		
		message = ChaineMessage.encode('utf-8')
		#On encode le tout en UTF8

		try:
			ConnexionSocket.send(bytes(message))
			#On essaie d'envoyer le message au serveur.

		except ConnectionResetError:
		#Si le serveur ne répond pas
	
			if NombreErreurs < 3:
				tkinter.messagebox.showerror(title="Aïe...", message="Impossible de joindre le serveur. Veuillez réessayer.")
				NombreErreurs += 1
			else:
    		#Si il y'a plus de trois erreurs, on stoppe le programme, en invitant l'utilisateur à se reconnecter

				messsageErreur = "Le serveur est injoignable pour le moment. Veuillez vous reconnecter ou bien référez vous à l'aide"
				#On stocke le message dans un variable pour diminuer la taille de la ligne d'en dessous
				tkinter.messagebox.showerror(title="Aïe...", message=messsageErreur)
				exit()

		else:
    	#Si il n'a pas eu d'execeptions
			filMessages.insert(END, messageInterface)
			filMessages.yview(END)
			#On insère le message dans listbox et on défile tout en bas cette dernière, vers le message le plus récent
			winsound.PlaySound("Médias/SonEnvoi.wav", winsound.SND_ASYNC)
			saisieMessage.delete(0, 'end')
			#On vide la zone de saisie du message




def reception():
    	
	""" Fonction récursive (Qui s'appelle elle même toutes les 10ms) qui permet de vérifier
	la présence de nouveaux messages"""

	global filMessages, ConnexionSocket, CléPrivée, Module
	#On récupere les variables nécéssaires au fonctionemment de la fonction

	try:
	#Cette partie du code est dans un bloc "try, except" car "ConnexionSocket.setblocking(0)" a été défini sur False
	#Au lieu d'attendre un message, si rien n'est envoyé cela va générer une exception, ce qui permet un fonctionnement asynchrone.

		messageRecu = ConnexionSocket.recv(2048)
		#2048 est la limite d'octets recevables
		messageRecu = messageRecu.decode("utf-8")

		messageRecu = messageRecu.split("/")
		#On transforme le message recu en liste
		#Exemple => "234/23124/34142" donnera la liste ["234", "23124", "34142"]

		messageRecu.remove("")
		#On supprime le dernier index vide de la liste
		
		for index in range (len(messageRecu)):
    	#Boucle qui sera executé autant de fois qu'il y'a d'index dans la liste messageRecu

			messageRecu[index] = int(messageRecu[index])
			#On transforme l'index de la liste en entier pour pouvoir le déchiffrer

		messageRecu = décryptage(messageRecu, CléPrivée, Module)
		messageRecu = transformationCaratères(messageRecu)
		#On décrypte le message recu, puis ensuite,  on le transforme en caractères

		filMessages.insert(END, messageRecu)
		filMessages.yview(END)
		#On insére le message dans la listbox des messages, puis on force le défilement tout en bas de cette dernière

		winsound.PlaySound("Médias/SonMessage.wav", winsound.SND_ASYNC)
	except BlockingIOError:
	#Si aucun message n'a été envoyé, on ne fait rien
		pass
	finally:	
	#Bloc qui sera executé aprés le try ou l'except
		fen.after(10, reception)
		#La fonction s'appelle après 10ms




def placeholder(Provenance):
    
	""" Fonction qui reproduit l'atribut "placeholder" des input HTML. Un suggestions est affiché, quand l'utilisateur clique
	dessus elle disparait"""

	if Provenance == "AppelManuel":
    #Si la fonction a été appellé par une instruction 
		saisieMessage.insert(0, "Saisissez votre message ici")
	else:
    #La fonction a été appellé par un bind, on supprime alors le placeholder
		saisieMessage.delete(0, "end")



def toucheEntre(argumentUseless):
    
	""" Cette fonction sert simplement à contourner un défaut de conception de Tkinter : Les fonctions appellées avec bind le sont
	toujours avec argument qui contient la position de la souris, ce qui pose problème quand la fonction cible ne prend aucun 
	argument"""

	envoyer()



def affichageConversation():
    	
	""" Cette fonction sert à générer l'interface de la conversation"""

	global cadreParametres, saisieMessage, nomUser, filMessages
	#On récuperer les objets et les variables nécéssaire au fonctionnement de la fonction

	logo.pack_forget()
	cadreParametres.pack_forget()
	#On efface les élements de connexion / paramétrage du serveur

	filMessages = Listbox(fen, width="70", height="20")
	filMessages.pack(pady=15)

	saisieMessage = Entry(fen, width="60")
	saisieMessage.pack()

	bouttonEnvoyer = Button(fen, text="Envoyer", command=envoyer)
	bouttonEnvoyer.pack(pady=15)

	saisieMessage.bind("<Button-1>", placeholder)
	#On associe le clic gauche sur la zone de saisie du message à la fonction placeholder
	fen.bind_all('<Return>', toucheEntre)
	#On associe l'appui sur la toucheEntre à la fonction toucheEntre

	reception()
	#On commence à recevoir des messages
	placeholder("AppelManuel")



def connexion():
    	
	""" Cette fonction sert à se connecter au serveur et à envoyer le nom d'utilisateur, la clé publique, le module de chiffrement au serveur,
	et on recoit les informations de chiffrement du serveur, la clé publique et le module de chiffrement"""

	global IP, Port, nomUser, entreNom, ConnexionSocket, entreIP, Role, CléPublique, CléPubliqueServeur, ModuleServeur
	#On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

	IP = entreIP.get()
	nomUser = entreNom.get()

	ConnexionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#On défini notre connexion socket
	# - AF_INET => Protocole IPV4
	# - SOCK_STREAM => Stream veut dire cours d'eau, comme un flot continu de donnés qui est envoyé

	ConnexionSocket.settimeout(5)
	#Si au bout de 5secondes, il n'y pas de réponse (Délai plus que nécéssaire pour des simples paquets TCP) une exception est générée

	try:
		ConnexionSocket.connect((IP, Port))
		#Le code après cette instruction est executé uniquement si la connection réussit

		données = f"{nomUser}|{CléPublique}|{Module}"
		données = données.encode('utf-8')

		ConnexionSocket.send(bytes(données))

		#On formate, puis on envoi les données de chiffrement au serveur

		AutorisationEtDonnées = ConnexionSocket.recv(2048)
		AutorisationEtDonnées = AutorisationEtDonnées.decode("utf-8")

		#On recoit de la part du serveur l'autorisation de se connecter, et les données de chiffrement du serveur

		if AutorisationEtDonnées != "False":
    	#Si le serveur autorise la connexion

			AutorisationEtDonnées = AutorisationEtDonnées.split("|")
			#On récupere les données sous forme de le liste

			CléPubliqueServeur = int(AutorisationEtDonnées[0])
			ModuleServeur = int(AutorisationEtDonnées[1])

			#On converti les données en entiers, puis on les affectes au variables adaptées

			ConnexionSocket.setblocking(0)
			#On définit le mode de connexion sur non bloquant (Voir explications dans la fonction reception)

			
			return True
			#On retoune que la connexion a été validé 
		else:
		#Si le serveur ne donne pas son autorisation

			messageErreur = "Un utilisateur avec le même nom d'utilisateur que le votre est déja connecté. Changez de nom d'utilisateur pour accéder à ce serveur."
			#On raccourci la ligne du dessous avec cette variable
			tkinter.messagebox.showerror(title="Aïe...", message=MessageErreur)	

	except (ConnectionRefusedError, socket.timeout):
	#Si on arrive pas à se connecter au serveur

		if Role == "Hote":
		#Si c'est l'hôte, il a déja recu l'erreur de la part du serveur donc affiche rien

			return False
			#On indique que la connexion est un échec
		else:
			messageErreur = "IL semblerait que les coordonées du serveur ne soit pas valides. Réferez vous à l'aide pour régler ce problème."
			#On raccourci la ligne du dessous avec cette variable
			tkinter.messagebox.showerror(title="Aïe...", message=messageErreur)
			return False



def démarrerServeur():
    	
	""" Cette fonction sert à démarrez le serveur quand on est hôte"""

	global entreIP, entrePort, IP, Port, Role
	#On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

	Role = "Hote"
	IP = entreIP.get()
	Port = int(entrePort.get())

	subprocess.Popen(f"python Serveur.py {IP} {Port}")
	#On lance le serveur dans un processus parallèle.

	if connexion() == True:
    #Si la connexion est une réussite, on affiche les conversations
		affichageConversation()



def seConnecter():
    	
	""" Fonction qui affiche l'interface de discusion si la connexion est une réussite"""

	global entreIP, entrePort, IP, Port, Role
	#On récupereles objets et les variables nécéssaire au fonctionnement de la fonction
	
	Role = "Client"
	Port = int(entrePort.get())
	IP = entreIP.get()

	if connexion() == True: 
		affichageConversation()




def hote():
    	
	""" Fonction qui affiche l'interface de création de serveur """

	global entrePort, IP, nomUser, cadreParametres, entreNom, entreIP, listeNoms
	#On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()
	#On efface le menu

	hote = socket.gethostname()
	IP = socket.gethostbyname(hote)
	#On récupere l'addresse IP de la machine

	cadreParametres = Frame(fen, bg="grey")
	cadreParametres.pack()       

	votreIP = Label(cadreParametres, text="Votre Adresse IP", bg="Grey")
	votreIP.pack(anchor=CENTER, pady=7)

	entreIP = Entry(cadreParametres)
	entreIP.insert("end", IP)
	entreIP.pack(anchor=CENTER)

	votrePort = Label(cadreParametres, text="Port", bg="Grey")
	votrePort.pack(anchor=CENTER, pady=7)

	portRecommande = randint(49152, 65535)
	#On recommande un port dans la plage de ceux les moins utilisés

	entrePort = Entry(cadreParametres)
	entrePort.insert("end", portRecommande)
	entrePort.pack(anchor=CENTER)

	suggestionNom = choices(listeNoms)
	#On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms

	votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
	votreNom.pack(anchor=CENTER, pady=7)

	entreNom = Entry(cadreParametres)
	entreNom.insert("end", suggestionNom)
	entreNom.pack(anchor=CENTER)

	bouttonStart = Button(cadreParametres, text="Démarrer", command=démarrerServeur)
	bouttonStart.pack(pady=20)



def client():
    	
	""" Cette fonction permet à un client de se connecter au serveur""" 

	global entreIP, entrePort, entreNom, cadreParametres, listeNoms
	#On récupereles objets et les variables nécéssaire au fonctionnement de la fonction

	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()
	#On efface le menu

	cadreParametres = Frame(fen, bg="grey")
	cadreParametres.pack()       

	IpduServeur = Label(cadreParametres, text="Adresse IP du serveur", bg="Grey")
	IpduServeur.pack(anchor=CENTER, pady=7)

	entreIP = Entry(cadreParametres)
	entreIP.insert("end", "192.168.1.")
	entreIP.pack(anchor=CENTER)

	PortduServeur = Label(cadreParametres, text="Port du serveur", bg="Grey")
	PortduServeur.pack(anchor=CENTER, pady=7)

	entrePort = Entry(cadreParametres)
	entrePort.pack(anchor=CENTER)

	suggestionNom = choices(listeNoms)
	#On suggére à l'utilisateur un nom d'utilisateur parmis la liste des noms

	votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
	votreNom.pack(anchor=CENTER, pady=7)

	entreNom = Entry(cadreParametres)
	entreNom.insert("end", suggestionNom)
	entreNom.pack(anchor=CENTER)

	bouttonStart = Button(cadreParametres, text="Se connecter",  command=seConnecter)
	bouttonStart.pack(pady=20)



fen = Tk()
fen.geometry("550x450")
fen.title("Kripto - Un chat chiffré")
fen.configure(bg="grey")
fen.resizable(width=False, height=False)
fen.iconbitmap(bitmap="Médias/icone.ico")

policeBienvenue = tkFont.Font(family="Verdanna",size=16,weight="bold")
policeBoutton = tkFont.Font(family="Arial",size=12,weight="bold")
policeIP = tkFont.Font(size=14,weight="bold")

imageLogo = PhotoImage(file="Médias/Logo.png")
 
logo = Label(fen, bg="grey", image=imageLogo)
logo.pack() 

messageBienvenue = Label(fen, text="Bienvenue dans Kripto. Pour démarrez, dites-nous \nsi vous voulez être hôte ou bien client.", bg="grey", font=policeBienvenue)
messageBienvenue.pack()

cadreBouttons = Frame(fen, bg="grey")
cadreBouttons.pack(pady=60)

bouttonHote = Button(cadreBouttons, text="Être hôte", font=policeBoutton, command=hote)
bouttonHote.pack(side=LEFT, padx=7)

bouttonClient = Button(cadreBouttons, text="Être client", font=policeBoutton, command=client)
bouttonClient.pack(side=LEFT, padx=7)

fen.mainloop()