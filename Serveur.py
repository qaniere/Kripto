import socket
import errno
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 1234))

server_socket.setblocking(0)

server_socket.listen()

listeClient = []

while True:
	try:
		client_socket, client_address = server_socket.accept()
		listeClient.append(client_socket)
		print("Nouveau client connecté !")
	except IOError:
		time.sleep(0.5)
	for client in listeClient:
		try:
			message = client.recv(2048)
			message = message.decode("utf-8")
			if message == "":
				pass
			else:
				print(message)
				for aenvoyer in listeClient:
					if aenvoyer != client:
						aenvoyer.send(bytes(message, "utf-8"))
					else:
		except Exception as E:
			time.sleep(0.5)