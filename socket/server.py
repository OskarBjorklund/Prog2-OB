import socket
import pickle



HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, TCP
s.bind((socket.gethostname(), 8822)) #Serverhost, port
s.listen(5) #queue

while True:
    clientsocket, address = s.accept()
    print(f"{address} är uppkopplad")

    dic = {1: "Hej", 2: "Per"}
    msg = pickle.dumps(dic)


    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg

    clientsocket.send(msg)

