import sys
from client_file_transfert import Client, ReceiveServerMessages, ReceiveServerFiles, SendServerFiles
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ClientWindow(QWidget):

	def __init__(self, my_ip, pseudo):
		super(ClientWindow, self).__init__()
		#self.title = QtGui.QLabel('Title')
		self.received_message_window = QTextEdit()
		self.send_message_windows = QLineEdit()
		self.send_message_button = QPushButton("Envoyer")
		self.choose_file_button = QPushButton("Choose file")
		self.setWindowIcon(QIcon('logo_messenger.png'))

		self.client = Client(pseudo, my_ip, self.received_message_window)
		self.receive_server_messages = ReceiveServerMessages(self.client, self.received_message_window)
		self.receive_server_files = ReceiveServerFiles(self.client, self.received_message_window)
		self.handle_file_sending = SendServerFiles(self.client, self.received_message_window)

		self.receive_server_messages.start()
		self.receive_server_files.start()
		self.client.receive_server_messages = self.receive_server_messages
		self.client.receive_server_files = self.receive_server_files


		self.initUI()

	def initUI(self):

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(self.received_message_window, 1, 0, 4, 3)
		grid.addWidget(self.choose_file_button,5,0)
		grid.addWidget(self.send_message_windows,5,1)
		grid.addWidget(self.send_message_button,5,2)


		self.setLayout(grid)

		self.send_message_button.clicked.connect(self.send_text_messages)
		self.send_message_windows.returnPressed.connect(self.send_message_button.click)
		self.choose_file_button.clicked.connect(self.choose_file_to_sent)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Ptit Chat - Client')
		self.show()

	def send_text_messages(self):
		message_to_send = self.send_message_windows.text()
		if message_to_send:
			if message_to_send=="ENDED_SIGNAL_MESSAGE":
				self.client.connection_with_server.send(message_to_send.encode())
				self.client.kill()
			else:
				self.client.connection_with_server.send((self.client.pseudo + ': ' + message_to_send).encode())
			self.received_message_window.append(message_to_send)
			self.send_message_windows.clear()

	def choose_file_to_sent(self):
		dlg = QFileDialog()
		if dlg.exec_():
			filenames = dlg.selectedFiles()
			for file in filenames:
				self.handle_file_sending.send_file(file)

	# Handle closure of window (when client clicks on red cross)
	def closeEvent(self, event):
		ended_message = "ENDED_SIGNAL_MESSAGE"
		self.client.connection_with_server.send(ended_message.encode())
		self.client.kill()
		event.accept() # let the window close

def main():
	#my_ip = input("Quelle IP voulez-vous contacter ? ")
	#pseudo = input('Choisis un pseudo : ')
	my_ip = "127.0.0.1"
	pseudo = "test"
	app = QApplication(sys.argv)
	client_windows = ClientWindow(my_ip, pseudo)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
