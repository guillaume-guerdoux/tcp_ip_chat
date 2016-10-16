import socket
import threading
import select

''' Server Thread 

Thread which is enabled when server is created. Listen to new client connection '''

class Server(threading.Thread):
	def __init__(self, host, receive_client_messages, send_messages_to_clients):
		threading.Thread.__init__(self)
		self.host = host
		self.running = True
		self.main_connection = None
		self.clients_connected = []
		self.port = 44451
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
class ReceiveMessages(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.server = None
		self.running = True

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
					print(msg_received)
					if msg_received == "fin":
						self.kill(client)

	def kill(self, client):
		self.server.clients_connected.remove(client)
		client.close()
		print("connection with client closed")
		
''' Send message Thread 

Thread which is enabled server to send messages to clients '''
class SendMessages(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.server = None
		self.running = True

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("> ")
			if msg_a_envoyer:
				self.send_message_to_list_of_client(msg_a_envoyer, self.server.clients_connected)
			if msg_a_envoyer == "fin":
				self.kill()
				
				
	# Send a message to a list of client
	def send_message_to_list_of_client(self, message, list_client):
		for client in list_client:
			client.send(message.encode())

	def kill(self):
		self.running = False
		print("send message thread closed")
		self.server.kill()
		
		



my_ip = input("Quel est ton ip?")
receive_client_messages = ReceiveMessages()
send_messages_to_clients = SendMessages()
send_messages_to_clients.start()
receive_client_messages.start()
server = Server(my_ip, receive_client_messages, send_messages_to_clients)
server.start()
receive_client_messages.server = server
send_messages_to_clients.server = server


