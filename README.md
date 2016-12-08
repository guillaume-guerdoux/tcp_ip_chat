-------------- READ ME ----------------
Use python 3.5.2
Install pyqt4 (sudo apt-get python-qt4)

1. Discussion between two users
- Open two terminals : terminal1 and terminal2 (ctrl+alt+T in Linux)
- terminal1 : cd main/server
- terminal1 : python3 ptit_chat_server.py
- Enter IP address : 127.0.0.1
- Enter pseudo : Jean-Philou
- Enter port : 44444
---> A windows is opened
- terminal2 : cd main/client
- terminal2 : python3 ptit_chat_client.py
- Enter IP address : 127.0.0.1
- Enter pseudo : Client
- Enter port : 44444
---> A windows is opened

You can send message by write in little textedit input then press "enter"
Server sends file : 
	On server window, click on "Envoyer fichier" then choose "server_file" in main/server
	Go to main/client : file is received and named by now.datetime()

Client sends file : 
	On client window, click on "Envoyer fichier" then choose "client_file" in main/client
	Go to main/server : file is received and named by now.datetime()

Close by clicking on red cross 

2. Discussion between several users
-- Open three terminals : terminal1, terminal2, terminal3 (ctrl+alt+T in Linux)
- terminal1 : cd main/server
- terminal1 : python3 ptit_chat_server.py
- Enter IP address : 127.0.0.1
- Enter pseudo : Jean-Philou
- Enter port : 33333
---> A windows is opened
- terminal2 : cd main/client
- terminal2 : python3 ptit_chat_client.py
- Enter IP address : 127.0.0.1
- Enter pseudo : Client
- Enter port : 33333
---> A windows is opened
- terminal3 : cd main/second_client
- terminal3 : python3 ptit_chat_client.py
- Enter IP address : 127.0.0.1
- Enter pseudo : Client
- Enter port : 33333
---> A windows is opened

When one sends a message, it's broadcast to others
Same thing with file, if server of client send a file, everybody receives it



