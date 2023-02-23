import socket as sock
import tkinter as tk
import pickle, threading
from tkinter import Listbox

GAME_WIDTH = 500
GAME_HEIGHT = 500
HEADER_LENGTH = 10
FORMAT = "utf-16"
BUFFERSIZE = 1024
IP = "localhost"
PORT = 8822

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.client, self.address = self.socket.getsockname()
        self.client_name = str(self.client) + ":" + str(self.address)


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
        self.button1 = tk.Button(self.frame, text = "Rock", command = self.rock)
        
        self.button2 = tk.Button(self.frame, text = "Paper", command = self.paper)

        self.button3 = tk.Button(self.frame, text = "Spock", command = self.spock)

        self.button4 = tk.Button(self.frame, text = "Lizard", command = self.lizard)

        self.button5 = tk.Button(self.frame, text = "Scissors", command = self.scissors)

        self.button = [self.button1, self.button2, self.button3, self.button4, self.button5]

        #Listbox
        self.listbox = Listbox(self.frame, width = 30)
  
        self.listbox.grid(row = 1, rowspan = 3, column = 5, pady = 5)
  
        self.scrollbar = tk.Scrollbar(self.frame)
  
        self.scrollbar.grid(row = 1, rowspan = 3, column = 6, sticky = "news")

        self.listbox.config(yscrollcommand = self.scrollbar.set)
  
        self.scrollbar.config(command = self.listbox.yview)

    def rock(self):
        self.socket.send("rock".encode(FORMAT))

        for b in self.button:
            b.grid_forget()

    def paper(self):
        self.socket.send("paper".encode(FORMAT))

        for b in self.button:
            b.grid_forget()

    def spock(self):
        self.socket.send("spock".encode(FORMAT))

        for b in self.button:
            b.grid_forget()

    def lizard(self):
        self.socket.send("lizard".encode(FORMAT))

        for b in self.button:
            b.grid_forget()
        
    def scissors(self):
        self.socket.send("scissors".encode(FORMAT))

        for b in self.button:
            b.grid_forget()

    def loser(self):
        pass

    def winner(self):
        pass

    def playing(self):
        self.button1.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.button2.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.button3.grid(row = 3, column = 2, padx = 5, pady = 5)
        self.button4.grid(row = 3, column = 3, padx = 5, pady = 5)
        self.button5.grid(row = 3, column = 4, padx = 5, pady = 5)

    def disconnect(self):
        self.socket.send("disconnect".encode(FORMAT))
        self.connected = False
        self.socket.shutdown(sock.SHUT_RDWR)
        self.socket.close()
        self.root.destroy()

    def recieve_info(self):
        while self.connected:
            recv_msg = self.socket.recv(BUFFERSIZE).decode(FORMAT)
            self.listbox.delete(0, tk.END)

            #FIXA VARIABEL
            if len(recv_msg.split(" ")) >= 2:
                for s in recv_msg.split(" ")[ :2]:
                    address, wins = s.split(",")
                    if address == self.client_name:
                        self.playing()

            for s in recv_msg.split(" "):
                address, wins = s.split(",")
                list_item = f"Wins: {wins}, " + address
                if address == self.client_name:
                    list_item += " (You)"
                self.listbox.insert(tk.END, list_item)

    def start_gui(self):
        self.root.mainloop()
        self.disconnect()

client = Client()