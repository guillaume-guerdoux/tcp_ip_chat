import socket
connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input('Quelle IP voulez-vous contacter ? ')
port = 60003              

connection_with_server.connect((host, port))

data = connection_with_server.recv(1024).decode()
if data == "Voulez-vous recevoir un fichier ?":
	response = input(data)
	connection_with_server.send(response.encode())

filename = input("Quel nom veut tu donner au fichier?")

with open(filename, 'wb') as f:
    print ('file opened')
    while True:
        data = connection_with_server.recv(1024)
        print('receiving data...')
        
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
connection_with_server.close()
print('connection closed')