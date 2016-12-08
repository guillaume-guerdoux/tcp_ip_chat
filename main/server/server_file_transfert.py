import socket
import threading
import select

import re

from datetime import datetime

from PyQt4.QtCore import QThread

''' ------- Server thread
		Input : pseudo / ip / port / windows where received messages are displayed
		Function : This thread listens to client connecions. If there is a connection, new client is
		added to a client_connected list ------- '''

class Server(QThread):
	def __init__(self, pseudo, host, port, received_message_window):
		QThread.__init__(self)
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
		
		self.running = True
		self.clients_connected = []
		self.client_connected_for_file_sending = []

		# Get thread to send and receiver messages
		#self.receive_client_messages = receive_client_messages
		#self.send_messages_to_clients = send_messages_to_clients

		try:
			# Create main connection
			self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.main_connection.bind((self.host,self.port))
			self.main_connection.listen(5)

			# Create connection for file sending
			self.main_connection_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.main_connection_file.bind((self.host,self.file_port))
			self.main_connection_file.listen(5)
		except OSError:
			print("Le port chosi est déjà pris, veuillez en choisir un autre")
			exit()

	def run(self):

		while self.running == True:
			# Get all new connections asked by client
			try:
				ask_connections, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
				for connection in ask_connections:
					# Accept client connection
					connection_with_client, connection_infos = self.main_connection.accept()
					self.received_message_window.append("Une nouvelle personne a rejoint la conversation")
					# Add client connection to list and to threads list of client connected
					self.clients_connected.append(connection_with_client)

				ask_connections_file, wlist, xlist = select.select([self.main_connection_file], [], [], 0.05)
				for connection in ask_connections_file:
					# Accept client connection for file
					connection_with_client, connection_infos = self.main_connection_file.accept()
					# Add client connection to list and to threads list of client connected for file
					self.client_connected_for_file_sending.append(connection_with_client)
			except OSError:
				self.running = False

''' ------- Receive Message thread
		Input : server / function to broadcast message to other clients / windows where received messages are displayed
		Function : 
		- Listen if new messages are received by server
		- Print received messages in the dedicated window in pyqt interface
		- Call broadcast function to broadcast received messages to all clients ------- '''
class ReceiveMessages(QThread):
	def __init__(self, server, broadcast, received_message_window):
		QThread.__init__(self)
		self.server = server
		self.running = True
		self.broadcast = broadcast
		self.received_message_window = received_message_window

	def run(self):
		while self.running == True:
			clients_to_read = []
			try:
				# Clients to read is a list of client who has sent a message
				clients_to_read, wlist, xlist = select.select(self.server.clients_connected,
					self.server.clients_connected, [],0.05)
			except Exception:
				pass
			else:
				# Print all messages received
				for client in clients_to_read:
					msg_received = client.recv(1024)
					msg_received = msg_received.decode()
					self.received_message_window.append(msg_received)
					if msg_received == "ENDED_SIGNAL_MESSAGE":
						self.kill(client)
					else:
						self.broadcast.broadcast(msg_received, client)


	def kill(self, client):
		#Close the the connection when a client leaves.
		self.server.clients_connected.remove(client)
		client.close()



''' ------- Receive File thread
		Input : server / function to broadcast message to other clients / windows where received messages are displayed
		Function : 
		- Listen if new files are received by server
		- Open a new file named by now's datetime
		- Write received data in opened file
		- Close file and send to client confirmation message ------- '''
class ReceiveClientFiles(threading.Thread):

	def __init__(self, server, broadcast, received_message_window):
		threading.Thread.__init__(self)
		self.server = server
		self.broadcast = broadcast
		self.running = True
		self.received_message_window = received_message_window

	def run(self):
		while self.running == True:
			file_clients_to_read = []
			try:
				# Clients to read is a list of client who has sent a message
				file_clients_to_read, wlist, xlist = select.select(self.server.client_connected_for_file_sending,
					self.server.client_connected_for_file_sending, [],0.05)
			except Exception:
				pass
			else:
				for client in file_clients_to_read:		# Check if it's the coding message to send file
					data = client.recv(1024).decode()
					if data:
						if data =="file_to_be_sent":
							new_filename = "new_file-"+datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
							with open(new_filename, 'wb') as f:  #create the file							
								msg_send = "file_opened"
								client.send(msg_send.encode())	# Tell client server is writing in file
								file_reception_message = client.recv(1024).decode()
								if file_reception_message == "file_is_sending": # Test if client is going to send file
									receiving = True
									while receiving == True:
										file_data = client.recv(1024)
										if not file_data:
											break
										f.write(file_data)		# Write in opnened file
										receiving = False
									f.close()
									self.received_message_window.append("Fichier bien reçu")
								self.broadcast.broadcast_file(new_filename, client)

''' ------- Send Message 
		Input : server
		Function : 
		- Send text message to a client list ------- '''

class SendMessages():


	def __init__(self, server, close_main_connection):
		self.server = server
		self.close_main_connection = close_main_connection

	# Send a message to a list of client
	def send_message_to_list_of_client(self, message, list_client):
		for client in list_client:
			client.send(message.encode())

	def kill(self):
		self.close_main_connection.kill()

''' ------- Send File 
		Input : server / windows where received messages are displayed
		Function : 
		- Send file all clients
		- Send file to client list ------- '''

class SendFile():
	def __init__(self, server, received_message_window):
		self.server = server
		self.received_message_window = received_message_window

	def send_file(self, filename):
		warning_msg = "file_to_send"	
		for client in self.server.client_connected_for_file_sending:
			client.send(warning_msg.encode())		# Send message to tell client a file is to be sent
			file_openend_message = client.recv(1024) # Wait for client to open a new file
			file_openend_message = file_openend_message.decode()
			if file_openend_message == "file_opened":
				sending_file_message = "file_is_sending" 
				client.send(sending_file_message.encode())
				f = open(filename,'rb') #Open the file in reading mode
				l = f.read(1024)
				while (l):
					client.send(l)
					l = f.read(1024)	# Send file data
				f.close() 				# Close file
				False
				self.received_message_window.append("Fichier envoyé")

	def send_file_to_client_list(self, filename, list_client):
		warning_msg = "file_to_be_sent"
		for client in list_client:
			client.send(warning_msg.encode())
			file_openend_message = client.recv(1024)
			file_openend_message = file_openend_message.decode()
			if file_openend_message == "file_opened":
				sending_file_message = "file_is_sending" 
				client.send(sending_file_message.encode())
				f = open(filename,'rb') 
				l = f.read(1024)
				while (l):
					client.send(l)
					l = f.read(1024)
				f.close()
				False
				self.received_message_window.append("Fichier envoyé")

''' ------- Broadcast message to all clients
		Input : send message fuction
		Function : 
		- Function called when server receive a message from one client
		- Brodacast this message to other clients  ------- '''

class Broadcast():

	def __init__(self, send_messages_to_clients):
		self.send_messages_to_clients = send_messages_to_clients

	# Send receive message from one client to all clients
	def broadcast(self, message, client):
		list_clients_who_send_message = list(self.send_messages_to_clients.server.clients_connected)
		list_clients_who_send_message.remove(client) #remove the sender
		self.send_messages_to_clients.send_message_to_list_of_client(message, list_clients_who_send_message)

''' ------- Broadcast file to all clients
		Input : send file fuction
		Function : 
		- Function called when server receive a file from one client
		- Brodacast this message to other clients  ------- '''

class BroadcastFile():

	def __init__(self, send_files_to_clients):
		self.send_files_to_clients = send_files_to_clients

	def broadcast_file(self, filename, client):
		list_clients_to_send_file = list(self.send_files_to_clients.server.client_connected_for_file_sending)
		list_clients_to_send_file.remove(client) #remove the sender
		self.send_files_to_clients.send_file_to_client_list(filename, list_clients_to_send_file)

''' ------- Close connection and thread
		Input : server
		Function : 
		- Close all connection with all clients 
		- Close all threads  ------- '''

class CloseMainConnection():

	def __init__(self, server):
		self.server = server
		self.receive_client_messages = None
		self.receive_client_files = None

	def kill(self):
		self.server.running = False
		self.receive_client_messages.running = False
		self.receive_client_files.running = False
		for client in self.server.clients_connected:
			client.close()
		for client in self.server.client_connected_for_file_sending:
			client.close()
		self.server.main_connection.close()
		self.server.main_connection_file.close()
		print("Connexion fermée")


if __name__ == "__main__":
	#my_ip = input("Quel est ton ip?")
	#pseudo = input('Choisis un pseudo : ')
	my_ip = "127.0.0.1"
	pseudo = "ryan"
	server = Server(pseudo, my_ip)
	close_main_connection = CloseMainConnection(server)
	send_messages_to_clients = SendMessages(server, close_main_connection)
	broadcast = Broadcast(send_messages_to_clients)
	receive_client_messages = ReceiveMessages()

	send_messages_to_clients.start()
	receive_client_messages.start()
	server = Server(pseudo, my_ip, receive_client_messages, send_messages_to_clients)
	server.start()
	receive_client_messages.server = server
	send_messages_to_clients.server = server
