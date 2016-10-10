import socket
import threading
import select
import time


class Chat_Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = 1
		self.connexion_avec_client = None
		self.infos_connexion = None
	def run(self):
		HOST = '127.0.0.1'
		PORT = 44456
		connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		connexion_principale.bind((HOST,PORT))
		connexion_principale.listen(1)
		self.connexion_avec_client, self.infos_connexion = connexion_principale.accept()
		# Select loop for listen
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.connexion_avec_client],[self.connexion_avec_client],[])
			for input_item in inputready:
				# Handle sockets
				data = self.connexion_avec_client.recv(1024)
				if data:
					print (data)
				else:
					break
				time.sleep(0)
	def kill(self):
		self.running = 0

class Chat_Client(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.sock = None
		self.running = 1
	def run(self):
		PORT = 44456
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, PORT))
		# Select loop for listen
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.sock],[self.sock],[])
			for input_item in inputready:
				# Handle sockets
				data = self.sock.recv(1024)
				if data:
					print (data)
				else:
					break
			time.sleep(0)
	def kill(self):
		self.running = 0

class Text_Input(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = 1
	def run(self):
		while self.running == True:
			text = raw_input('>')
			try:
				chat_client.sock.sendall(text)
			except:
				Exception
			try:
				chat_server.connexion_avec_client.sendall(text)
			except:
				Exception
			time.sleep(0)
	def kill(self):
		self.running = 0


ip_addr = raw_input('What IP (or type listen)?: ')

if ip_addr == 'listen':
	chat_server = Chat_Server()
	chat_client = Chat_Client()
	chat_server.start()
	text_input = Text_Input()
	text_input.start()

elif ip_addr == 'Listen':
	chat_server = Chat_Server()
	chat_client = Chat_Client()
	chat_server.start()
	text_input = Text_Input()
	text_input.start()

else:
	chat_server = Chat_Server()
	chat_client = Chat_Client()
	text_input = Text_Input()
	chat_client.start()
	text_input.start()