import socket
import sys
import subprocess

def menu():
    #funzione che mostra il menu
    print("sono nel menu")

def receive(s):
    #dim_received = int(s.recv(4096)) #ricevo la dimensione del messaggio
    data_received = s.recv(dim_received).decode('utf-8') #ricevo il messaggio

    return data_received

def send(s, m):
    #s.send(str(sys.getsizeof(m)).encode('utf-8')) #invio la dimensione della risposta al server
    s.send(m.encode('utf-8')) #invio la risposta al server
    #s.close()
def server_connection(id, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_name, server_port))

    return s

if __name__ == '__main__':
    server_id = "252.3.233.130" # ip del container con cui comunicare
    server_port = 12000
    s = server_connection(server_id, server_port)

    #while True:
    #menu()
         #request = input('what do you want to do? ')
    request = 'get_object_list'

    if request == 'get_object_list':
        #s.send(str(sys.getsizeof(request)).encode('utf-8'))
        s.send(request.encode('utf-8'))

    elif r == 'exit':
        print("sono nell'exit")
