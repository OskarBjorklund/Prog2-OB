import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
s.connect((socket.gethostname(), 8822))

while True:


    full_msg = ""
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"Längd: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            print("Fullständigt meddelande")
            print(full_msg[HEADERSIZE:])

            dic = pickle.loads(full_msg[HEADERSIZE:])
            print(dic)
            
            new_msg = True
            full_msg = b""

print(full_msg)