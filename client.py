import socket
import threading
import select

# TODO : Send files
# TODO Qt for graphic interface
# TODO : login password to access chat
# TODO : login before message

''' Client Class 

Create the object client and connect to server '''
class Client():
	def __init__(self, pseudo, host, received_message_window):
		self.pseudo = pseudo
		self.host = host
		self.received_message_window = received_message_window
		self.port = 44445
		try:
			self.connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection_with_server.connect((self.host, self.port))
			self.received_message_window.append("Vous avez rejoint la discussion")
		except:
			self.received_message_window.append("Le serveur '" + self.host+ "' est introuvable.")
			exit()
		self.receive_server_messages = None

	def kill(self):
		self.receive_server_messages.running = False
		print("receive server message thread closed")
		self.connection_with_server.close()
		print("Connection closed")
		

''' Receive message thread 

Thread which is enabled client to receive messages from server '''

class ReceiveServerMessages(threading.Thread):
	def __init__(self, client, received_message_window):
		threading.Thread.__init__(self)
		self.client = client
		#self.connection_with_server = self.client.connection_with_server
		self.running = True
		self.received_message_window = received_message_window 

	def run(self):
		while self.running == True:
			inputready,outputready,exceptready \
			= select.select ([self.client.connection_with_server],[],[])
			#print(inputready)
			for input_item in inputready:
				# Handle sockets
				data = self.client.connection_with_server.recv(1024).decode()
				if data:
					if data!="file":
						self.received_message_window.append(data)
						print(data)
						if data =="fin":
							self.client.kill()
					else:
						break
				else:
					break

if __name__ == "__main__":
	host = input('Quelle IP voulez-vous contacter ? ')
	pseudo = input ('Choisis un pseudo : ')
	client = Client(pseudo, host)
	receive_server_messages = ReceiveServerMessages(client)
	receive_server_messages.start()
	client.receive_server_messages = receive_server_messages