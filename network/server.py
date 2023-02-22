import socket as sock
import pickle, threading

HEADER_LENGTH = 10
FORMAT = "utf-16"
BUFFERSIZE = 1024
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

        self.clients = {}

    def client_accepter(self):
        client, address = self.socket.accept()

        address = address[0] + ":" + str(address[1])

        self.clients[address] = client

        self.client_list_update()
    
        recv_thread = threading.Thread(target=self.client_handler, args=(client, address))
        recv_thread.start()

        print(len(self.clients))

    def client_list_update(self):
        client_list = []

        for a in self.clients.keys():
            client_list.append(a)
        client_str = ",".join(client_list)

        for c in self.clients.values():
            c.send(client_str.encode(FORMAT))

    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True
        while connected:
            msg = client.recv(BUFFERSIZE).decode(FORMAT)
            if msg == "disconnect":
                print(f"Client disconnected: {address}")
                del self.clients[address]        
                connected = False 
                client.close()
                self.client_list_update()
                print(len(self.clients))

    def start_game(self):
        if len(self.clients) >= 2:
            print("Working!")
    
server = Server()

while True:
    server.client_accepter()
    server.start_game()