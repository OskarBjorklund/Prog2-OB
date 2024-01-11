from socket import *
from json import loads, dumps
import threading
from sys import argv



class Connection:
    connections = []

    def __init__(self, socket) -> None:
        self.socket = socket
        self.connections.append(self)
        self.start()

    def start(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        while True:
            data: bytes = self.socket.recv(1024)
            if data:
                print(data.decode())
                self.__send(data)
    
    
    def __send(self, data: bytes):
        for connection in filter(lambda x: x != self, self.connections):
            connection.socket.send(data)

    @classmethod
    def serve(cls):
        threading.Thread(target=cls.__serve).start()

    @classmethod
    def send(cls, data: bytes):
        for connection in cls.connections:
            connection.socket.send(data)

    @staticmethod
    def __serve():
        s = socket(AF_INET, SOCK_STREAM)
        host = "0.0.0.0"
        port = 12345
        s.bind((host, port))
        s.listen()

        while True:
            client, _ = s.accept()
            Connection(client)

    @staticmethod
    def connect(ip: str, port: int):
        s = socket()
        s.connect((ip, port))
        Connection(s)
    
    

if __name__ == "__main__":
    if not (len(argv) == 4 and argv[3] == "--no-serve"):
        Connection.serve()
    if len(argv) >= 3 and argv[1] == "-c":
        Connection.connect(argv[2], 12345)

    while (i:=input()) != "exit":
        Connection.send(i.encode())