import datetime, json, os
import socket as sock
import threading, mysql.connector, hashlib

HEADER_LENGTH = 10
IP = "localhost"
PORT = 8822
FORMAT = "utf-8"

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class Server:
    def __init__(self) -> None:
        print("Server is starting...")
        self.db_name = "forum_test"
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        self.setup_database()

        self.socket.bind((IP, PORT))
        self.socket.listen(10)
        print(f"Server listening on {IP}:{PORT}")

    def setup_database(self):
        """
        Creates database if not already existing
        """
        self.mydb = mysql.connector.connect(
            host=IP,
            user="root",  # default name for XAMPP
            password=""  # password
        )
        self.db_cursor = self.mydb.cursor()

        # Predefined tables
        with open(os.path.join(DIR_PATH, "database.json")) as f:
            self.db_tables = json.load(f)

        # Help from Kalle
        self.db_cursor.execute("SHOW DATABASES")

        # Creates database if it does not exist
        if self.db_name not in [x[0] for x in self.db_cursor.fetchall()]:
            self.db_cursor.execute(f"CREATE DATABASE {self.db_name}")
        self.mydb.connect(database=self.db_name) # Connects to database
        
        # Ensures all neccessary tables exists 
        self.db_cursor.execute("SHOW TABLES")
        existing_tables = [x[0] for x in self.db_cursor.fetchall()]
        for table_name in self.db_tables.keys():
            if table_name not in existing_tables:
                # If table in database does not exist
                required_columns = self.db_tables[table_name]
                sql_commands = []
                for name, cmd in required_columns.items():
                    # Format column name into sql command
                    sql_commands.append(cmd % name)
                self.db_cursor.execute(f"CREATE TABLE {table_name} ({', '.join(sql_commands)})")
                #ex CREATE TABLE post (id bigint(20) NOT NULL PRIMARY KEY AUTO_INCREMENT, name varchar(100) ... )

    def client_accepter(self):
        """
        Accepts clients and starts a thread to handle information
        sent by the client. Therefore, each client can handeled simultaneously.
        """
        client, address = self.socket.accept()
        thread = threading.Thread(target=self.client_handler, args=(client, address))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

    def database_execute(self, insfet, sql, info):
        """
        Method that handles all fetches and commits to the database.
        The argument insfet (insert/fetch) is either 1 or 0, 1 means insert and
        0 means fetch. sql is the mySQL code. Info only needed if
        the server needs to insert something into the database, otherwise it is
        None. Depending on insert or fetch, the method either just inserts information
        or returns the fetched results.
        """

        print("Database connection established")
        
        if insfet == 1: #INS = INSERT
            self.db_cursor.execute(sql, info)
            self.mydb.commit()
            print(self.db_cursor.rowcount, "record inserted.")
    
        elif insfet == 0: #FET = FETCH
            self.db_cursor.execute(sql)
            result = self.db_cursor.fetchall()
            return(result) #Returns the fetched results

    def login(self, client, credentials):
        """
        Login method. This method tries to fetch the password used by the username
        from the database that the client input. If the server cannot find any password
        the username does not exist. If the password exists, the method compares
        the password listed in the database with the password the client input was but encrypted.
        If the credentials are correct the server will send the information to the clienten
        letting them know they are allowed to connect. If the password is incorrect,
        the server will tell the client it is wrong. 
        """
        
        myresult = self.database_execute(0, 
                f'SELECT password, display_name FROM user WHERE username = "{credentials[1].lower()}"', 
                None)
        if len(myresult) > 0:
            if myresult[0][0] == encrypt(credentials[2]):
                client.send(f"1§{myresult[0][1]}".encode(FORMAT)) # Correct login
            else:
                client.send("0".encode(FORMAT)) # Wrong login
        else:
            client.send("0".encode(FORMAT))
                
    def register(self, client, credentials):
        """
        This method registers a new user. Firstly, all usernames are fetched from the database.
        These usernames are then compared to the username that the client want to register with.
        If the username already exists in the database, the server will tell the user that
        the username is already in use. The server will either accept usernames or passwords
        smaller than 1. If everything goes right the credentials will be insertet into the
        database.
        """
        usernames = [name[0] for name in self.database_execute(0, "SELECT username FROM user", None)]

        if credentials[1].lower() in usernames or len(credentials[1]) < 1 or len(credentials[2]) < 1:
            client.send("1".encode(FORMAT)) # 1 = True, something went wrong
        else:
            register = [credentials[1].lower(), encrypt(credentials[2]), credentials[1]]

            self.database_execute(1, 
                    "INSERT INTO user (username, password, display_name) VALUES (%s, %s, %s)", 
                    register)
            client.send("0".encode(FORMAT)) # 0 = False, nothing went wrong.

    def new_post(self, client, post_info):
        """
        This method uploads new posts to the database. To begin with, the method checks if the title
        alredy exists, if it does, the client will be told that the title is already in use.
        Otherwise the post will be uploaded to the database.
        """
        if len(self.database_execute(0, f"SELECT title FROM post WHERE title = '{post_info[2]}'", None)) > 0:
            client.send("1".encode(FORMAT)) # Something went wrong
        else:
            post_input = [post_info[2], post_info[3], post_info[1], 0]
            self.database_execute(1, 
                    "INSERT INTO post (title, text, author_name, answer_count) VALUES (%s, %s, %s, %s)",
                    post_input)
            client.send("0".encode(FORMAT)) # Tell client everything went good
    
    def new_comment(self, comment_info):
        """
        This method functions almost the same as the new_post method.
        The comments are directly inserted into the database. The answer count is also
        updated on posts with this method. Everytime, after a comment is added,
        the lenght of all comments on the same post is set as the current answer count on the
        specific post.
        """
        comment_input = [comment_info[2], comment_info[1], comment_info[3]] #Text, user, post
        self.database_execute(1, 
                        "INSERT INTO comment (text, comment_user, connected_post) VALUES (%s, %s, %s)", 
                        comment_input)
        
        answer_count_update = [len(self.database_execute(0, f"SELECT connected_post FROM comment WHERE connected_post='{comment_info[3]}'", None)), comment_info[3]]
        self.database_execute(1, f"UPDATE post SET answer_count=%s WHERE title=%s", answer_count_update )

    def update_post_list(self, client):
        """
        All posts are fetched from the database
        and sent to the client. If no posts exists, the server sends a "0" to the client.
        """
        posts = self.database_execute(0, 
            "SELECT title, date_published, author_name, answer_count from post", 
            None)
        if len(posts) > 0:
            client.send(convert_post(posts).encode(FORMAT))
        else:
            client.send("0".encode(FORMAT))
    
    def update_comment_list(self, client, post):
        """
        Almost identical to update_post_list but with comments instead.
        The only diffrence is that this method needs the specific post as an
        argument.
        """
        comments = self.database_execute(0, 
                    f"SELECT text, comment_user, date_commented FROM comment WHERE connected_post = '{post[1]}'", 
                    None)
        if len(comments) > 0:
            client.send(convert_comment(comments).encode(FORMAT))
        else:
            client.send("0".encode(FORMAT))

    def post_info(self, client, title):
        """
        This method sends the client the text to the corresponding post. This is
        done through fetching the text from post where the title is the the title of
        the post the client wants.
        """
        send_post = self.database_execute(0, 
                f"SELECT text from post WHERE title = '{title[1]}'",
                None)
        package = "0§" + send_post[0][0]
        client.send(package.encode(FORMAT))

    def client_handler(self, client, address):
        """
        This method is run on a thread. The method is always waiting
        for messages from clients and depening on the number in the beginning
        of their message, the server knows what the client wants.
        """
        print(f"New client connected: {address}")
        
        connected = True

        while connected:
            recv_msg = client.recv(1024).decode(FORMAT)
            
            recv_msg = recv_msg.split("§")

            if recv_msg[0] == "0": # Register
                self.register(client, recv_msg)
            elif recv_msg[0] == "1": # Login
                self.login(client, recv_msg)
            elif recv_msg[0] == "2": # New post
                self.new_post(client, recv_msg)
            elif recv_msg[0] == "3": # Post text
                self.post_info(client, recv_msg)
            elif recv_msg[0] == "4": # Update post list
                self.update_post_list(client)
            elif recv_msg[0] == "5": # New comment
                self.new_comment(recv_msg)
            elif recv_msg[0] == "6": # Update comment list
                self.update_comment_list(client, recv_msg)

        client.close()

def encrypt(password):
    """
    Returns an encrypted version of the given password.
    As a result, there is no way for server or database to know
    what the client's real password is.
    """
    return hashlib.sha256(password.encode(FORMAT)).hexdigest()

def convert_post(tuple_list):
    """
    When fetching the posts from the database they are returned as a list containing tuples.
    Socket is trash and can only send strings, therefore, this function converts the nested tuples
    into a string separated by "§" and "¤" and returns it.
    """
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
    """
    This function does the exact same thing as convert_post, except that
    the comment_list is a little different
    """
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