#Importering av bibliotek
import datetime
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
        self.db_cursor = self.mydb.cursor()
        self.clients = {}

    def client_accepter(self):
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

        self.clients[address[1]] = client

    def database_connect(self, insfet, sql, info):
        print("Database connection established")
        
        if insfet == 1: #INS = INSERT
            self.db_cursor.execute(sql, info)
            self.mydb.commit()
            print(self.db_cursor.rowcount, "record inserted.")
    
        elif insfet == 0: #FET = FETCH
            self.db_cursor.execute(sql)
            result = self.db_cursor.fetchall()
            return(result)

    def login(self, client, credentials):
        if credentials.pop(0) == "1": #Existing user
            myresult = self.database_connect(0, 
                    f'SELECT password, display_name FROM user WHERE username = "{credentials[0].lower()}"', 
                    None)
            if len(myresult) > 0:
                if myresult[0][0] == encrypt(credentials[1]):
                    print("Correct password")
                    client.send(f"1§{myresult[0][1]}".encode(FORMAT)) #Rätt inloggning
                else:
                    print("Incorrect password/Unknown user")
                    client.send("0".encode(FORMAT)) #Fel inloggning
            else:
                print("Incorrect password")
                client.send("0".encode(FORMAT))
    
        else: #New user
            usernames = [name[0] for name in self.database_connect(0, "SELECT username FROM user", None)]

            if credentials[0].lower() in usernames or len(credentials[0]) < 1 or len(credentials[1]) < 1:
                print("Registration not valid")
                client.send("1".encode(FORMAT)) #1 = True, något är fel vid registreringen
            else:
                credentials[1] = encrypt(credentials[1])
                credentials.append(credentials[0])
                credentials[0] = credentials[0].lower()
                client.send("0".encode(FORMAT))
                self.database_connect(1, 
                        "INSERT INTO user (username, password, display_name) VALUES (%s, %s, %s)", 
                        credentials)
    
    def new_post(self, client, post_info):
        if len(self.database_connect(0, f"SELECT title FROM post WHERE title = '{post_info[2]}'", None)) > 0:
            client.send("1".encode(FORMAT))
        else:
            post_input = [post_info[2], post_info[3], post_info[1], 0]
            self.database_connect(1, 
                    "INSERT INTO post (title, text, author_name, answer_count) VALUES (%s, %s, %s, %s)",
                    post_input)
            client.send("0".encode(FORMAT))
    
    def new_comment(self, client, comment_info):
        comment_input = [comment_info[2], comment_info[1], comment_info[3]]
        self.database_connect(1, 
                        "INSERT INTO comment (text, comment_user, connected_post) VALUES (%s, %s, %s)", 
                        comment_input)
        
        answer_count_update = [len(self.database_connect(0, f"SELECT connected_post FROM comment WHERE connected_post='{comment_info[3]}'", None)), comment_info[3]]
        self.database_connect(1, f"UPDATE post SET answer_count=%s WHERE title=%s", answer_count_update )

    def update_post_list(self, client):
        posts = self.database_connect(0, 
            "SELECT title, date_published, author_name, answer_count from post", 
            None)
        if len(posts) > 0:
            client.send(convert_post(posts).encode(FORMAT))
        else:
            client.send("0".encode(FORMAT))
    
    def update_comment_list(self, client, post):
        comments = self.database_connect(0, 
                    f"SELECT text, comment_user, date_commented FROM comment WHERE connected_post = '{post[1]}'", 
                    None)
        if len(comments) > 0:
            client.send(convert_comment(comments).encode(FORMAT))
        else:
            client.send("0".encode(FORMAT))

    def post_info(self, client, title):
        send_post = self.database_connect(0, 
                f"SELECT text from post WHERE title = '{title[1]}'",
                None)
        package = "0§" + send_post[0][0]
        print(package)
        client.send(package.encode(FORMAT))

    def client_handler(self, client, address):
        print(f"New client connected: {address}")
        
        connected = True

        while connected:
            recv_msg = client.recv(1024).decode(FORMAT)
            
            recv_msg = recv_msg.split("§")

            if recv_msg[0] == "1" or recv_msg[0] == "0":
                self.login(client, recv_msg)
            elif recv_msg[0] == "2":
                self.new_post(client, recv_msg)
            elif recv_msg[0] == "3":
                self.post_info(client, recv_msg)
            elif recv_msg[0] == "4":
                self.update_post_list(client)
            elif recv_msg[0] == "5":
                self.new_comment(client, recv_msg)
            elif recv_msg[0] == "6":
                self.update_comment_list(client, recv_msg)

        client.close()

def encrypt(password):
        return hashlib.sha256(password.encode(FORMAT)).hexdigest()

def convert_post(tuple_list):
    post_list = []
    for i, tuples in enumerate(tuple_list):
        #Converts tuples to list in order to convert datetime to str
        post_list.append(list(tuples))
        date_convert = post_list[i][1].strftime("%m/%d/%Y")
        post_list[i][1] = date_convert
        post_list[i][3] = str(post_list[i][3])
        post_list[i] = "¤".join(post_list[i])

    return("§".join(post_list))

def convert_comment(tuple_list):
    comment_list = []
    for i, tuples in enumerate(tuple_list):
        comment_list.append(list(tuples))
        date_convert = comment_list[i][2].strftime("%m-%d-%Y")
        comment_list[i][2] = date_convert
        comment_list[i] = "¤".join(comment_list[i])

    return("§".join(comment_list))

server = Server()

while True:
    server.client_accepter()