import sys
from server_file_transfert import Server, ReceiveMessages, SendMessages, Broadcast, CloseMainConnection
from PyQt4 import QtGui


class ServerWindow(QtGui.QWidget):

	def __init__(self, my_ip, pseudo):
		super(ServerWindow, self).__init__()
		#self.title = QtGui.QLabel('Title')
		self.received_message_window = QtGui.QTextEdit()
		self.send_message_windows = QtGui.QLineEdit()
		self.send_message_button = QtGui.QPushButton("Envoyer")
		self.setWindowIcon(QtGui.QIcon('logo_messenger.png'))

		self.server = Server(pseudo, my_ip, self.received_message_window)
		self.close_main_connection = CloseMainConnection(self.server)
		self.send_messages_to_clients = SendMessages(self.server, self.close_main_connection)
		self.broadcast = Broadcast(self.send_messages_to_clients)
		self.receive_client_messages = ReceiveMessages(self.server, self.broadcast, self.received_message_window)

		self.close_main_connection.receive_client_messages = self.receive_client_messages

		self.server.start()
		self.receive_client_messages.start()
		self.initUI()

	def initUI(self):

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(self.received_message_window, 1,0, 4, 2)
		grid.addWidget(self.send_message_windows,5,0)
		grid.addWidget(self.send_message_button,5,1)

		self.setLayout(grid)

		self.send_message_button.clicked.connect(self.send_text_messages)
		self.send_message_windows.returnPressed.connect(self.send_message_button.click)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Ptit Chat - Server')
		self.show()

	def send_text_messages(self):
		message_to_send = self.send_message_windows.text()
		if message_to_send:
			if message_to_send=="fin":
				self.send_messages_to_clients.send_message_to_list_of_client(message_to_send,
					self.send_messages_to_clients.server.clients_connected)
				self.send_messages_to_clients.kill()
			else:
				self.send_messages_to_clients.send_message_to_list_of_client((self.send_messages_to_clients.server.pseudo
					+ ": "
					+ message_to_send), self.send_messages_to_clients.server.clients_connected)
		self.received_message_window.append(message_to_send)
		self.send_message_windows.clear()

def main():
	my_ip = input("Quel est ton ip?")
	pseudo = input('Choisis un pseudo : ')
	app = QtGui.QApplication(sys.argv)
	server_windows = ServerWindow(my_ip, pseudo)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
