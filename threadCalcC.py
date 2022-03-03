#calcolatrice client per calcoServer.py versione multithread
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    primoNumero=random.randint(0,100)
    operazione=["+","-","*","/","%",]
    scelta=random.randint(0,4)
    secondoNumero=random.randint(0,100)
    richiesta={'primoNumero':primoNumero,'operazione':operazione[scelta],'secondoNumero':secondoNumero}
    print("Invio richiesta",richiesta)
    
    richiesta=json.dumps(richiesta)
    s.sendall(richiesta.encode("UTF-8"))
    data=s.recv(1024)

    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Risultato: {data.decode()}")
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    for i in range(NUM_WORKERS):
        print("ok")
        genera_richieste(i,SERVER_ADDRESS,SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    for i in range(NUM_WORKERS):
        trd=threading.Thread(target=genera_richieste(i,SERVER_ADDRESS,SERVER_PORT))
        threads.append(trd)
    for thread in threads:
        # 5 avvio tutti i thread
        thread.start()
    for thread in threads:
        # 6 aspetto la fine di tutti i thread 
        thread.join()
    
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    """start_time=time.time()
    process=[]
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    # 8 avvio tutti i processi
    # 9 aspetto la fine di tutti i processi 
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)"""