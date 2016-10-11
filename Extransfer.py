##################################################################
# PySTFS : Systeme de transfert de fichier par socket en Python
# Version 0.1
# Developpeur : Moreau Guillaume
# Contact : XXXXXXXXXXXXXXXXXXXXXX
# Revision par :
##################################################################

import time, socket, os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print
""
print
" ##################################################################"
print
" # PySTFS : Systeme de transfert de fichier par socket en Python"
print
" # Developpeur : Moreau Guillaume "
print
" # Contact : XXXXXXXXXXXXXXX"
print
" ##################################################################"
print
""

nomFich = raw_input(" >> Nom du fichier a envoyer (ou rien pour recevoir) : ")

##################################################################
# PARTIE ENVOIE DU FICHIER
##################################################################
if nomFich != "":
    try:
        fich = open(nomFich, "rb")  # test si le fichier existe
        fich.close()
    except:
        print
        " >> le fichier '" + nomFich + "' est introuvable."
        time.sleep(2)
        exit()

    octets = os.path.getsize(nomFich) / 1024
    print
    " >> OK : '" + nomFich + "' [" + str(octets) + " Ko]"
    print
    ""

    # Connexion au serveur
    ############################################
    host = raw_input(" >> Adresse IP du serveur : ")
    print
    " >> Connexion en cours avec " + host + "..."
    try:
        socket.connect((host, 2110))  # test si le serveur existe
    except:
        print
        " >> le serveur '" + host + "' est introuvable."
        time.sleep(2)
        exit()

    print
    ""
    print
    " >> Vous etes connecte au serveur, patientez d'une reponse..."
    print
    ""
    socket.send("NAME " + nomFich + "OCTETS " + str(octets))  # Envoi du nom et de la taille du fichier

    # Boucle temps que l'ont est connecte
    ############################################
    while (socket.connect):

        recu = socket.recv(1024)
        if not recu: break

        if recu == "GO":  # Si le serveur accepte on envoi le fichier
            print
            " >> Le serveur accepte le transfert"
            print
            time.strftime(" >> [%H:%M] transfert en cours veuillez patienter...")
            print
            " "

            num = 0
            pourcent = 0
            octets = octets * 1024  # Reconverti en octets
            fich = open(nomFich, "rb")

            if octets > 1024:  # Si le fichier est plus lourd que 1024 on l'envoi par paquet
                for i in range(octets / 1024):

                    fich.seek(num, 0)  # on se deplace par rapport au numero de caractere (de 1024 a 1024 octets)
                    donnees = fich.read(1024)  # Lecture du fichier en 1024 octets
                    socket.send(donnees)  # Envoi du fichier par paquet de 1024 octets
                    num = num + 1024

                    # Condition pour afficher le % du transfert (pas trouve mieu) :
                    if pourcent == 0 and num > octets / 100 * 10 and num < octets / 100 * 20:
                        print
                        " >> 10%"
                        pourcent = 1
                    elif pourcent == 1 and num > octets / 100 * 20 and num < octets / 100 * 30:
                        print
                        " >> 20%"
                        pourcent = 2
                    elif pourcent < 3 and num > octets / 100 * 30 and num < octets / 100 * 40:
                        print
                        " >> 30%"
                        pourcent = 3
                    elif pourcent < 4 and num > octets / 100 * 40 and num < octets / 100 * 50:
                        print
                        " >> 40%"
                        pourcent = 4
                    elif pourcent < 5 and num > octets / 100 * 50 and num < octets / 100 * 60:
                        print
                        " >> 50%"
                        pourcent = 5
                    elif pourcent < 6 and num > octets / 100 * 60 and num < octets / 100 * 70:
                        print
                        " >> 60%"
                        pourcent = 6
                    elif pourcent < 7 and num > octets / 100 * 70 and num < octets / 100 * 80:
                        print
                        " >> 70%"
                        pourcent = 7
                    elif pourcent < 8 and num > octets / 100 * 80 and num < octets / 100 * 90:
                        print
                        " >> 80%"
                        pourcent = 8
                    elif pourcent < 9 and num > octets / 100 * 90 and num < octets / 100 * 100:
                        print
                        " >> 90%"
                        pourcent = 9

            else:  # Sinon on envoi tous d'un coup
                donnees = fich.read()
                socket.send(donnees)

            fich.close()
            print
            ""
            print
            time.strftime(" >> Le %d/%m a %H:%M transfert termine !")
            socket.send("BYE")  # Envoi comme quoi le transfert est fini

##################################################################
# CREATION DU SERVEUR
##################################################################
else:

    print
    " >> Creation du serveur (le pare feu peut alerter)"
    socket.bind(("0.0.0.0", 2110))  # Creation du serveur
    socket.listen(1)  # Mise en ecoute d'un client

    print
    " >> Attente d'une nouvelle connexion..."
    conn, adresse = socket.accept()  # accepte le client

    print
    ""
    print
    " >> Vous etes connecte avec : " + adresse[0]
    print
    ""

    accepte = "non"
    num = 0
    pourcent = 0
    # Boucle temps que l'ont est connecte
    ############################################
    while (conn.connect):
        recu = ""
        recu = conn.recv(1024)
        if not recu: break

        if accepte == "non":  # Condition si on a pas deja envoyer le nom et la taille du fichier
            nomFich = recu.split("NAME ")[1]
            nomFich = nomFich.split("OCTETS ")[0]
            taille = recu.split("OCTETS ")[1]
            print
            " >> Fichier '" + nomFich + "' [" + taille + " Ko]"

            accepte = raw_input(
                " >> Acceptez vous le transfert [o/n] : ")  # demande si on accepte ou pas le transfert

            if accepte == "o" or accepte == "oui":  # Si oui en lenvoi au client et on cree le fichier
                conn.send("GO")
                print
                time.strftime(" >> [%H:%M] transfert en cours veuillez patienter...")
                print
                ""
                f = open(nomFich, "wb")
                identifier = "oui"
                taille = int(taille) * 1024  # Conversion de la taille en octets pour le %

            else:
                conn.send("Bye")  # Si pas accepte on ferme le programme
                exit()


        elif recu == "BYE":  # Si on a recu "BYE" le transfer est termine
            f.close()
            print
            ""
            print
            time.strftime(" >> Le %d/%m a %H:%M transfert termine !")

        else:  # Sinon on ecrit au fur et a mesure dans le fichier
            f.write(recu)

            if taille > 1024:  # Si la taille est plus grande que 1024 on s'occupe du %

                # Condition pour afficher le % du transfert :
                if pourcent == 0 and num > taille / 100 * 10 and num < taille / 100 * 20:
                    print
                    " >> 10%"
                    pourcent = 1
                elif pourcent == 1 and num > taille / 100 * 20 and num < taille / 100 * 30:
                    print
                    " >> 20%"
                    pourcent = 2
                elif pourcent < 3 and num > taille / 100 * 30 and num < taille / 100 * 40:
                    print
                    " >> 30%"
                    pourcent = 3
                elif pourcent < 4 and num > taille / 100 * 40 and num < taille / 100 * 50:
                    print
                    " >> 40%"
                    pourcent = 4
                elif pourcent < 5 and num > taille / 100 * 50 and num < taille / 100 * 60:
                    print
                    " >> 50%"
                    pourcent = 5
                elif pourcent < 6 and num > taille / 100 * 60 and num < taille / 100 * 70:
                    print
                    " >> 60%"
                    pourcent = 6
                elif pourcent < 7 and num > taille / 100 * 70 and num < taille / 100 * 80:
                    print
                    " >> 70%"
                    pourcent = 7
                elif pourcent < 8 and num > taille / 100 * 80 and num < taille / 100 * 90:
                    print
                    " >> 80%"
                    pourcent = 8
                elif pourcent < 9 and num > taille / 100 * 90 and num < taille / 100 * 100:
                    print
                    " >> 90%"
                    pourcent = 9

                num = num + 1024