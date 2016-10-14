import socket
import threading
import select
import time

# Thread to receive client messages
class Receive_client_messages(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.clients_connected = []
		self.running = True

	def run(self):
		while self.running == True:
			clients_to_read = []
			try:
				clients_to_read, wlist, xlist = select.select(self.clients_connected,
					self.clients_connected, [],0.05)
			except select.error:
				pass
			else:
				for client in clients_to_read:
					msg_received = client.recv(1024)
					msg_received = msg_received.decode()
					print(msg_received)
					if msg_received == "fin":
						print("end of connection with client")
						self.kill()
# Thread to send messages to client
class Send_messages_to_clients(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.clients_connected = []
		self.running = True

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("> ")
			if msg_a_envoyer:
				self.send_message_to_list_of_client(msg_a_envoyer, self.clients_connected)
			if msg_a_envoyer == "fin":
				#self.closure()
				break
				self.running = False
				print("le thread est stopé")

	def send_message_to_list_of_client(self, message, list_client):
		for client in list_client:
			client.send(message.encode())

#Server thread 
class Server(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.running = True
		self.main_connection = None
		self.clients_connected = []
		self.port = 44443
		# Create thread to send and receiver messages
		self.receive_client_messages = Receive_client_messages()
		self.send_messages_to_clients = Send_messages_to_clients()

	def run(self):
		# Create main connection
		self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_connection.bind((self.host,self.port))
		self.main_connection.listen(5)
		# Start both thread of receiving and sending message
		self.receive_client_messages.start()
		self.send_messages_to_clients.start()
		while self.running:
			ask_connections, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
			for connection in ask_connections:
				connection_with_client, connection_infos = self.main_connection.accept()
				print("Connection with client done")
				# Add client connection to list and to threads list of client connected
				self.clients_connected.append(connection_with_client)
				self.receive_client_messages.clients_connected.append(connection_with_client)
				self.send_messages_to_clients.clients_connected.append(connection_with_client)
				
# Client thread
class Client(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running = True
		self.port = 44443

	def run(self):
		self.connection_with_server.connect((self.host, self.port))
		print("Connection with server done")
		while self.running == True:
			msg_a_envoyer = input("> ")
			msg_recu = self.receive_message()
			if msg_a_envoyer:
				self.send_message(msg_a_envoyer)
				if msg_a_envoyer == "fin":
					#self.closure()
					break
			elif msg_recu :
				print(msg_recu)
			if msg_recu == "fin":
				#self.closure()
				break
				self.running = False
				print("le thread est stopé")

	def send_message(self, message):
		self.connection_with_server.send(message.encode())

	def receive_message(self):
		return self.connection_with_server.recv(1024).decode()


host = input('Quelle IP voulez-vous contacter ? ')

if host.lower() == 'listen':
	my_ip = input("Quel est ton ip?")
	server = Server(my_ip)
	server.start()
	
else:
	client = Client(host)
	client.start()
