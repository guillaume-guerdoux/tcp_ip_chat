import sys
from client_file_transfert import Client, ReceiveServerMessages, ReceiveServerFiles, SendServerFiles
from PyQt4.QtCore import *
from PyQt4.QtGui import *

''' --------------- Client Window ------------
	Pyqt Windows which enables client to have an interface to use ptit chat
	Input : IP / Pseudo / Numéro de port
	Output : Start all threads and display graphic interface'''
class ClientWindow(QWidget):
#Chat window creation

	def __init__(self, my_ip, pseudo, port):
		super(ClientWindow, self).__init__()

		''' ------- Create all components of displayed window ------- '''

		self.received_message_window = QTextEdit()
		self.send_message_windows = QLineEdit()
		self.send_message_button = QPushButton("Envoyer")
		self.choose_file_button = QPushButton("Envoyer fichier")

		''' ------- Create all server classes and thread to enable message sending ------- '''
		self.client = Client(pseudo, my_ip, port, self.received_message_window)
		self.receive_server_messages = ReceiveServerMessages(self.client, self.received_message_window)
		self.receive_server_files = ReceiveServerFiles(self.client, self.received_message_window)
		self.handle_file_sending = SendServerFiles(self.client, self.received_message_window)
		self.client.receive_server_messages = self.receive_server_messages
		self.client.receive_server_files = self.receive_server_files

		''' ------- Start threads ------- '''
		self.receive_server_messages.start()
		self.receive_server_files.start()
		
		self.initUI()

	''' ------- Init windows properties ------- '''
	def initUI(self):
		#Chat window layout and design

		''' ------- Init windows geometrics properties ------- '''
		grid = QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(self.received_message_window, 1, 0, 4, 3)
		grid.addWidget(self.choose_file_button,5,0)
		grid.addWidget(self.send_message_windows,5,1)
		grid.addWidget(self.send_message_button,5,2)
		self.setLayout(grid)
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Ptit Chat - Client')

		''' ------- Init connection between buttons and functions ------- '''
		self.send_message_button.clicked.connect(self.send_text_messages)
		self.send_message_windows.returnPressed.connect(self.send_message_button.click)
		self.choose_file_button.clicked.connect(self.choose_file_to_sent)

		self.show()

	''' ------- Function to send text message
			Input : a text message, if this message is ENDED_SIGNAL_MESSAGE then stop connection with server
			else just send message to server ------- '''
	def send_text_messages(self):
		message_to_send = self.send_message_windows.text()
		if message_to_send:
			#Close client connection
			if message_to_send=="ENDED_SIGNAL_MESSAGE":
				self.client.connection_with_server.send(message_to_send.encode())
				self.client.kill()
			#Send the message with the client pseudo
			else:
				self.client.connection_with_server.send((self.client.pseudo + ': ' + message_to_send).encode())
			self.received_message_window.append(message_to_send)
			self.send_message_windows.clear()

	''' ------- Function to send file
			Input : a file chosen in a window. Send this file to server ------- '''
	def choose_file_to_sent(self):
		#Select the file to be sent.
		dlg = QFileDialog()
		if dlg.exec_():
			filenames = dlg.selectedFiles()
			for file in filenames:
				self.handle_file_sending.send_file(file)

	
	''' ------- Function to stop discution
			When red cross of windows is pressed : close connection ------- '''
	def closeEvent(self, event):
		ended_message = "ENDED_SIGNAL_MESSAGE"
		try:
			self.client.connection_with_server.send(ended_message.encode())
		except OSError:
			pass
		self.client.kill()
		event.accept() # let the window close

def main():
	my_ip = input("Quelle IP voulez-vous contacter ? ")
	pseudo = input('Choisissez un pseudo : ')
	port = input('Port de connection : ')
	app = QApplication(sys.argv)
	client_windows = ClientWindow(my_ip, pseudo, port)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
