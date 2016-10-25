import socket
import threading
import select
import time



class Chat_Server(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.running = True
		self.main_connection = None
		#self.connection_infos = None
		self.type_of_thread = "SERVER"
		self.clients_connected = []
	
	def run(self):
		PORT = 44441
		self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.main_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.main_connection.bind((self.host,PORT))
		self.main_connection.listen(5)
		while self.running:
			connection_with_client, connection_infos = self.main_connection.accept()
			chat_with_client = Chat_With_Client(connection_with_client)


class Chat_With_Client(threading.Thread):
	
	def __init__(self, connection_with_client):
		threading.Thread.__init__(self)
		self.connection_with_client = connection_with_client
		self.running = 1

	def run (self):
		while self.running == True:
			msg_received = client.recv(1024)
			msg_received = msg_received.decode()
			print(msg_received)
			if msg_received == "fin":
				print("end of connection with client")
				self.kill()

	def send(self, message):
		for client in self.clients_connected:
			client.send(message.encode())

	def kill(self):
		self.running = False
		self.connection_with_client.close()
		self.main_connection.close()
		print("main socket closed")

class Chat_Client(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
		self.sock = None
		self.running = 1
		self.type_of_thread = "CLIENT"
	def run(self):
		PORT = 44441
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, PORT))
		print("Connection with server done")
		# Select loop for listen
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.sock],[self.sock],[])
			#print(inputready)
			for input_item in inputready:
				# Handle sockets
				data = self.sock.recv(1024).decode()
				if data:
					if data == "fin":
						print("end of connection with server")
						self.kill()
					else:
						print(data)
				else:
					break
			time.sleep(0)

	def send(self, message):
		self.sock.send(message.encode())

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
			text = input('')
			try:
				if text == "fin" and self.send_chat.type_of_thread=="SERVER":
					self.send_chat.send(text)
					print("end of connection with client")
					self.send_chat.kill()
					self.kill()
				elif text=="fin" and self.send_chat.type_of_thread=="CLIENT":
					self.send_chat.send(text)
					print("end of connection with server")
					self.send_chat.kill()
					self.kill()
				else:
					#text = text.encode()
					# On envoie le message
					self.send_chat.send(text)
			except:
				Exception
			time.sleep(0)
	def kill(self):
		self.running = False
		print("close text input")


host = input('Quelle IP voulez-vous contacter ? ')

if host.lower() == 'listen':
	my_ip = input("Quel est ton ip?")
	chat_server = Chat_Server(my_ip)
	chat_server.start()
	text_input = Text_Input(chat_server)
	text_input.start()
else:
	chat_client = Chat_Client(host)
	text_input = Text_Input(chat_client)
	chat_client.start()
	text_input.start()