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

def receive(s):
    #dim_received = int(s.recv(4096)) #ricevo la dimensione del messaggio
    data_received = s.recv(1024)
    print("data_received: {}".format(data_received))

    header = data_received.decode('utf-8')

    header = header.split("\n\n")[0] # selezione l'header
    l = header.split("Content-Length:")     # seleziono tutti i campi dell'header per prendere l'ultimo che corrisponde a Content-Length
    dim = l[1]
    l = int(dim.split("\r\n")[0])             # qui prendo la dimensione del body
    missing_len = l - (1024 - len(header))  # io potrei aver ricevuto parte del body di dimensione (1024 - dimensione dell'hader), vedo quanto è lungo il body in totale, e vedo quanto ho ricevuto attualmente e mi aspetto la differenze
    if missing_len > 0:
        missing_data_received = s.recv(missing_len)
        body = ((data_received + missing_data_received).decode('utf-8')).split("\n\n")[1]
    else:
        body = data_received.decode('utf-8').split("\n\n")[1]
    
    print("header: {}".format(header))
    print("l: {}".format(l))
    print("missing_len: {}".format(missing_len))
    print("body: {}".format(body))

    return body

def send(s, m, b):
    s.send(m.encode('utf-8')) #invio la risposta al server
    
def server_connection(id, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_name, server_port))

    return s

def create_HTTP_request(request_line, body):
    request_line = request_line
    header = header = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n".format(sys.getsizeof(body))
    empty_line = "\n"
    body = body
    message = request_line + header + empty_line + body

    return message 

def create_HTTP_response(status_line, body):
    status_line = status_line
    header = header = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n".format(sys.getsizeof(body))
    empty_line = "\n"
    body = body
    message = status_line + header + empty_line + body
    
    return message

if __name__ == '__main__':
    server_id = "252.3.233.130" # ip del container con cui comunicare
    server_port = 8080
    binary_obj = False
    
    while True:
        request = input('what do you want to do? ')

        ### struttura del messaggio request HTTP
        ### riga di richiesta "GET /objects HTTP/1.1\r\n"
        ### header
        ### riga vuota
        ### body

        ### struttura del messaggio response HTTP
        ### riga di stato "HTTP/1.1 200 OK"
        ### header
        ### riga vuota
        ### body

        ### nell'header inserire Content-Type, Content-Length, Host (nome del server, non so se ce l'abbiamo)
        if request == 'get_object_list':
            message = "GET /objects HTTP/1.1\r\n"
            message = create_HTTP_request(request_line, "")
            
            s = server_connection(server_id, server_port)
            
            send(s, message)
            r = receive(s)
            print(r)
            s.close()

        elif request == 'get_object':
            file_name = input('which fil do you want to download? ')
            
            message = "GET /objects/{} HTTP/1.1\r\n".format(file_name)
            message = create_HTTP_request(request_line, "")

            s = server_connection(server_id, server_port)
            
            send(s, messaggio_finale)
            
            r = receive(s, binary_obj)
            if r.decode('utf-8') == "oggetto richiesto non trovato!":
                print(r)
            else:
                r = r.encode('utf-8')
                file = open(file_name, "wb")
                file.write(r)
                file.close()

            s.close()

        elif request == 'exit':
            loop = False
            #r = requests.get("{}/objects/exit".format(server_id))

    print("\n")
