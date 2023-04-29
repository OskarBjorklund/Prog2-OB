#Importering av bibliotek

import socket as sock
import pickle, threading, mysql.connector, hashlib

HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822
FORMAT = "utf-8"

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

    def login(self, client, credentials):
        if credentials.pop(0) == "1": #Existing user
            mycursor = self.mydb.cursor()
            print("Uppkopplad till databasen!")
            mycursor.execute(f'SELECT password FROM user WHERE username = "{credentials[0].lower()}"')
            myresult = mycursor.fetchall()
            if len(myresult) > 0:
                if myresult[0][0] == encrypt(credentials[1]):
                    print("Correct password")
                    client.send("1".encode(FORMAT)) #Rätt inloggning
                else:
                    print("Incorrect password/Unknown user")
                    client.send("0".encode(FORMAT)) #Fel inloggning
            else:
                print("Incorrect password")
                client.send("0".encode(FORMAT))
    
        else: #New user
            mycursor = self.mydb.cursor()

            print("Uppkopplad till databasen!")

            mycursor.execute("SELECT username FROM user")
            myresult = [name[0] for name in mycursor.fetchall()]

            if credentials[0].lower() in myresult or len(credentials[0]) < 1 or len(credentials[1]) < 1:
                print("Registration not valid")
                client.send("1".encode(FORMAT)) #1 = True, något är fel vid registreringen
            else:
                credentials[1] = encrypt(credentials[1])
                credentials.append(credentials[0])
                credentials[0] = credentials[0].lower()
                print(credentials[1])
                client.send("0".encode(FORMAT))
                sql = "INSERT INTO user (username, password, display_name) VALUES (%s, %s, %s)"
                mycursor.execute(sql, credentials)
                self.mydb.commit()
                print(mycursor.rowcount, "record inserted.")


    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True

        while connected:
            recv_msg = client.recv(1024).decode(FORMAT)
            
            recv_msg = recv_msg.split(",")

            if len(recv_msg) == 3: #Login register
                self.login(client, recv_msg)

        client.close()

def encrypt(password):
        return hashlib.sha256(password.encode(FORMAT)).hexdigest()

    
server = Server()

while True:
    server.client_accepter()