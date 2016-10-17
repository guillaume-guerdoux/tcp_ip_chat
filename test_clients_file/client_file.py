import socket
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "138.195.107.59"    
port = 60003                

try:
    connexion_avec_serveur.connect((host, port))
except Exception:
    alert("Something's wrong with")
print("coucou")
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