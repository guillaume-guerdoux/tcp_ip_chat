import socket
import threading
import select

import re

from PyQt4.QtCore import QThread

from datetime import datetime

''' ------- Client
		Input : pseudo / ip / port / windows where received messages are displayed
		Function : Connect to server ------- '''
class Client():
	def __init__(self, pseudo, host, port, received_message_window):
		self.pseudo = pseudo
		# http://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
		regex_match_ip=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",host)
		if not regex_match_ip:
			print("L'adresse IP n'est pas valide")
			exit()
		self.host = host
		self.received_message_window = received_message_window
		try:
			self.port = int(port)
			self.file_port = int(port)+1
		except ValueError:
			print("Le port n'est pas valide.")
			exit()
		try:
			#Create main connection
			self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection_with_server.connect((self.host, self.port))

			self.file_connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.file_connection_with_server.connect((self.host, self.file_port))

			self.received_message_window.append("Vous avez rejoint la discussion")
		except ConnectionRefusedError:
			print("Le serveur '" + self.host+ "' est introuvable")
			exit()

		except OSError:
			print("L'adresse IP '" + self.host+ "' n'est pas valide")
			exit()
		self.receive_server_messages = None
		self.receive_server_files = None

	def kill(self):
		#Close the connection
		self.receive_server_messages.running = False
		self.receive_server_files.running = False
		self.connection_with_server.close()
		self.file_connection_with_server.close()
		print("Connexion fermée")



''' ------- Receive Message thread
		Input : client / windows where received messages are displayed
		Function : 
		- Listen if new messages are received from server
		- Print received messages in the dedicated window in pyqt interface
		- If it's an ended message : close connection ------- '''

class ReceiveServerMessages(QThread):
	def __init__(self, client, received_message_window):
		QThread.__init__(self)
		self.client = client
		self.running = True
		self.received_message_window = received_message_window

	def run(self):
		while self.running == True:
			try:
				inputready,outputready,exceptready \
				= select.select ([self.client.connection_with_server],[],[])
				for input_item in inputready:
					# Handle sockets
					data = self.client.connection_with_server.recv(1024).decode()
					if data:
						if data == "ENDED_SIGNAL_MESSAGE":
							self.received_message_window.append("La connection a été fermée")
							self.running = False
							self.client.kill()
						else:
							self.received_message_window.append(data)
					else:
						break
			except OSError:
				self.running = False
				self.client.kill()

''' ------- Receive File thread
		Input : client / windows where received messages are displayed
		Function : 
		- Listen if new files are received from server
		- Open a new file named by now's datetime
		- Write received data in opened file
		- Close file and send to server confirmation message ------- '''

class ReceiveServerFiles(QThread):
	def __init__(self, client, received_message_window):
		QThread.__init__(self)
		self.client = client
		self.running = True
		self.received_message_window = received_message_window

	def run(self):
		while self.running == True:
			try:
				inputready,outputready,exceptready \
				= select.select([self.client.file_connection_with_server],[],[])
				for input_item in inputready:
					# Handle sockets
					data = self.client.file_connection_with_server.recv(1024).decode()
					if data:
						if data =="file_to_send":
							new_filename = "new_file-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
							with open(new_filename, 'wb') as f:  #create the file
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

''' ------- Send File 
		Input : client / windows where received messages are displayed
		Function : 
		- Send file server ------- '''

class SendServerFiles():
	def __init__(self, client, received_message_window):
		self.client = client
		self.received_message_window = received_message_window

	def send_file(self, filename):
		warning_msg = "file_to_be_sent"
		self.client.file_connection_with_server.send(warning_msg.encode())	# Send message to tell server a file is to be sent
		file_openend_message = self.client.file_connection_with_server.recv(1024) # Wait for server to open a new file
		file_openend_message = file_openend_message.decode()
		if file_openend_message == "file_opened":
			sending_file_message = "file_is_sending"
			self.client.file_connection_with_server.send(sending_file_message.encode())
			f = open(filename,'rb') #Open the file in reading mode
			l = f.read(1024)
			while (l):
				self.client.file_connection_with_server.send(l)
				l = f.read(1024)
			f.close() # Close the file
			False
			self.received_message_window.append("Fichier envoyé")


if __name__ == "__main__":
	host = input('Quelle IP voulez-vous contacter ? ')
	pseudo = input ('Choisis un pseudo : ')
	client = Client(pseudo, host)
	receive_server_messages = ReceiveServerMessages(client)
	receive_server_messages.start()
	client.receive_server_messages = receive_server_messages
