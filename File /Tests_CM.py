import unittest
import socket

from server_file_transfert import Server, ReceiveMessages, SendMessages, Broadcast, CloseMainConnection
from client_file_transfert import Client, ReceiveServerMessages, ReceiveServerFiles

class TestServerInstantiateClassMethods(unittest.TestCase):

    def test_create_server(self):
        server = Server("test_pseudo", "127.0.0.1", [],)
        self.assertEqual(server.host, "127.0.0.1")
        self.assertEqual(server.pseudo, "test_pseudo")
        self.assertEqual(server.received_message_window, [])
        self.assertEqual(server.port, 44445)
        self.assertEqual(server.port_file, 44449)
        self.assertEqual(server.running, True)
        self.assertEqual(server.main_connection, None)
        self.assertEqual(server.client_connected_for_file_sending, [])
        self.assertEqual(server.clients_connected, [])

    if __name__ == '__main__':
        unittest.main()


class TestClientInstantiateClassMethods(unittest.TestCase):

    def test_create_server(self):
        client = Client("test_pseudo", "127.0.0.1",[])
        self.assertEqual(client.pseudo,"test_pseudo")
        self.assertEqual(client.host, "127.0.0.1")
        self.assertEqual(client.port, 44448)
        self.assertEqual(client.file_port, 44449)
        self.assertEqual(client.received_message_window, [])

    if __name__ == '__main__':
        unittest.main()

