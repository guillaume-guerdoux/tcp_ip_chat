import socket                   # Import socket module
import select
port = 60002                   # Reserve a port for your service.
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Create a socket object
host = "127.0.0.1"     # Get local machine name
connexion_principale.bind((host, port))            # Bind to the port
connexion_principale.listen(5)                     # Now wait for client connection.



while True:
	print('Server listening....')
	connexion_avec_client, infos_connexion = connexion_principale.accept()     # Establish connection with client.
	print('Got connection from', addr)
	data = connexion_avec_client.recv(1024)
	data = data.decode()
	print('Server received', data)
	filename='mytext.txt'
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		conn.send(l)
		print('Sent ',repr(l))
		l = f.read(1024)
	f.close()
	print('Done sending')
	connexion_avec_client.close()

