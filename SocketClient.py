# coding: utf-8
import socket

hote = "localhost"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print ("Connection on {}".format(port))

while 1:
    message = input(">>> ").encode('utf-8')
    socket.send(message)

print ("Close")
socket.close()