import socket
import threading
import select
import time



class Chat_Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = 1
		self.sock = None
		self.connexion_principale = None
		self.infos_connexion = None

	def run(self):
		HOST = '127.0.0.1'
		PORT = 44465
		self.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connexion_principale.bind((HOST,PORT))
		self.connexion_principale.listen(1)
		self.sock, self.infos_connexion = self.connexion_principale.accept()
		print("Connection with client done")
		# Select loop for listen
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.sock],[self.sock],[])
			for input_item in inputready:
				# Handle sockets
				data = self.sock.recv(1024).decode()
				if data:
					if data == "fin":
						print("end of connection with client")
						self.kill()
					else:
						print(data)
				else:
					break
				time.sleep(0)
	def kill(self):
		self.running = False
		self.sock.close()
		print("socket of server closed")
		self.connexion_principale.close()
		print("main socket closed")

class Chat_Client(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.sock = None
		self.running = 1
	def run(self):
		PORT = 44465
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, PORT))
		print("Connection with server done")
		# Select loop for listen
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.sock],[self.sock],[])
			for input_item in inputready:
				# Handle sockets
				data = self.sock.recv(1024).decode()
				if data:
					print(data)
					if data == "fin":
						print("end of connection with server")
						self.kill()
					else:
						print(data)
				else:
					break
			time.sleep(0)
	def kill(self):
		self.running = False
		self.sock.close()
		print("socket of client closed")

class Text_Input(threading.Thread):
	def __init__(self, send_chat):
		threading.Thread.__init__(self)
		self.running = 1
		self.send_chat = send_chat

	def run(self):
		while self.running == True:
			text = raw_input('>')
			try:
				self.send_chat.sock.sendall(text)
				if text == "fin":
					print("end of connection")
					self.send_chat.kill()
					print("wait for kill")
					self.kill()
			except:
				Exception
			time.sleep(0)
	def kill(self):
		self.running = False
		print("close text input")


host = raw_input('Quelle IP voulez-vous contacter ? ')

if host == 'listen':
	chat_server = Chat_Server()
	chat_server.start()
	text_input = Text_Input(chat_server)
	text_input.start()

elif host == 'Listen':
	chat_server = Chat_Server()
	chat_server.start()
	text_input = Text_Input(chat_server)
	text_input.start()

else:
	chat_client = Chat_Client(host)
	text_input = Text_Input(chat_client)
	chat_client.start()
	text_input.start()