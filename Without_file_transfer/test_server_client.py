import unittest
import socket

from server import Server, ReceiveMessages, SendMessages, Broadcast, CloseMainConnection
from client import Client, SendMessageToServer, ReceiveServerMessages
class TestServerInstantiateClassMethods(unittest.TestCase):

    def create_server(self):
        server = Server("test_pseudo", "127.0.0.1", [])
        return server

    def test_create_server(self):
        server = Server("test_pseudo", "127.0.0.1", [])
        self.assertEqual(server.host, "127.0.0.1")
        self.assertEqual(server.pseudo, "test_pseudo")
        self.assertEqual(server.received_message_window, [])
        self.assertEqual(server.port, 44445)
        self.assertEqual(server.running, True)
        self.assertEqual(server.main_connection, None)
        self.assertEqual(server.clients_connected, [])

    def test_create_client_without_server(self):
        with self.assertRaises(SystemExit) as cm:
            client = Client("test_client", "127.0.0.1", [])
        self.assertEqual(cm.exception.code, None)

    def test_create_client_with_server_connected(self):
        server = self.create_server()
        server.start()
        connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_with_server.connect(("127.0.0.1", 44445))
        connection_with_server.close()
    '''def test_run_server(self):
        server = self.create_server()
        server.start()
        time.sleep(0.000001)'''

if __name__ == '__main__':
    unittest.main()