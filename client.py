import socket
import sys
import subprocess

def menu():
    #funzione che mostra il menu
    print("**********************MENU*******************\n"
          "Operazioni disponibili:\n"
          "get_object_list\n"
          "prova\n"
          "exit\n"
          "**********************************************\n")

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
    server_port = 8080
    
    while True:
        request = input('what do you want to do? ')

        if request == 'get_object_list':
            message = "GET /objects HTTP/1.1\r\n"
            contentType = "Content-Type: application/x-www-form-urlencoded\r\n"

            s = server_connection(server_id, server_port)
            send(s, message)
            r = receive(s)
            print(r)

        elif request == 'prova':
            #r = requests.get("{}/objects/prova".format(server_id))
            #print(r.text)

            message = "GET /objects/prova HTTP/1.1\r\n"
            contentType = "Content-Type: application/x-www-form-urlencoded\r\n"

            messaggio_finale = message + contentType
            s = server_connection(server_id, server_port)
            send(s, messaggio_finale)
            r = receive(s)
            print(r)

        elif request == 'exit':
            loop = False
            #r = requests.get("{}/objects/exit".format(server_id))

    print("\n")
