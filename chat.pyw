import sys
import errno
import socket
import select
import random
from tkinter import *

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = "User" + str(random.randint(1,9999))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(0)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

fen = Tk()
fen.geometry("700x500")
fen.title("Chat Python RSA")
fen.configure(bg="#60a3bc")

filMessages = Listbox(fen, width="100")
filMessages.pack()

entre = Entry(fen)
entre.pack()

def envoyer():
	message = entre.get()
	message = message.encode('utf-8')
	message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(message_header + message)
	filMessages.insert(END, my_username + " : " + entre.get())
	entre.delete(0, 'end')
	
def reception():
	try:
		messageRecu = client_socket.recv(2048)
		print(messageRecu)
		
	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error: {}'.format(str(e)))

	finally:	
		fen.after(3000, reception)

envoyer = Button(fen, text="Envoyer", command=envoyer)
envoyer.pack()

fen.after(100, reception)

fen.mainloop()