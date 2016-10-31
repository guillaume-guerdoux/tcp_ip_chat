import sys
from client import Client, ReceiveServerMessages
from PyQt4 import QtGui
import re

class ClientWindow(QtGui.QWidget):

	def __init__(self, my_ip, pseudo):
		super(ClientWindow, self).__init__()
		#self.title = QtGui.QLabel('Title')
		self.received_message_window = QtGui.QTextEdit()
		self.send_message_windows = QtGui.QLineEdit()
		self.send_message_button = QtGui.QPushButton("Envoyer")

		self.client = Client(pseudo, my_ip, self.received_message_window)
		self.receive_server_messages = ReceiveServerMessages(self.client, self.received_message_window)

		self.receive_server_messages.start()
		self.client.receive_server_messages = self.receive_server_messages

		self.initUI()

	def initUI(self):

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(self.received_message_window, 1, 0, 4, 2)
		grid.addWidget(self.send_message_windows,5,0)
		grid.addWidget(self.send_message_button,5,1)

		self.setLayout(grid)

		self.send_message_button.clicked.connect(self.send_text_messages)
		self.send_message_windows.returnPressed.connect(self.send_message_button.click)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Ptit Chat - Client')
		self.show()

	def send_text_messages(self):
		message_to_send = self.send_message_windows.text()
		if message_to_send:
			if message_to_send=="fin":
				self.client.connection_with_server.send(message_to_send.encode())
				self.client.kill()
			else:
				self.client.connection_with_server.send((self.client.pseudo + ': ' + message_to_send).encode())
			self.received_message_window.append(message_to_send)
			self.send_message_windows.clear()

def main():
	my_ip = input("Quelle IP voulez-vous contacter ? ")
	reg = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}?$")
	#Check IP format before startint the connexion
	while not reg.match(my_ip):
		print ("Le format de l'IP n'est pas le bon")
		my_ip = input("Quel est ton ip?")

	pseudo = input('Choisis un pseudo : ')
	app = QtGui.QApplication(sys.argv)

	client_windows = ClientWindow(my_ip, pseudo)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
