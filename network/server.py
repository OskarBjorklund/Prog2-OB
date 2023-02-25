import socket as sock
import pickle, threading

HEADER_LENGTH = 10
FORMAT = "utf-16"
BUFFERSIZE = 1024
IP = "localhost"
PORT = 8822
RULES = [
    [-1, 0, 0, 1, 1],
    [1, -1, 1, 0, 0],
    [1, 0, -1, 0, 1],
    [0, 1, 1, -1, 0],
    [0, 1, 0, 1, -1]
]

class Server:
    def __init__(self) -> None:
        print("Server is starting...")
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

        self.socket.bind((IP, PORT))
        self.socket.listen(10)
        print(f"Server listening on {IP}:{PORT}")

        self.clients = {}

        self.player_choice = {}

    def client_accepter(self):
        client, address = self.socket.accept()
        address = address[0] + ":" + str(address[1])

        self.clients[address] = [client, 0, -1]
        self.broadcast_client_list()
    
        recv_thread = threading.Thread(target=self.client_handler, args=(client, address))
        recv_thread.start()

    def broadcast_client_list(self):
        client_str = " ".join([f"{addr},{c[1]},{c[2]}" for addr, c in self.clients.items()])

        for client in self.clients.values():
            client[0].send(client_str.encode(FORMAT))

        print(len(self.clients))

    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True
        while connected:
            recv_msg = client.recv(BUFFERSIZE).decode(FORMAT)

            is_playing = address in list(self.clients.keys())[:2]

            if recv_msg in "01234":
                if is_playing:
                    if not address in self.player_choice.keys():
                        self.player_choice[address] = recv_msg
                    if len(self.player_choice) == 2:
                        self.game_logic()


            elif recv_msg == "disconnect":
                print(f"Client disconnected: {address}")
                del self.clients[address]
                if is_playing:
                    opponent = list(self.clients)[0]
                    self.clients[opponent][1] += 1
                connected = False
                client.close()
                self.broadcast_client_list()
    
    def game_logic(self):
        champ_addr = list(self.clients.keys())[0]
        chall_addr = list(self.clients.keys())[1]
        champ_choice = self.player_choice[champ_addr]
        chall_choice = self.player_choice[chall_addr]

        if RULES[int(champ_choice)][int(chall_choice)] == 1:
            self.clients[champ_addr][1] += 1
            chall = self.clients[chall_addr]
            del self.clients[chall_addr]
            self.clients[chall_addr] = chall

        elif RULES[int(champ_choice)][int(chall_choice)] == 0:
            self.clients[chall_addr][1] += 1
            champ = self.clients[champ_addr]
            del self.clients[champ_addr]
            self.clients[champ_addr] = champ

        elif RULES[int(champ_choice)][int(chall_choice)] == -1:
            pass
        
        self.clients[champ_addr][2] = champ_choice
        self.clients[chall_addr][2] = chall_choice
        self.player_choice.clear()
        self.broadcast_client_list()


            
server = Server()

while True:
    server.client_accepter()