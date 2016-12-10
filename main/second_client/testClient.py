import unittest
import socket

from client_file_transfert import Client, ReceiveServerMessages, ReceiveServerFiles

class TestClientInstantiateClassMethods(unittest.TestCase):

    def test_create_client(self):
        client = Client("test_client", "127.0.0.1", 44448, [])
        self.assertEqual(client.pseudo,"test_client")
        self.assertEqual(client.host, "127.0.0.1")
        self.assertEqual(client.port, 44448)
        self.assertEqual(client.file_port, 44449)
#        self.assertEqual(client.received_message_window, [])



if __name__== '__main__':
	unittest.main()
