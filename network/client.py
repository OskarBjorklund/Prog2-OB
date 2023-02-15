import socket as sock
import tkinter as tk
import pickle, threading
from tkinter import messagebox


GAME_WIDTH = 500
GAME_HEIGHT = 500
HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.connected = True
        
        thread = threading.Thread(target=self.recieve_info)
        thread.start()

        while self.connected:
            msg = input("> ")

            self.socket.send(msg.encode("utf-16"))

            if msg == "/disconnect":
                self.connected = False
    

    def recieve_info(self):
        while self.connected:
            msg = self.socket.recv(1024).decode("utf-16")
            print(f"{msg}")

class GUI:
    def __init__(self, client) -> None:
        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)

        self.root.mainloop()

client = Client()
gui = GUI(client)