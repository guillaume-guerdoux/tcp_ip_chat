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
		self.connexion_avec_client = connexion_avec_client
		self.type_of_thread = "SERVER"
		self.running = 1	
		
	def run(self):
		msg_a_envoyer = ''
		while self.running == True:
			msg_a_envoyer = input("> ")
			msg_envoye = msg_a_envoyer.encode()
			# On envoie le message
			self.connexion_avec_client.send(msg_envoye)
			if msg_a_envoyer == "fin":
				self.closure()
				break
		self.running = False
		print("le thread est stopé")
	
	def closure(self):
		print ("Fermeture de la connexion")
		connexion_avec_client.close()
		connexion_principale.close()
		print ("La connexion est fermee")
		
		
class Chat_Receive_Message(threading.Thread):
	
	def __init__(self, connexion_avec_client):
		threading.Thread.__init__(self)
		self.connexion_avec_client=connexion_avec_client
		self.running = 1
		
	def run(self):
		while self.running == True:
			msg_recu = self.connexion_avec_client.recv(1024)
			print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
			if msg_recu.decode() == "fin":
				self.closure()
				break
		self.running = False
		print("le thread est stopé")

	def closure(self):
		print ("Fermeture de la connexion")
		connexion_avec_client.close()
		connexion_principale.close()
		print ("La connexion est fermee")

	

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

# Création des threads
thread_1 = Chat_Send_Message(connexion_avec_client)
thread_2 = Chat_Receive_Message(connexion_avec_client)
# Lancement des threads
thread_1.start()
thread_2.start()
# Attend que les threads se terminent
thread_1.join()
thread_2.join()


