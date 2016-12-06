import sys
from server_file_transfert import (Server, ReceiveMessages,ReceiveClientFiles, 
SendMessages, SendFile, Broadcast, BroadcastFile, CloseMainConnection)
#from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ServerWindow(QWidget):

	def __init__(self, my_ip, pseudo, port):
		super(ServerWindow, self).__init__()
		#self.title = QtGui.QLabel('Title')
		self.received_message_window = QTextEdit()
		self.send_message_windows = QLineEdit()
		self.send_message_button = QPushButton("Envoyer")
		self.choose_file_button = QPushButton("Choose file")
		self.setWindowIcon(QIcon('logo_messenger.png'))

		self.server = Server(pseudo, my_ip, port, self.received_message_window)
		self.close_main_connection = CloseMainConnection(self.server)
		self.send_messages_to_clients = SendMessages(self.server, self.close_main_connection)
		self.handle_file_sending = SendFile(self.server, self.received_message_window)
		self.broadcast = Broadcast(self.send_messages_to_clients)
		self.broadcast_file = BroadcastFile(self.handle_file_sending)
		self.receive_client_messages = ReceiveMessages(self.server, self.broadcast, self.received_message_window)
		self.receive_client_files = ReceiveClientFiles(self.server, self.broadcast_file, self.received_message_window)

		self.close_main_connection.receive_client_messages = self.receive_client_messages
		self.close_main_connection.receive_client_files = self.receive_client_files

		self.server.start()
		self.receive_client_messages.start()
		self.receive_client_files.start()
		self.initUI()

	def initUI(self):

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(self.received_message_window, 1,0, 4, 3)
		grid.addWidget(self.choose_file_button,5,0)
		grid.addWidget(self.send_message_windows,5,1)
		grid.addWidget(self.send_message_button,5,2)

		self.setLayout(grid)

		self.send_message_button.clicked.connect(self.send_text_messages)
		self.send_message_windows.returnPressed.connect(self.send_message_button.click)
		self.choose_file_button.clicked.connect(self.choose_file_to_sent)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Ptit Chat - Server')
		self.show()

	def send_text_messages(self):
		message_to_send = self.send_message_windows.text()
		if message_to_send:
			if message_to_send=="ENDED_SIGNAL_MESSAGE":
				self.send_messages_to_clients.send_message_to_list_of_client(message_to_send,
					self.send_messages_to_clients.server.clients_connected)
				self.send_messages_to_clients.kill()
				self.received_message_window.append(message_to_send)
			else:
				self.send_messages_to_clients.send_message_to_list_of_client((self.send_messages_to_clients.server.pseudo
					+ ": "
					+ message_to_send), self.send_messages_to_clients.server.clients_connected)
				self.received_message_window.append(message_to_send)
		self.send_message_windows.clear()

	def choose_file_to_sent(self):
		dlg = QFileDialog()
		if dlg.exec_():
			filenames = dlg.selectedFiles()
			for file in filenames:
				self.handle_file_sending.send_file(file)

	def closeEvent(self, event):
		ended_message = "ENDED_SIGNAL_MESSAGE"
		self.send_messages_to_clients.send_message_to_list_of_client(ended_message,
			self.send_messages_to_clients.server.clients_connected)
		self.send_messages_to_clients.kill()
		event.accept() # let the window close

def main():
	my_ip = input("Quel est ton ip?")
	pseudo = input('Choisissez un pseudo : ')
	port = input('Port de connection : ')
	app = QApplication(sys.argv)
	server_windows = ServerWindow(my_ip, pseudo, port)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
