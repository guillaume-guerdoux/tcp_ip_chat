'''  Création d'un client  Il va tenter de se connecter sur le port 12800 de la machine locale.
 Il demande à l'utilisateur de saisir quelque chose au clavier et envoie ce quelque chose au serveur, puis attend sa réponse.'''
import socket
import threading



class Chat_Send_Message(threading.Thread):
	
	def __init__(self, connexion_avec_serveur):
		threading.Thread.__init__(self)
		self.connexion_avec_serveur = connexion_avec_serveur
		self.type_of_thread = "CLIENT"
		self.running = 1
		

	def run(self):
		while self.running == True:
			msg_a_envoyer = input("> ")
			msg_envoye = msg_a_envoyer.encode()
			# On envoie le message
			self.connexion_avec_serveur.send(msg_envoye)
			if msg_a_envoyer == "fin":
				print("Fermeture de la connexion client envoi")
				self.closure()
				break
		self.running = False
		print ("le thread est stopé")
	
	def closure(self):
		print ("Fermeture de la connexion")
		connexion_avec_serveur.close()
		print ("La connexion est fermee")
		

class Chat_Receive_Message(threading.Thread):
	
	def __init__(self, connexion_avec_serveur):
		threading.Thread.__init__(self)
		self.connexion_avec_serveur = connexion_avec_serveur
		self.running = 1
		
	def run(self):
		while self.running == True:
			msg_recu = self.connexion_avec_serveur.recv(1024)
			print(msg_recu.decode()) # Là encore, peut planter s'il y a des accent
			if msg_recu.decode() == "fin":
				print("Fermeture de la connexion client recu")
				self.closure()
				break
		self.running = False
		print ("le thread est stopé")

	def closure(self):
		print ("Fermeture de la connexion")
		connexion_avec_serveur.close()
		print ("La connexion est fermee")

hote = "127.0.0.1"
port = 44446

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

# Création des threads
thread_1 = Chat_Send_Message(connexion_avec_serveur)
thread_2 = Chat_Receive_Message(connexion_avec_serveur)
# Lancement des threads
thread_2.start()
thread_1.start()
# Attend que les threads se terminent
thread_2.join()
thread_1.join()


