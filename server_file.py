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
filename=input('chemin du fichier : ') #Select the right fie
msg_send2 = "Envoi du fichier"
connexion_avec_client.send(msg_send2.encode())
msg_received2 = connexion_avec_client.recv(1024) #Wait for opened file on client file
msg_received2 = msg_received2.decode()
if msg_received2 == "file opened":
	msg_send3 = "Go" #Send the file 
	connexion_avec_client.send(msg_send3.encode())
	f = open(filename,'rb') #Open the file in reading mode
	l = f.read(1024)
	while (l):
		connexion_avec_client.send(l)
		print('Sent ',repr(l))
		l = f.read(1024)
	msg_received3 = connexion_avec_client.recv(1024) #Wait for the file to be successfully received
	msg_received3 = msg_received3.decode()
	print (msg_received3)
	f.close() #close the file 
	print('Done sending')
	connexion_avec_client.close()#close the connection
	False



