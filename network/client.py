import socket as sock
import tkinter as tk
import pickle, threading
from tkinter import Listbox

GAME_WIDTH = 500
GAME_HEIGHT = 500
HEADER_LENGTH = 10
FORMAT = "utf-16"
BYTES = 1024
IP = "localhost"
PORT = 8822

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.connected = True

        self.load_gui()

        recv_thread = threading.Thread(target=self.recieve_info)
        recv_thread.start()

        self.start_gui()

        # while self.connected:
        #     msg = input("> ")

        #     self.socket.send(msg.encode(FORMAT))

        #     if msg == "/disconnect":
        #         self.connected = False
    
    def load_gui(self):
        self.root = tk.Tk()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady = 10, padx = 10)

        #Score
        self.display = tk.Label(self.frame, text="Player 1", font=("Arial", 18))
        self.display.grid(row = 1, column = 0, columnspan = 5, padx = 5, pady = 5)
        
        #Winner
        self.winner = tk.Label(self.frame, text="Winner", font=("Arial", 18), width=15, borderwidth=2, relief="solid")
        self.winner.grid(row = 2, column = 0, columnspan = 5, padx = 5, pady = 5)

        #Choice
        self.button1 = tk.Button(self.frame, text = "Rock")
        self.button1.grid(row = 3, column = 0, padx = 5, pady = 5)
        
        self.button2 = tk.Button(self.frame, text = "Paper")
        self.button2.grid(row = 3, column = 1, padx = 5, pady = 5)

        self.button3 = tk.Button(self.frame, text = "Spock")
        self.button3.grid(row = 3, column = 2, padx = 5, pady = 5)

        self.button4 = tk.Button(self.frame, text = "Lizard")
        self.button4.grid(row = 3, column = 3, padx = 5, pady = 5)

        self.button5 = tk.Button(self.frame, text = "Scissors")
        self.button5.grid(row = 3, column = 4, padx = 5, pady = 5)

        self.listbox = Listbox(self.frame)
  
        self.listbox.grid(row = 1, rowspan = 3, column = 5, pady = 5)
  
        self.scrollbar = tk.Scrollbar(self.frame)
  
        self.scrollbar.grid(row = 1, rowspan = 3, column = 6, sticky = "news")

        self.listbox.config(yscrollcommand = self.scrollbar.set)
  
        self.scrollbar.config(command = self.listbox.yview)

    def rock(self):
        pass

    def paper(self):
        pass

    def spock(self):
        pass

    def lizard(self):
        pass
        
    def scissors(self):
        pass

    def recieve_info(self):
        while self.connected:
            listed_client = self.socket.recv(BYTES).decode(FORMAT)
            self.listbox.insert(tk.END, listed_client)

    def start_gui(self):
        self.root.mainloop()

client = Client()