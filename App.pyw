import socket
import random
from tkinter import *

IP = "127.0.0.1"
PORT = 1234
nomUser = "User" + str(random.randint(1,9999))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(0)

def envoyer():
	message = entre.get()
	if len(message) != 0:
		print("Beep")
		message = nomUser + " : " + message
		filMessages.insert(END, message)
		message = message.encode('utf-8')
		client_socket.send(bytes(message))
		entre.delete(0, 'end')
	else:
		entre.delete(0, 'end')
	
def reception():
	try:
		messageRecu = client_socket.recv(2048)
		messageRecu = messageRecu.decode("utf-8")
		filMessages.insert(END, messageRecu)	
	except:
		pass
	finally:	
		fen.after(3000, reception)

def placeholder(affichage):
	print("Je suis la fonction")
	if affichage == True:
		print("IF1")
		entre.insert(0, "Saisissez votre message ici")
	else:
		print("if2")
		entre.delete(0, "end")

fen = Tk()
fen.geometry("550x450")
fen.title("Chat Python RSA")
fen.configure(bg="grey")

filMessages = Listbox(fen, width="70", height="20")
filMessages.pack(pady=15)

entre = Entry(fen, width="60")
entre.pack()

bouttonEnvoyer = Button(fen, text="Envoyer", command=envoyer)
bouttonEnvoyer.pack(pady=15)

entre.bind("<Button-1>", placeholder)

fen.after(100, reception)
placeholder(True)

fen.mainloop()