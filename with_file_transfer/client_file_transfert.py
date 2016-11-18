import socket
import threading
import select

from PyQt4.QtCore import QThread

from datetime import datetime
# TODO : Send files
# TODO Qt for graphic interface
# TODO : login password to access chat
# TODO : login before message

# TODO : Pass send message to a class in client_file_transfert.py

''' Client Class 

Create the object client and connect to server '''
class Client():
	def __init__(self, pseudo, host, received_message_window):
		self.pseudo = pseudo
		self.host = host
		self.received_message_window = received_message_window
		self.port = 44464
		self.file_port = 44465
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

class ReceiveServerMessages(QThread):
	def __init__(self, client, received_message_window):
		QThread.__init__(self)
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

Thread which enabled client to receive files from server '''

class ReceiveServerFiles(QThread):
	def __init__(self, client, received_message_window):
		QThread.__init__(self)
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
							with open("new_file-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S"), 'wb') as f:  #create the file
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
''' Send File to Server

Thread which enabled client to send files to server '''

class SendServerFiles():
	def __init__(self, client, received_message_window):
		self.client = client
		self.received_message_window = received_message_window 

	def send_file(self, filename):
		# TODO : Be able to select a file in pyqt
		#filename='/media/guillaume/DATA/Cours/Third_year/ptit_chat_project/ptit_chat_POO/with_file_transfer/server/File'
		warning_msg = "file_to_be_sent"
		self.client.file_connection_with_server.send(warning_msg.encode())
		file_openend_message = self.client.file_connection_with_server.recv(1024) #Wait for opened file on client file
		file_openend_message = file_openend_message.decode()
		if file_openend_message == "file_opened":
			sending_file_message = "file_is_sending" #Send the file 
			self.client.file_connection_with_server.send(sending_file_message.encode())
			f = open(filename,'rb') #Open the file in reading mode
			l = f.read(1024)
			while (l):
				self.client.file_connection_with_server.send(l)
				l = f.read(1024)
			f.close() #close the file 
			False
			self.received_message_window.append("Fichier envoyé")


if __name__ == "__main__":
	#host = input('Quelle IP voulez-vous contacter ? ')
	#pseudo = input ('Choisis un pseudo : ')
	host = '127.0.0.1'
	pseudo = "test"
	client = Client(pseudo, host)
	receive_server_messages = ReceiveServerMessages(client)
	receive_server_messages.start()
	client.receive_server_messages = receive_server_messages