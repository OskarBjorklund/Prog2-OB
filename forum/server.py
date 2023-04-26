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
            user="root",  # standardanvändarnamn för XAMPP
            password="",  # dito lösenord (en tom sträng)
            database="forum"  # byt namn om din databas heter något annat
)

        self.clients = {}

    def client_accepter(self):
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

        self.clients[address[1]] = client

    def sendto_database(self, info):
        mycursor = self.mydb.cursor()
        print("Uppkopplad till databasen!")
        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
        #val = info.split(",")
        mycursor.execute(sql, info)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")

        # Läsa från databasen
        mycursor.execute("SELECT * FROM user")
        myresult = mycursor.fetchall()
        for x in myresult:
            users = list(x)
        print(users)

    def login(self, credentials):
        if credentials[0] == "1": #Existing user
            info = credentials.pop(0)
            mycursor = self.mydb.cursor()
            print("Uppkopplad till databasen!")
            sql = f"SELECT username AND password FROM user WHERE username = {credentials[1]} AND password = {credentials[2]}"
            mycursor.execute(sql, info)
            self.mydb.commit()
        else: #New user
            info = credentials.pop(0)
            mycursor = self.mydb.cursor()
            print("Uppkopplad till databasen!")
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            mycursor.execute(sql, info)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")


    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True

        while connected:
            recv_msg = client.recv(1024).decode("utf-16")
            
            recv_msg = recv_msg.split(",")

            if len(recv_msg) == 3:
                self.login(recv_msg)
            
        client.close()
    
server = Server()

while True:
    server.client_accepter()