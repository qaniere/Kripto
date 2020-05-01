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

#OUI LE CODE EST DEGEU ET PAS COMMENTE PARCE QUE J'AI PAS LE TEMPS GNAGNAGNA

global listeNoms, Module,CléPublique, CléPrivée, NombreErreurs

listeNoms = ["Autruche", "JeanBon", "AmiralBenson", "TomNook", "Karamazov", "OdileDeray", "PatéEnCroute", "Risitas", "Nagui", "Shrek", "Clown"]
Module, CléPublique, CléPrivée = génération(16)
NombreErreurs = 0

def formaterPaquet(TypePaquet, NomUser, Contenu):

    if TypePaquet == "Message":
    #Message|Longeur|Heure|Auteur

        Paquet = f"Message|&|{time.strftime('%H:%M:%S')}|{NomUser}|{Contenu}"

        longueurPaquet = len(Paquet) - 1
        longueurPaquet += len(str(longueurPaquet))

        Paquet = Paquet.replace("&", str(longueurPaquet))

    return Paquet

def envoyer():
	global entre, nomUser, filMessages, client_socket, NombreErreurs, CléPubliqueServeur, ModuleServeur
	message = entre.get()

	if len(message) != 0:
    		
		messageInterface = f"[{time.strftime('%H:%M:%S')}] {nomUser} : {message}"
		message = formaterPaquet("Message", nomUser, message)
		message = chiffrement(message)
		message = cryptage(message, CléPubliqueServeur, ModuleServeur)

		ChaineMessage = ""

		for index in message:
			ChaineMessage += str(index) + "/"
    		
		message = ChaineMessage.encode('utf-8')

		try:
			client_socket.send(bytes(message))
		except ConnectionResetError:
			if NombreErreurs < 3:
				tkinter.messagebox.showerror(title="Aïe...", message="Impossible de joindre le serveur. Veuillez réessayer.")
				NombreErreurs += 1
			else:
				tkinter.messagebox.showerror(title="Aïe...", message="Le serveur est injoignable pour le moment. Veuillez vous reconnecter ou bien référez vous à l'aide")
				exit()
		else:
			filMessages.insert(END, messageInterface)
			filMessages.yview(END)
			winsound.PlaySound("Médias/SonEnvoi.wav", winsound.SND_ASYNC)
			entre.delete(0, 'end')

def reception():
	global filMessages, client_socket, CléPrivée, Module
	try:
		messageRecu = client_socket.recv(2048)
		messageRecu = messageRecu.decode("utf-8")

		messageRecu = messageRecu.split("/")
		messageRecu.remove("")
		
		for index in range (len(messageRecu)):
			messageRecu[index] = int(messageRecu[index])

		messageRecu = décryptage(messageRecu, CléPrivée, Module)
		messageRecu = déchiffrement(messageRecu)

		filMessages.insert(END, messageRecu)
		filMessages.yview(END)
		winsound.PlaySound("Médias/SonMessage.wav", winsound.SND_ASYNC)
	except:
		pass
	finally:	
		fen.after(10, reception)








def placeholder(affichage):
	if affichage == True:
		entre.insert(0, "Saisissez votre message ici")
	else:
		entre.delete(0, "end")

def toucheEntre(argumentUseless):
    envoyer()

def affichageConversation():
	global cadreParametres, entre, nomUser, filMessages

	logo.pack_forget()
	cadreParametres.pack_forget()

	filMessages = Listbox(fen, width="70", height="20", activestyle=UNDERLINE, highlightbackground=None, selectbackground=None)
	filMessages.pack(pady=15)

	entre = Entry(fen, width="60")
	entre.pack()

	bouttonEnvoyer = Button(fen, text="Envoyer", command=envoyer)
	bouttonEnvoyer.pack(pady=15)

	entre.bind("<Button-1>", placeholder)
	fen.bind_all('<Return>', toucheEntre)

	reception()
	placeholder(True)

def connexion():
	global IP, Port, nomUser, entreNom, client_socket, entreIP, Role, CléPublique, CléPubliqueServeur, ModuleServeur

	IP = entreIP.get()
	nomUser = entreNom.get()

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.settimeout(5)

	try:
		client_socket.connect((IP, Port))

		données = f"{nomUser}|{CléPublique}|{Module}"
		données = données.encode('utf-8')

		client_socket.send(bytes(données))

		autorisation = client_socket.recv(2048)
		autorisation = autorisation.decode("utf-8")

		client_socket.setblocking(0)
		if autorisation != "False":
			autorisation = autorisation.split("|")
			CléPubliqueServeur = int(autorisation[0])
			ModuleServeur = int(autorisation[1])
			return True
		else:
			tkinter.messagebox.showerror(title="Aïe...", message="Un utilisateur avec le même nom d'utilisateur que le votre est déja connecté. Changez de nom d'utilisateur pour accéder à ce serveur.")	
	except (ConnectionRefusedError, socket.timeout):
		if Role == "Hote":
			return False
		else:
			tkinter.messagebox.showerror(title="Aïe...", message="IL semblerait que l'adresse IP fournie ne soit pas valide. Réferez vous à l'aide pour régler ce problème.")
			return False


def démarrerServeur():
	global entreIP, entrePort, IP, Port, Role
	Role = "Hote"
	IP = entreIP.get()
	Port = int(entrePort.get())
	subprocess.Popen(f"python Serveur.py {IP} {Port}")
	if connexion() == True:
		affichageConversation()






def hote():
	global entrePort, IP, nomUser, cadreParametres, entreNom, entreIP, listeNoms

	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()

	hote = socket.gethostname()
	IP = socket.gethostbyname(hote)

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

	entrePort = Entry(cadreParametres)
	entrePort.insert("end", portRecommande)
	entrePort.pack(anchor=CENTER)

	suggestionNom = choices(listeNoms)

	votreNom = Label(cadreParametres, text="Votre nom d'utilisateur", bg="Grey")
	votreNom.pack(anchor=CENTER, pady=7)

	entreNom = Entry(cadreParametres)
	entreNom.insert("end", suggestionNom)
	entreNom.pack(anchor=CENTER)

	bouttonStart = Button(cadreParametres, text="Démarrer", command=démarrerServeur)
	bouttonStart.pack(pady=20)






def seConnecter():
	global entreIP, entrePort, IP, Port, Role
	Role = "Client"
	Port = int(entrePort.get())
	IP = entreIP.get()
	if connexion() == True: 
		affichageConversation()





def client():
	global entreIP, entrePort, entreNom, cadreParametres, listeNoms
	messageBienvenue.pack_forget()
	cadreBouttons.pack_forget()

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