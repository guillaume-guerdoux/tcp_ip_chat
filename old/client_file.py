import socket
connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input('Quelle IP voulez-vous contacter ? ')
port = 60004              

connection_with_server.connect((host, port))

filename = input("Quel nom veut tu donner au fichier?")

data2 = connection_with_server.recv(1024).decode()
if data2 == "Envoi du fichier" : 
	with open(filename, 'wb') as f:  #create the file
		print ('file opened')
		msg_send = "file opened"
		connection_with_server.send(msg_send.encode())
		data4 = connection_with_server.recv(1024).decode()
		if data4 == "Go": #file reception started
			while True:
				data3 = connection_with_server.recv(1024)
				print('receiving data...')
				print('data=%s', (data3))
				if not data3:
					break
				f.write(data3)#write the received data in the file
				msg_sent2 = "fichier recu"
				connection_with_server.send(msg_send.encode())
			f.close() #close the file
			print('Successfully get the file')
			connection_with_server.close() #close the connection
			print('connection closed')