import socket as sock
import pickle

HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        #self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        connected = True
        while connected:
            msg = input("> ")

            self.socket.send(msg.encode("utf-16"))

            if msg == "/disconnect":
                connected = False
            else:
                msg = self.socket.recv(1024).decode("utf-16")
                print(f"{msg}")

client = Client()