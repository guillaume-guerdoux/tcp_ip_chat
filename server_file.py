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

msg_received = ""

while msg_received not in ["oui", "non"]:
	msg_send = "Voulez-vous recevoir un fichier ?"
	connexion_avec_client.send(msg_send.encode())
	print("en attente de la validation client")
	msg_received = connexion_avec_client.recv(1024)
	msg_received = msg_received.decode()
	print (msg_received)

if msg_received == 'non':
	f.close()
	print('le client ne veut pas recevoir le fichier')
	connexion_avec_client.close()
	False
elif msg_received == 'oui':
	filename=input('chemin du fichier : ')
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		connexion_avec_client.send(l)
		print('Sent ',repr(l))
		l = f.read(1024)
	f.close()
	print('Done sending')
	connexion_avec_client.close()
	False



