import socket                   # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
host = '138.195.110.204'    # Get local machine name
port = 44451                   # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!".encode())

with open('received_file', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')