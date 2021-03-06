import socket
import threading
import select

from PyQt4.QtCore import QThread
''' Server Thread 

Thread which is enabled when server is created. Listen to new client connection '''

class Server(QThread):
	def __init__(self, pseudo, host, received_message_window):
		QThread.__init__(self)
		self.pseudo = pseudo
		self.host = host
		self.received_message_window = received_message_window
		self.port = 44445
		self.running = True
		self.main_connection = None
		self.clients_connected = []
		# Get thread to send and receiver messages
		#self.receive_client_messages = receive_client_messages
		#self.send_messages_to_clients = send_messages_to_clients

	def run(self):
		# Create main connection
		self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_connection.bind((self.host,self.port))
		self.main_connection.listen(5)

		while self.running == True:
			# Get all new connections asked by client
			try:
				ask_connections, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
				for connection in ask_connections:
					# Accept client connection
					connection_with_client, connection_infos = self.main_connection.accept()
					print("accepté")
					self.received_message_window.append("Une nouvelle personne a rejoint la conversation")
					# Add client connection to list and to threads list of client connected
					self.clients_connected.append(connection_with_client)
			except OSError:
				self.running = False
				
		

''' Receive message Thread 

Thread which is enabled server to receive client messages '''
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
					print(msg_received)
					if msg_received == "fin":
						self.kill(client)
					else:
						self.broadcast.broadcast(msg_received, client)

	
	def kill(self, client):
		self.server.clients_connected.remove(client)
		client.close()
		print("connection with client closed")
		
''' Send message Thread 

Thread which is enabled server to send messages to clients '''
class SendMessages():
	def __init__(self, server, close_main_connection):
		self.server = server
		self.close_main_connection = close_main_connection

	# Send a message to a list of client
	def send_message_to_list_of_client(self, message, list_client):
		for client in list_client:
			client.send(message.encode())

	def kill(self):
		print("send message thread closed")
		self.close_main_connection.kill()

class Broadcast():
	def __init__(self, send_messages_to_clients):
		self.send_messages_to_clients = send_messages_to_clients

	# Send receive message from one client to all clients
	def broadcast(self, message, client):
		list_clients_who_send_message = list(self.send_messages_to_clients.server.clients_connected)
		list_clients_who_send_message.remove(client)
		self.send_messages_to_clients.send_message_to_list_of_client(message, list_clients_who_send_message) 		

class CloseMainConnection():
	def __init__(self, server):
		self.server = server
		self.receive_client_messages = None

	def kill(self):
		self.server.running = False
		print("Server closed")
		self.receive_client_messages.running = False
		print("receive client message thread closed")
		for client in self.server.clients_connected:
			client.close()
		print("connection with all clients closed")
		self.server.main_connection.close()
		print("main connection closed")


if __name__ == "__main__":
	my_ip = input("Quel est ton ip?")
	pseudo = input('Choisis un pseudo : ')
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


