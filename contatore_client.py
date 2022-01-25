import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        txt=input("Inserisci messaggio. KO per uscire \n")
        if txt=="KO":
            break
        messaggio={'txt':txt}
        messaggio=json.dumps(messaggio)
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        print("Ho ricevuto da te: ",data.decode())