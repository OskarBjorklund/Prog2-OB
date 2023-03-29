#Importering av bibliotek

import socket as sock
import pickle, threading, mysql.connector

HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822

class Server:
    def __init__(self) -> None:
        print("Server is starting...")
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

        self.socket.bind((IP, PORT))
        self.socket.listen(10)
        print(f"Server listening on {IP}:{PORT}")

        self.mydb = mysql.connector.connect(
            host=IP,
            user="root",  # s"tandardanvändarnamn för XAMPP
            password="",  # dito lösenord (en tom sträng)
            database="co"  # byt namn om din databas heter något annat
)

        self.clients = {}

    def client_accepter(self):
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

        self.clients[address[1]] = client

    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True
        while connected:
            msg = client.recv(1024).decode("utf-16")
            if msg == "/disconnect":
                connected = False
    
            print(f"{address}: {msg}")
            
            for c in self.clients.values():
                if c != client:
                    c.send(msg.encode("utf-16"))
            
        client.close()
    
server = Server()

while True:
    server.client_accepter()