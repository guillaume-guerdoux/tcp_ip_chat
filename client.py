import socket
import threading
import select

''' Client Class 

Create the object client and connect to server '''
class Client():
	def __init__(self, host):
		self.host = host
		self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 44447
		self.connection_with_server.connect((self.host, self.port))
		self.send_message_to_server = None
		self.receive_server_messages = None

	def kill(self):
		self.send_message_to_server.running = False
		print("send message thread closed")
		self.receive_server_messages.running = False
		print("receive server message thread closed")
		self.connection_with_server.close()
		print("Connection closed")
		

''' Send message thread 

Thread which is enabled client to send messages to server '''

class SendMessageToServer(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client
		self.connection_with_server = self.client.connection_with_server
		self.running = True

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("> ")
			if msg_a_envoyer:
				self.connection_with_server.send(msg_a_envoyer.encode())
			if msg_a_envoyer == "fin":
				self.client.kill()

''' Receive message thread 

Thread which is enabled client to receive messages from server '''

class ReceiveServerMessages(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client
		self.connection_with_server = self.client.connection_with_server
		self.running = True

	def run(self):
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.connection_with_server],[],[])
			#print(inputready)
			for input_item in inputready:
				# Handle sockets
				data = self.connection_with_server.recv(1024).decode()
				if data:
					print(data)
					if data =="fin":
						self.client.kill()
				else:
					break




host = input('Quelle IP voulez-vous contacter ? ')
client = Client(host)
send_message_to_server = SendMessageToServer(client)
receive_server_messages = ReceiveServerMessages(client)
send_message_to_server.start()
receive_server_messages.start()
client.send_message_to_server = send_message_to_server
client.receive_server_messages = receive_server_messages