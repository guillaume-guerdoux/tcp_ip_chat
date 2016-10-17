'''  Création d'un client  Il va tenter de se connecter sur le port 12800 de la machine locale.
 Il demande à l'utilisateur de saisir quelque chose au clavier et envoie ce quelque chose au serveur, puis attend sa réponse.'''
import socket
import threading
import os
import time



hote = "138.195.107.59"
port = 44460

nomFich = "test"

try:
    fich = open(nomFich, "rb")  # test si le fichier existe
    fich.close()
except:
    print(" >> le fichier '" + nomFich + "' est introuvable.")
    time.sleep(2)
    exit()

octets = os.path.getsize(nomFich) / 1024

try:
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))  # test si le serveur existe
    print("Connexion établie avec le serveur sur le port {}".format(port))
except:
    print(" >> le serveur '" + hote + "' est introuvable.")
    time.sleep(2)
    exit()

nomFich = nomFich.encode()
connexion_avec_serveur.send(nomFich)

while (connexion_avec_serveur.connect):

    recu = connexion_avec_serveur.recv(1024)
    if not recu: break

    if recu == "GO":  # Si le serveur accepte on envoi le fichier
        print(" >> Le serveur accepte le transfert")

        num = 0
        pourcent = 0
        octets = octets * 1024  # Reconverti en octets
        fich = open(nomFich, "rb")

        if octets > 1024:  # Si le fichier est plus lourd que 1024 on l'envoi par paquet
            for i in range(octets / 1024):

                fich.seek(num, 0)  # on se deplace par rapport au numero de caractere (de 1024 a 1024 octets)
                donnees = fich.read(1024)  # Lecture du fichier en 1024 octets
                connexion_avec_serveur.send(donnees)  # Envoi du fichier par paquet de 1024 octets
                num = num + 1024

        else:  # Sinon on envoi tous d'un coup
            donnees = fich.read()
            connexion_avec_serveur.send(donnees)

            fich.close()

