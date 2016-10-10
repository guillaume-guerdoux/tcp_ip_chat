''' Version mod. Création d'un serveur Il n'accepte
qu'un seul client (nous verrons plus bas comment en accepter plusieurs) 
et il tourne jusqu'à recevoir du client le message fin.'''
import socket
import threading

hote = '127.0.0.1'
port = 44446

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""
while msg_recu != b"fin":
    msg_recu = connexion_avec_client.recv(1024)
    print(msg_recu.decode())
    msg_a_envoyer = input("> ")
    # Peut planter si vous tapez des caractères spéciaux
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_client.send(msg_a_envoyer)
    # L'instruction ci-dessous peut lever une exception si le message
    # Réceptionné comporte des accents
    
print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()