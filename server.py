''' Version mod. Création d'un serveur Il n'accepte
qu'un seul client (nous verrons plus bas comment en accepter plusieurs) 
et il tourne jusqu'à recevoir du client le message fin.'''
import socket
import threading

hote = '127.0.0.1'
port = 44446

class Chat_Send_Message(threading.Thread):
	
	def __init__(self, connexion_avec_client):
		threading.Thread.__init__(self)
		self.connexion_avec_client=connexion_avec_client

	def run(self):
		msg_a_envoyer = ''
		while msg_a_envoyer != b"fin":
			msg_a_envoyer = input("> ")
			# Peut planter si vous tapez des caractères spéciaux
			msg_a_envoyer = msg_a_envoyer.encode()
			# On envoie le message
			self.connexion_avec_client.send(msg_a_envoyer)


class Chat_Receive_Message(threading.Thread):
	
	def __init__(self, connexion_avec_client):
		threading.Thread.__init__(self)
		self.connexion_avec_client=connexion_avec_client

	def run(self):
		msg_recu = ''
		while msg_recu != b"fin":
			msg_recu = self.connexion_avec_client.recv(1024)
			print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents



connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""
msg_a_envoyer = b""
while msg_recu != b"fin" and msg_a_envoyer != b"fin":
	'''msg_recu = connexion_avec_client.recv(1024)
	print(msg_recu.decode())
	msg_a_envoyer = input("> ")
	# Peut planter si vous tapez des caractères spéciaux
	msg_a_envoyer = msg_a_envoyer.encode()
	connexion_avec_client.send(msg_a_envoyer)
	# L'instruction ci-dessous peut lever une exception si le message
	# Réceptionné comporte des accents'''

	# Création des threads
	thread_1 = Chat_Send_Message(connexion_avec_client)
	thread_2 = Chat_Receive_Message(connexion_avec_client)
	# Lancement des threads
	thread_1.start()
	thread_2.start()
	# Attend que les threads se terminent
	thread_1.join()
	thread_2.join()


print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()



