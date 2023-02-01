import socket as sock
import pickle, threading

HEADER_LENGTH = 10
IP = "127.0.0.0"
PORT = 8822

class Server:
    def __init__(self) -> None:
        print("Server is starting...")
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

        self.socket.bind((IP, PORT))
        self.socket.listen()
        print(f"Server listening on {IP}:{PORT}")


    
    def accept_clients(self):
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()
        print(f"Active connections: {threading.activeCount() - 1}")

    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True
        while connected:
            msg = client.recv(1024).decode("utf-8")
            if msg == "/disconnect":
                connected = False
            else:
                print(f"{address}: {msg}")
                msg = f"Message recieved: {msg}"
                client.send(msg.encode("utf-8"))
            
        client.close()