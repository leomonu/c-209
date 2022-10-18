


import socket
from  threading import Thread
from typing import Counter
import time
IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}


def handleShowList(client):
    global clients
    counter = 0
    for c in clients:
        counter+=1
    
    client_addr=clients[c]["address"][0]
    connected_with=client[c]["connected_with"]
    msg=""
    if connected_with:
        msg=f"{counter},{c},{client_addr},Connected With{connected_with},tiul,\n"
    
    else :
        msg=f"{counter},{c},{client_addr},Available,tiul,\n"
    
    client.send(msg.encode('utf-8'))
    time.sleep(1)





def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList(client)
    



def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER


    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass

def removeClient():
    pass


def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client,addr)

        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")


    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))


    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()



setup_thread = Thread(target=setup)          
setup_thread.start()