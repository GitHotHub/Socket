import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("[*] In ascolto su %s:%d"%(HOST,PORT))
    clientsocket, address=s.accept()
    cont=0
    with clientsocket as cs:
        print("Connessione da ",address)
        while True:
            cont+=1
            data=cs.recv(1024)
            if not data:
                break
            data=data.decode()
            data=json.loads(data)
            print(data['txt'])
            txt=str(cont)+") "+data['txt']
            cs.sendall(txt.encode("UTF-8"))