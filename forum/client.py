import socket as sock
import tkinter as tk
import pickle, threading

HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.connected = True
        
        self.load_gui()

        thread = threading.Thread(target=self.recieve_info)
        thread.start()

        self.start_gui()

        # while self.connected:
        #     msg = input("> ")

        #     self.socket.send(msg.encode("utf-16"))

        #     if msg == "/disconnect":
        #         self.connected = False
    

    def load_gui(self):
        self.root = tk.Tk()

        self.l1 = tk.Label(self.root, text = "Name:")
        self.l2 = tk.Label(self.root, text = "Address:")
        self.l3 = tk.Label(self.root, text = "City:")
        self.l4 = tk.Label(self.root, text = "Country:")

        self.l1.grid(row = 0, column = 0, sticky = "W", pady = 2)
        self.l2.grid(row = 1, column = 0, sticky = "W", pady = 2)
        self.l3.grid(row = 2, column = 0, sticky = "W", pady = 2)
        self.l4.grid(row = 3, column = 0, sticky = "W", pady = 2)

        self.e1 = tk.Entry(self.root)
        self.e2 = tk.Entry(self.root)
        self.e3 = tk.Entry(self.root)
        self.e4 = tk.Entry(self.root)

        self.e1.grid(row = 0, column = 1, pady = 2)
        self.e2.grid(row = 1, column = 1, pady = 2)
        self.e3.grid(row = 2, column = 1, pady = 2)
        self.e4.grid(row = 3, column = 1, pady = 2)

        self.bt = tk.Button(self.root, text = "Confirm", command = self.send_info)
    
        self.bt.grid(row = 4, column = 0, columnspan = 2)
    
    def send_info(self):
        pass
        
    def recieve_info(self):
        while self.connected:
            msg = self.socket.recv(1024).decode("utf-16")
            print(f"{msg}")

    def start_gui(self):
        self.root.mainloop()

client = Client()