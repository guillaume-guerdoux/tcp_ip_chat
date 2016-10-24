import socket
import threading
import select

from PyQt4.QtCore import QThread
''' Server Thread 

Thread which is enabled when server is created. Listen to new client connection '''

class Server(QThread):
	def __init__(self, pseudo, host, receive_client_messages, send_messages_to_clients):
		QThread.__init__(self)
		self.pseudo = pseudo
		self.host = host
		self.port = 44445
		self.running = True
		self.main_connection = None
		self.clients_connected = []
		# Get thread to send and receiver messages
		self.receive_client_messages = receive_client_messages
		self.send_messages_to_clients = send_messages_to_clients

	def run(self):
		# Create main connection
		self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_connection.bind((self.host,self.port))
		self.main_connection.listen(5)

		while self.running == True:
			# Get all new connections asked by client
			ask_connections, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
			for connection in ask_connections:
				# Accept client connection
				connection_with_client, connection_infos = self.main_connection.accept()
				print("Connection with client done")
				# Add client connection to list and to threads list of client connected
				self.clients_connected.append(connection_with_client)



	# Send receive message from one client to all clients
	def broadcast(self, message, client):
		list_clients_who_send_message = list(self.clients_connected)
		list_clients_who_send_message.remove(client)
		self.send_messages_to_clients.send_message_to_list_of_client(message, list_clients_who_send_message)


	def kill(self):
		self.running = False
		print("Server closed")
		self.receive_client_messages.running = False
		print("receive client message thread closed")
		for client in self.clients_connected:
			client.close()
		print("connection with all clients closed")
		self.main_connection.close()
		print("main connection closed")
		

''' Receive message Thread 

Thread which is enabled server to receive client messages '''
class ReceiveMessages(QThread):
	def __init__(self, received_message_window):
		QThread.__init__(self)
		self.server = None
		self.running = True
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
					print(msg_received)
					if msg_received == "fin":
						self.kill(client)
					else:
						self.server.broadcast(msg_received, client)

	def kill(self, client):
		self.server.clients_connected.remove(client)
		client.close()
		print("connection with client closed")
		
''' Send message Thread 

Thread which is enabled server to send messages to clients '''
class SendMessages(QThread):
	def __init__(self):
		QThread.__init__(self)
		self.server = None
		self.running = True

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("")
			if msg_a_envoyer:
				if msg_a_envoyer=="fin":
					self.send_message_to_list_of_client(msg_a_envoyer, self.server.clients_connected)
					self.kill()
				else:
					self.send_message_to_list_of_client((self.server.pseudo + ": " 
						+ msg_a_envoyer), self.server.clients_connected)
				
	# Send a message to a list of client
	def send_message_to_list_of_client(self, message, list_client):
		for client in list_client:
			client.send(message.encode())

	def kill(self):
		self.running = False
		print("send message thread closed")
		self.server.kill()
		
		


if __name__ == "__main__":
	my_ip = input("Quel est ton ip?")
	pseudo = input('Choisis un pseudo : ')
	receive_client_messages = ReceiveMessages()
	send_messages_to_clients = SendMessages()
	send_messages_to_clients.start()
	receive_client_messages.start()
	server = Server(pseudo, my_ip, receive_client_messages, send_messages_to_clients)
	server.start()
	receive_client_messages.server = server
	send_messages_to_clients.server = server


