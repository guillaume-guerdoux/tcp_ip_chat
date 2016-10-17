import socket                   # Import socket module
import select
port = 60002                   # Reserve a port for your service.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # Create a socket object
host = '138.195.110.204'     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

while True:
    print('Server listening....')
    # Get all new connections asked by client
    ask_connections, wlist, xlist = select.select([s], [], [], 0.05)
    for connection in ask_connections:
        # Accept client connection
        conn, addr = s.accept()
        print("Connection with client done")
        # Add client connection to list and to threads list of client connected
        data = conn.recv(1024)
        print('Server received',data.decode())
        filename='mytext.txt'
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()

        print('Done sending')
        conn.close()