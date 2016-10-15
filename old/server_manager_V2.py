import socket
import threading
import select
import time
import sys

# Thread to receive client messages
class Chat_with_client(threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.sock = sock
		self.running = True

	def run(self):
		while self.running == True:
			
			inputready,outputready,exceptready \
			= select.select ([self.sock],[self.sock],[])
			for input_item in inputready:
				data = self.sock.recv(1024).decode()
				if data:
					print(data)
			'''if len(inputready) != 0:
				print(inputready)
			for input_item in inputready:
				data = self.sock.recv(1024).decode()
				if data:
					print(data)
				else:
					msg = sys.stdin.readline()
					self.sock.send(msg.encode())
					sys.stdout.write('[Me] '); sys.stdout.flush()''' 
						

#Server thread 
class Server(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.running = True
		self.main_connection = None
		self.clients_connected = []
		self.port = 44445
		self.chat_with_client = []
		# Create thread to send and receiver messages

	def run(self):
		# Create main connection
		self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main_connection.bind((self.host,self.port))
		self.main_connection.listen(5)
		# Start both thread of receiving and sending message
		
		while self.running:
			ask_connections, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
			for connection in ask_connections:
				connection_with_client, connection_infos = self.main_connection.accept()
				print("Connection with client done")
				# Add client connection to list and to threads list of client connected
				self.clients_connected.append(connection_with_client)
				self.chat_with_client.append(Chat_with_client(connection_with_client))
				self.chat_with_client[len(self.chat_with_client)-1].start()
				
# Client thread
class Client(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.running = True
		self.port = 44445

	def run(self):
		self.connection_with_server.connect((self.host, self.port))
		print("Connection with server done")
		while self.running == True:
			msg = "coucou"
			self.connection_with_server.send(msg.encode())
			'''msg_a_envoyer = input("> ")
			msg_recu = self.connection_with_server.recv(1024).decode()
			if msg_a_envoyer:
				self.connection_with_server.send(msg_a_envoyer.encode())
			elif msg_recu :
				print(msg_recu)'''


host = input('Quelle IP voulez-vous contacter ? ')

if host.lower() == 'listen':
	my_ip = input("Quel est ton ip?")
	server = Server(my_ip)
	server.start()
	
	
else:
	client = Client(host)
	client.start()