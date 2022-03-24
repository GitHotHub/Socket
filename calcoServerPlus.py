import socket
import json
from threading import Thread

SERVER_ADDRESS='127.0.0.1'
SERVER_PORT=22225
class Server():
    def __init__(self,address,port):
        self.address=address
        self.port=port

    def avvia_server(self):
        sock_listen=socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock_listen.bind((self.address, self.port))
        sock_listen.listen(5)
        print("Server in ascolto su %s." %str((self.address, self.port)))
        return sock_listen
    
    def accetta_conn(self,sock_listen):
        while True:
            sock_service,addr_client=sock_listen.accept()
            print("\nConnessione ricevuta da "+ str(addr_client))
            print("\nCreao un thread per servire le richieste ")
            try:
                Thread(target=self.ricevi_comandi, args=(sock_service,addr_client)).start()
            except:
                print("Il thread non si avvia")
                sock_listen.close()

    def ricevi_comandi(self,sock_service,addre_client):
        print("Avviato")
        while True:
            dati=sock_service.recv(2048)
            if not dati:
                print("Fine dati dal client. Reset")
                break
            dati=dati.decode()
            dati=json.loads(dati)
            print("Ricevuto: '%s" % dati)
            if dati=='0':
                print("Chiudo la connessione con " + str(addre_client))
                break
            risultato=0
            oper,n1,n2= dati.split(";")
            if oper=="+":
                risultato=int(n1)+int(n2)
            
            if oper=="-":
                risultato=int(n1)-int(n2)

            if oper=="*":
                risultato=int(n1)*int(n2)

            if oper=="/":
                risultato=int(n1)/int(n2)
            
            dati=f"Risposta a : {str(addre_client)}. Il risultato dall'operazione({n1} {oper} {n2}) è : {risultato} "
            dati= dati.encode()
            sock_service.send(dati)
        sock_service.close()

s1=Server(SERVER_ADDRESS,SERVER_PORT)
sock_lis=s1.avvia_server()
s1.accetta_conn(sock_lis)