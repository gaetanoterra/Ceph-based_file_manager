import socket
import sys
import subprocess

def menu():
    #funzione che mostra il menu
    print("**********************MENU*******************\n"
          "Operazioni disponibili:\n"
          "get_object_list\n"
          "get_object\n"
          "exit\n"
          "**********************************************\n")

def receive(s, b):
    #dim_received = int(s.recv(4096)) #ricevo la dimensione del messaggio
    if b == True:
        data_received = s.recv(4096)
    else:
        data_received = s.recv(4096).decode('utf-8') #ricevo il messaggio

    return data_received

def send(s, m, b):
    #s.send(str(sys.getsizeof(m)).encode('utf-8')) #invio la dimensione della richiesta al server
    if b == True:
        s.send(m)
    else:
        s.send(m.encode('utf-8')) #invio la risposta al server
    
def server_connection(id, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_name, server_port))

    return s

if __name__ == '__main__':
    server_id = "252.3.233.130" # ip del container con cui comunicare
    server_port = 8080
    binary_obj = False
    
    while True:
        request = input('what do you want to do? ')

        if request == 'get_object_list':
            message = "GET /objects HTTP/1.1\r\n"
            contentType = "Content-Type: application/x-www-form-urlencoded\r\n"

            s = server_connection(server_id, server_port)
            binary_obj = False #il messaggio che voglio inviare non è binario => lo devo codificare per la send
            
            send(s, message, binary_obj)
            #binary_obj = False => il messaggio che voglio ricevere non è binario => lo devo decodificare quando arriva
            r = receive(s, binary_obj)
            print(r)
            s.close()

        elif request == 'get_object':
            #r = requests.get("{}/objects/prova".format(server_id))
            #print(r.text)
            file_name = input('which fil do you want to download? ')
            
            message = "GET /objects/{} HTTP/1.1\r\n".format(file_name)
            contentType = "Content-Type: application/x-www-form-urlencoded\r\n"

            messaggio_finale = message + contentType
            s = server_connection(server_id, server_port)
            send(s, messaggio_finale)
            binary_obj = True #il messaggio che voglio ricevere è binario => non lo devo decodificare
            
            r = receive(s, binary_obj)
            if r.decode('utf-8') == "oggetto richiesto non trovato!":
                print(r.decode('utf-8'))
            else:
                file = open(file_name, "wb")
                file.write(r)
                file.close()

            s.close()

        elif request == 'exit':
            loop = False
            #r = requests.get("{}/objects/exit".format(server_id))

    print("\n")
