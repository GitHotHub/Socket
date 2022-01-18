import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        primoNumero=input("Inserisci il primo numero. exit() per uscire \n")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("Inserisci l'operazione(+,-,*,/,%) \n")
        secondoNumero=float(input("Inserisci il secondo numero \n"))
        messaggio={'primoNumero':primoNumero,
        'operazione':operazione,
        'secondoNumero':secondoNumero}
        messaggio=json.dumps(messaggio)# Trasformiamo l'oggetto in una stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        print("Risultato: ",data.decode())