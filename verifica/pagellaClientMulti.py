from ast import Num
from audioop import add
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except Exception as e:
        print(e)
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    #   di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    #   di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    #   di un voto (valori ammessi 1 ..10)
    #   delle assenze (valori ammessi 1..5) 
    cognomi=["Moraru", "Colombo","Pietra","Ghidoli","Falcone"]
    materie=["Matematica", "Italiano", "Inglese", "Storia", "Geografia"]
    studente=random.randint(0,4)
    materia=random.randint(0,4)
    voto=random.randint(1,10)
    assenze=random.randint(1,5)
    #2. comporre il messaggio, inviarlo come json
    #   esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    dati={'studente':cognomi[studente],'materia':materie[materia],'voto':voto,'assenze':assenze}
    print("Invio dati",dati)
    dati=json.dumps(dati)
    s.sendall(dati.encode("UTF-8"))
    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}
    risposta=s.recv(1024)
    if not risposta:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(threading.current_thread().name)
        #4 stampare la valutazione ricevuta esempio: La valutazione di Studente4 in italiano è Gravemente insufficiente
        risposta=risposta.decode()
        risposta=json.loads(risposta)
        testo=risposta['testo']
        materia=risposta['materia']
        studente=risposta['studente']
        print("La valutazione di "+studente+" in "+materia+" è "+testo)           
    s.close()

#Versione 2 
def genera_richieste2(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except Exception as e:
        print(e)
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)
    #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
    #   generazione di un voto (valori ammessi 1 ..10)
    #   e delle assenze (valori ammessi 1..5) 
    cognomi=["Moraru", "Colombo","Pietra","Ghidoli","Falcone"]
    studente=cognomi[random.randint(0,4)]
    pagella={studente:[("Matematica",random.randint(1,10),random.randint(1,5)),("Italiano",random.randint(1,10),random.randint(1,5)),("Inglese",random.randint(1,10),random.randint(1,5)),("Storia",random.randint(1,10),random.randint(1,5)),("Geografia",random.randint(1,10),random.randint(1,5))]}
    studente=pagella['studente']
    print(studente)
    #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
    #2. comporre il messaggio, inviarlo come json
    pagella=json.dumps(pagella)
    s.sendall(pagella.encode("UTF-8"))
    #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}
    pagella=s.recv(1024)
    if not pagella:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(threading.current_thread().name)
        pagella=pagella.decode()
        pagella=json.loads(pagella)      
    s.close()

#Versione 3
    def genera_richieste3(num,address,port):
        pass
  #....
  #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
  #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
  #                        .....}
  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3

if __name__ == '__main__':
    start_time=time.time()
    # PUNTO A) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)
    # alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    for i in range(NUM_WORKERS):
        genera_richieste1(i,SERVER_ADDRESS,SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    # PUNTO B) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)  
    # tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i thread e attenderne la fine
    for thread in range(NUM_WORKERS):
        trd=threading.Thread(target=genera_richieste2(i,SERVER_ADDRESS,SERVER_PORT))
        threads.append(trd)
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    """start_time=time.time()
    process=[]
    # PUNTO C) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3) 
    # tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i processi e attenderne la fine
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)"""