import socket
import threading
import select

# TODO : Send files
# TODO Qt for graphic interface
# TODO : login password to access chat
# TODO : login before message

''' Client Class 

Create the object client and connect to server '''
class Client():
	def __init__(self, pseudo, host):
		self.pseudo = pseudo
		self.host = host
		self.port = 44444
		try:
			self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection_with_server.connect((self.host, self.port))
			print("Connexion établie avec le serveur sur le port {0}".format(self.port))
		except:
			print("Le serveur '" + self.host+ "' est introuvable.")
			exit()
		self.send_message_to_server = None
		self.receive_server_messages = None

	def kill(self):
		self.send_message_to_server.running = False
		print("send message thread closed")
		self.receive_server_messages.running = False
		print("receive server message thread closed")
		self.connection_with_server.close()
		print("Connection closed")
		

''' Send message thread 

Thread which is enabled client to send messages to server '''

class SendMessageToServer(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client
		self.connection_with_server = self.client.connection_with_server
		self.running = True

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("")
			if msg_a_envoyer:
				'''if msg_a_envoyer == "file":
					nomFich = "fichiertexte.txt"
					try:
						msg_to_tell_sent_file = "ISENDYOUAFILE"
						self.connection_with_server.send(msg_to_tell_sent_file.encode())
						fich = open(nomFich, "rb")  # test if file exists
						file_size = os.path.getsize(nomFich)
						num = 0
						if file_size > 1024:  # If file_size > 1024, send file by paquet
							for i in range(file_size / 1024):
								fich.seek(num, 0)  # Move from 1024 octets to 1024 octets
								donnees = fich.read(1024)  # Read file 
								connexion_avec_serveur.send(donnees)  # Send file by paquet
								num = num + 1024
						else:  # Send file in one time
							donnees = fich.read()
							connexion_avec_serveur.send(donnees)
							fich.close()
					except:
						print(" >> le fichier '" + nomFich + "' est introuvable.")
						time.sleep(2)
						exit()
				else:'''
				if msg_a_envoyer == "fin":
					self.connection_with_server.send(msg_a_envoyer.encode())
					self.client.kill()
				else:
					self.connection_with_server.send((self.client.pseudo + ': ' + msg_a_envoyer).encode())
					

''' Receive message thread 

Thread which is enabled client to receive messages from server '''

class ReceiveServerMessages(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client
		self.connection_with_server = self.client.connection_with_server
		self.running = True

	def run(self):
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.connection_with_server],[],[])
			#print(inputready)
			for input_item in inputready:
				# Handle sockets
				data = self.connection_with_server.recv(1024).decode()
				if data:
					print(data)
					if data =="fin":
						self.client.kill()
				else:
					break



if __name__ == "__main__":
	host = input('Quelle IP voulez-vous contacter ? ')
	pseudo = input ('Choisis un pseudo : ')
	client = Client(pseudo, host)
	send_message_to_server = SendMessageToServer(client)
	send_message_to_server.daemon = True 	# To close thread while in input function
	receive_server_messages = ReceiveServerMessages(client)
	send_message_to_server.start()
	receive_server_messages.start()
	client.send_message_to_server = send_message_to_server
	client.receive_server_messages = receive_server_messages