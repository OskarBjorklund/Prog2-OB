import socket as sock
import pickle, threading

HEADER_LENGTH = 10
IP = "127.0.0.0"
PORT = 8822

class Server:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

        self.socket.bind((IP, PORT))
        self.socket.listen()
    
    def accept_clients(self):
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()

    def client_handler(self):
        print("Bing chilling")