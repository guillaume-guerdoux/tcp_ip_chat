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
	def __init__(self, pseudo, host, received_message_window):
		self.pseudo = pseudo
		self.host = host
		self.received_message_window = received_message_window
		self.port = 44466
		self.file_port = 44467
		try:
			self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection_with_server.connect((self.host, self.port))
			print("connetion with server done")

			self.file_connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.file_connection_with_server.connect((self.host, self.file_port))
			print("connetion with server file done")

			self.received_message_window.append("Vous avez rejoint la discussion")
		except:
			self.received_message_window.append("Le serveur '" + self.host+ "' est introuvable.")
			exit()
		self.receive_server_messages = None
		self.receive_server_files = None

	def kill(self):
		self.receive_server_messages.running = False
		print("receive server message thread closed")
		self.receive_server_files.running = False
		print("receive server file thread closed")
		self.connection_with_server.close()
		print("Connection closed")
		self.file_connection_with_server.close()
		print("File Connection closed")
		

''' Receive message thread 

Thread which is enabled client to receive messages from server '''

class ReceiveServerMessages(threading.Thread):
	def __init__(self, client, received_message_window):
		threading.Thread.__init__(self)
		self.client = client
		#self.connection_with_server = self.client.connection_with_server
		self.running = True
		self.received_message_window = received_message_window 

	def run(self):
		while self.running == True:
			try:
				inputready,outputready,exceptready \
				= select.select ([self.client.connection_with_server],[],[])
				#print(inputready)
				for input_item in inputready:
					# Handle sockets
					data = self.client.connection_with_server.recv(1024).decode()
					if data:
						self.received_message_window.append(data)
						print(data)
						if data =="fin":
							self.running = False
							self.client.kill()
					else:
						break
			except OSError:
				self.running = False
				self.client.kill()

''' Receive File thread 

Thread which is enabled client to receive files from server '''

class ReceiveServerFiles(threading.Thread):
	def __init__(self, client, received_message_window):
		threading.Thread.__init__(self)
		self.client = client
		#self.connection_with_server = self.client.connection_with_server
		self.running = True
		self.received_message_window = received_message_window 

	def run(self):
		while self.running == True:
			try:
				inputready,outputready,exceptready \
				= select.select([self.client.file_connection_with_server],[],[])
				#print(inputready)
				for input_item in inputready:
					# Handle sockets
					data = self.client.file_connection_with_server.recv(1024).decode()
					if data:
						if data =="file_to_be_sent":
							with open("new_file", 'wb') as f:  #create the file
								print("we write")
								msg_send = "file_opened"
								self.client.file_connection_with_server.send(msg_send.encode())
								file_reception_message = self.client.file_connection_with_server.recv(1024).decode()
								if file_reception_message == "file_is_sending": #file reception started
									receiving = True
									while receiving == True:
										file_data = self.client.file_connection_with_server.recv(1024)
										if not file_data:
											break
										f.write(file_data)
										receiving = False
									f.close()
									self.received_message_window.append("Fichier bien reçu")
					else:
						break
			except OSError:
				self.running = False
				self.client.kill()


if __name__ == "__main__":
	#host = input('Quelle IP voulez-vous contacter ? ')
	#pseudo = input ('Choisis un pseudo : ')
	host = '127.0.0.1'
	pseudo = "test"
	client = Client(pseudo, host)
	receive_server_messages = ReceiveServerMessages(client)
	receive_server_messages.start()
	client.receive_server_messages = receive_server_messages