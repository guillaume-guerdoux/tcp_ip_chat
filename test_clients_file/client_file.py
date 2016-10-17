import socket
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "138.195.110.204"    
port = 60002                

try:
    connexion_avec_serveur.connect((host, port))
except Exception, e:
    alert("Something's wrong with %s. Exception type is %s" % (address, e))

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