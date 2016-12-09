import unittest
import socket

from server_file_transfert import Server, ReceiveMessages, SendMessages
from server_file_transfert import Broadcast, CloseMainConnection

class TestServerInstantiateClassMethods(unittest.TestCase):

    def test_create_server(self):
        server = Server("test_pseudo", "127.0.0.1", 44464, [])
        self.assertEqual(server.host, "127.0.0.1")
        self.assertEqual(server.pseudo, "test_pseudo")
        self.assertEqual(server.received_message_window, [])
        self.assertEqual(server.port, 44464)
        self.assertEqual(server.file_port, 44465)
        self.assertEqual(server.running, True)
        self.assertEqual(server.main_connection, None)
        self.assertEqual(server.client_connected_for_file_sending, [])
        self.assertEqual(server.clients_connected, [])


if __name__== '__main__':
	unittest.main()
