import socket
import threading
import os

hote = '127.0.0.1'
port = 44460

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()

accepte = "non"
num = 0
pourcent = 0
# Boucle temps que l'ont est connecte
############################################
while (connexion_avec_client.connect):
    recu = ""
    recu = connexion_avec_client.recv(1024)
    if not recu: break

    if accepte == "non":  # Condition si on a pas deja envoyer le nom et la taille du fichier
        nomFich = recu.split(b"NAME ")[0]
        nomFich = nomFich.split(b"OCTETS ")[0]
        taille = recu.split(b"OCTETS ")[0]
        #print(" >> Fichier '" + nomFich + "' [" + taille + " Ko]")

        accepte = input(
            " >> Acceptez vous le transfert [o/n] : ")  # demande si on accepte ou pas le transfert

        if accepte == "o" or accepte == "oui":  # Si oui en lenvoi au client et on cree le fichier
            connexion_avec_client.send(b"GO")

            print("on est ligne 37")
            f = open(nomFich, "wb")
            identifier = "oui"
            #taille = int(taille) * 1024  # Conversion de la taille en octets pour le %

        else:
            connexion_avec_client.send(b"Bye")  # Si pas accepte on ferme le programme
            exit()


    elif recu == b"BYE":  # Si on a recu "BYE" le transfer est termine
        f.close()


    else:  # Sinon on ecrit au fur et a mesure dans le fichier
        f.write(recu)

