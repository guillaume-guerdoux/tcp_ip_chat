'''  Création d'un client  Il va tenter de se connecter sur le port 12800 de la machine locale.
 Il demande à l'utilisateur de saisir quelque chose au clavier et envoie ce quelque chose au serveur, puis attend sa réponse.'''
import socket
import threading


class Chat_Send_Message(threading.Thread):
    def __init__(self, connexion_avec_serveur):
        threading.Thread.__init__(self)
        self.connexion_avec_serveur = connexion_avec_serveur

    def run(self):
        msg_a_envoyer = ''
        while msg_a_envoyer != b"fin":
            msg_a_envoyer = input("> ")
            # Peut planter si vous tapez des caractères spéciaux
            msg_a_envoyer = msg_a_envoyer.encode()
            # On envoie le message
            self.connexion_avec_serveur.send(msg_a_envoyer)
            # if msg_a_envoyer == b"fin":
            #	print("Fermeture de la connexion")
            #	connexion_avec_serveur.close()


class Chat_Receive_Message(threading.Thread):
    def __init__(self, connexion_avec_serveur):
        threading.Thread.__init__(self)
        self.connexion_avec_serveur = connexion_avec_serveur

    def run(self):
        msg_recu = ''
        while msg_recu != b"fin":
            msg_recu = self.connexion_avec_serveur.recv(1024)
            print(msg_recu.decode())  # Là encore, peut planter s'il y a des accents
        if msg_recu == b"fin":
            print("Fermeture de la connexion")
            self.connexion_avec_serveur.send(msg_recu)
            connexion_avec_serveur.close()


hote = "127.0.0.1"
port = 44454

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""

while msg_a_envoyer != b"fin":
    # Création des threads
    thread_1 = Chat_Send_Message(connexion_avec_serveur)
    thread_2 = Chat_Receive_Message(connexion_avec_serveur)
    # Lancement des threads
    thread_2.start()
    thread_1.start()
    # Attend que les threads se terminent
    thread_2.join()
    thread_1.join()

''' Version mod. Création d'un serveur Il n'accepte
qu'un seul client (nous verrons plus bas comment en accepter plusieurs)
et il tourne jusqu'à recevoir du client le message fin.'''
import socket
import threading

hote = '127.0.0.1'
port = 44454

msg_recu = b"fin"


class Chat_Send_Message(threading.Thread):
    def __init__(self, connexion_avec_client):
        threading.Thread.__init__(self)
        self.connexion_avec_client = connexion_avec_client

    def run(self):
        msg_a_envoyer = ''
        while msg_a_envoyer != b"fin":
            msg_a_envoyer = input("> ")
            # Peut planter si vous tapez des caractères spéciaux
            msg_a_envoyer = msg_a_envoyer.encode()
            # On envoie le message
            self.connexion_avec_client.send(msg_a_envoyer)
            # if msg_a_envoyer == b"fin":
            #	print("Fermeture de la connexion")
            #	connexion_avec_client.close()


class Chat_Receive_Message(threading.Thread):
    def __init__(self, connexion_avec_client):
        threading.Thread.__init__(self)
        self.connexion_avec_client = connexion_avec_client

    def run(self):
        msg_recu = ''
        while msg_recu != b"fin":
            msg_recu = self.connexion_avec_client.recv(1024)
            print(msg_recu.decode())  # Là encore, peut planter s'il y a des accents
        if msg_recu == b"fin":
            print("Fermeture de la connexion")
            # self.connexion_avec_client.send(msg_a_envoyer)
            connexion_avec_client.close()


connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""

while msg_recu != b"fin":
    # Création des threads
    thread_1 = Chat_Send_Message(connexion_avec_client)
    thread_2 = Chat_Receive_Message(connexion_avec_client)
    # Lancement des threads
    thread_1.start()
    thread_2.start()
    # Attend que les threads se terminent
    thread_1.join()
    thread_2.join()

connexion_principale.close()

