#TODO : ajouter droit d'acces 
#choix du fichier

import socket                   # Import socket module
import select


port = 60003                   # Reserve a port for your service.
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Create a socket object
host = input("Quel est ton ip?")				   # Get local machine name
connexion_principale.bind((host, port))            # Bind to the port
connexion_principale.listen(5)                     # Now wait for client connection.


print('Server listening....')
connexion_avec_client, infos_connexion = connexion_principale.accept()     # Establish connection with client.
print('Got connection from', infos_connexion)
filename=input('chemin du fichier : ')
msg_send2 = "Envoi du fichier"
connexion_avec_client.send(msg_send2.encode())
msg_received2 = connexion_avec_client.recv(1024)
msg_received2 = msg_received2.decode()
if msg_received2 == "file opened":
	msg_send3 = "Go"
	connexion_avec_client.send(msg_send3.encode())
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		connexion_avec_client.send(l)
		print('Sent ',repr(l))
		l = f.read(1024)
	msg_received3 = connexion_avec_client.recv(1024)
	msg_received3 = msg_received3.decode()
	print (msg_received3)
	f.close()
	print('Done sending')
	connexion_avec_client.close()
	False



