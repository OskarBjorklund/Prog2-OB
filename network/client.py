import socket as sock
import tkinter as tk
import pickle, threading
from tkinter import Listbox
from typing import NamedTuple

GAME_WIDTH = 500
GAME_HEIGHT = 500
HEADER_LENGTH = 10
FORMAT = "utf-16"
BUFFERSIZE = 1024
IP = "localhost"
PORT = 8822
CHOICE = {
    -1: "Left",
    0: "Rock",
    1: "Paper",
    2: "Spock",
    3: "Lizard",
    4: "Scissors"
}


class Player(NamedTuple):
    addr: str
    wins: int
    choice: int

    def is_me(self, addr):
        return True if self.addr == addr else False

class Client:
    def __init__(self) -> None:
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.connect((IP, PORT))
        print(f"Client connected to server at {IP}:{PORT}")

        self.has_made_choice = False
        self.client, address = self.socket.getsockname()
        self.client_name = str(self.client) + ":" + str(address)


        self.connected = True
        self.player_list = []

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
        self.score_display = tk.StringVar()
        self.score_display.set("Not enough players...")
        self.display = tk.Label(self.frame, textvariable = self.score_display, font=("Arial", 18))
        self.display.grid(row = 0, column = 0, columnspan = 5, padx = 5, pady = 5)
        
        #Winner
        self.winner_display = tk.StringVar()
        self.winner = tk.Label(self.frame, textvariable = self.winner_display, font=("Arial", 18), width=15, borderwidth=2, relief="solid")
        self.winner.grid(row = 1, column = 0, columnspan = 5, padx = 5, pady = 5)

        #Choice
        self.button1 = tk.Button(self.frame, text = "Rock", command = self.rock)
        self.button2 = tk.Button(self.frame, text = "Paper", command = self.paper)
        self.button3 = tk.Button(self.frame, text = "Spock", command = self.spock)
        self.button4 = tk.Button(self.frame, text = "Lizard", command = self.lizard)
        self.button5 = tk.Button(self.frame, text = "Scissors", command = self.scissors)
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5]

        #Listbox
        self.listbox = Listbox(self.frame, width = 30)
        self.listbox.grid(row = 0, rowspan = 3, column = 5, pady = 5)
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(row = 0, rowspan = 3, column = 6, sticky = "news")
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)

    def rock(self):
        self.socket.send("0".encode(FORMAT))
        self.hide_buttons()

    def paper(self):
        self.socket.send("1".encode(FORMAT))
        self.hide_buttons()

    def spock(self):
        self.socket.send("2".encode(FORMAT))
        self.hide_buttons()

    def lizard(self):
        self.socket.send("3".encode(FORMAT))
        self.hide_buttons()
        
    def scissors(self):
        self.socket.send("4".encode(FORMAT))
        self.hide_buttons()

    def show_buttons(self):
        self.button1.grid(row = 2, column = 0, padx = 5, pady = 5)
        self.button2.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.button3.grid(row = 2, column = 2, padx = 5, pady = 5)
        self.button4.grid(row = 2, column = 3, padx = 5, pady = 5)
        self.button5.grid(row = 2, column = 4, padx = 5, pady = 5)
    
    def hide_buttons(self):
        self.has_made_choice = True
        for b in self.buttons:
            b.grid_forget()

    # self.score_display.set(f"{} vs {}")

    def disconnect(self):
        self.socket.send("disconnect".encode(FORMAT))
        self.connected = False
        self.socket.shutdown(sock.SHUT_RDWR)
        self.socket.close()
        self.root.destroy()

    def recieve_info(self):
        while self.connected:
            msg = self.socket.recv(BUFFERSIZE).decode(FORMAT)
            new_player_list = self.parse_players(msg)

            # Not enough players
            if len(new_player_list) < 2:
                self.score_display.set("Not enough players...")
                self.update_player_list(new_player_list)
                continue

            # Display matchup
            self.score_display.set(f"{new_player_list[0].addr} vs {new_player_list[1].addr}")

            # Is part of round
            competing_addrs = list(map(lambda p: p.addr, new_player_list[:2]))
            if self.client_name in competing_addrs:
                i = competing_addrs.index(self.client_name)
                made_choice = new_player_list[i].choice != -1
                if not self.has_made_choice or made_choice:
                    self.show_buttons()

            if len(self.player_list) < 2:
                self.update_player_list(new_player_list)
                continue

            # Both players have made a choice
            if new_player_list[0].choice != -1 or new_player_list[1].choice != -1:
                self.determine_outcome(new_player_list)
            

            self.update_player_list(new_player_list)
            
    def determine_outcome(self, new_player_list):
        champion_stands = self.player_list[0].addr == new_player_list[0].addr
        challenger_prevails = self.player_list[1].addr == new_player_list[0].addr

        room_size_changed = len(new_player_list) != len(self.player_list)
        score_changed = self.player_list[0].wins != new_player_list[0].wins
        draw = champion_stands and not challenger_prevails and not score_changed and not room_size_changed
        
        result = champion_stands if not draw else -1
        
        if self.client_name == self.player_list[0].addr:
            pov = 1
        elif self.client_name == self.player_list[1].addr:
            pov = 0
        else:
            pov = -1

        challenger_left = not champion_stands and not challenger_prevails
        champion_left = self.player_list[0].addr not in list(map(lambda p: p.addr, new_player_list))
        
        print(f"prev: {self.player_list[0].choice}, {self.player_list[1].choice} | curr: {new_player_list[0].choice}, {new_player_list[1].choice}")
        champ_choice = new_player_list[0].choice if not champion_left else -1
        chall_choice = new_player_list[1].choice if not challenger_left else -1

        self.display_results(result, pov, champ_choice, chall_choice)

    def display_results(self, result: int, pov: int, champ_choice: int, chall_choice: int):
        """
        RESULT: 1 (Champion won), 0 (Challenger won), -1 (Draw)
        POV: 1 (Champion), 0 (Challenger), -1 (Spectator)
        CHOICE: konstant variabeln i början av koden
        """
        self.score_display.set(f"{CHOICE[champ_choice]} vs {CHOICE[chall_choice]}")
        if result == -1:
            self.winner_display.set(f"Game draw!")
            return
        if pov == 1:
            if result == 1:
                self.winner_display.set("You won!")
            elif result == 0:
                self.winner_display.set("You lost!")
        elif pov == 0:
            if result == 1:
                self.winner_display.set("You lost!")
            elif result == 0:
                self.winner_display.set("You won!")
        elif pov == -1:
            if result == 1:
                self.winner_display.set(f"Champion stands!")
            if result == 0:
                self.winner_display.set(f"Challenger wins!")

    def update_player_list(self, new_player_list):
        self.listbox.delete(0, tk.END)

        for player in new_player_list:
            list_item = f"Wins: {player.wins}, " + player.addr
            if player.addr == self.client_name:
                list_item += " (You)"
            self.listbox.insert(tk.END, list_item)

        self.player_list = new_player_list
        
    @staticmethod
    def parse_players(msg):
        players = []
        for s in msg.split(" "):
            addr, wins, choice = s.split(",")
            players.append(Player(addr, int(wins), int(choice)))
        return players

    def start_gui(self):
        self.root.mainloop()
        self.disconnect()

client = Client()