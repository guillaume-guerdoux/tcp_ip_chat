import socket
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"    
port = 60002                
connexion_avec_serveur.connect((host, port))

<<<<<<< Updated upstream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
host = '138.195.110.204'    # Get local machine name
port = 44451                   # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!".encode())
=======
print("client connecté")
connexion_avec_serveur.send(b"Hello server!")
>>>>>>> Stashed changes

with open('received_file', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = connexion_avec_serveur.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
connexion_avec_serveur.close()
print('connection closed')