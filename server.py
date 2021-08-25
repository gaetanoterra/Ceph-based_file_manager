import rados
import socket
import sys
import subprocess

class HandleServer:
    def __init__(self):
        self.handle_request(self.create_pool_if_non_existent)

    def handle_request(self, func, *args):
        self.cluster = rados.Rados(conffile='ceph.conf')
        self.cluster.connect()
        func(*args)
        self.cluster.shutdown()

    def get_object_list(self):
        try:
            ioctx = self.cluster.open_ioctx(self.pool)
            objects = list(ioctx.list_objects())
            [print(obj) for obj in objects]
            ioctx.close()
        except Exception as e:
            print("Unable to get the object list from: " + self.pool)

    def add_object(self, file):
        ioctx = self.cluster.open_ioctx(self.pool)
        with open(file) as f:
            file_content_in_binary = str.encode(f.read())
        try:
            ioctx.write_full(file, file_content_in_binary)
            print("{} was successfully added.".format(file))
        except Exception as e:
            print(e)
            print("Unable to add the object to: " + self.pool)
        ioctx.close()

    def delete_object(self, file):
        ioctx = self.cluster.open_ioctx(self.pool)
        ioctx.remove_object(file)
        print("{} was successfully deleted.".format(file))
        ioctx.close()

    def get_object(self, file):
        ioctx = self.cluster.open_ioctx(self.pool)
        file_content = ioctx.read(file, length = int(10e12)).decode("utf-8")
        print(file_content)
        ioctx.close()

    def create_pool_if_non_existent(self, pool="exam_data"):
        if self.cluster.pool_exists(pool) is False:
            self.cluster.create_pool(pool)
        self.pool = pool

    def get_cluster_state(self):
        io_context = self.cluster.open_ioctx(self.pool)
        status = io_context.get_stats()
        print("Clusters Status: \n")
        for key, value in status.items():
            print("{}: {} \n".format(key, value))

    def exit(self):
        pass

def create_pool_if_non_existent(cluster, pool):
    if cluster.pool_exists(pool) is False:
        cluster.create_pool(pool)

    return pool

def get_object_list(cluster, pool):
    obj_string = ""
    try:
        ioctx = cluster.open_ioctx(pool)
        objects = list(ioctx.list_objects())
        for obj in objects:
            obj_string += "{}\n".format(obj.key)
    except Exception as e:
        print("error: {}".format(e))
        print("unable to get object list from pool " + pool)
        return "unable to get object list"
    finally:
        if not obj_string:
            obj_string = "unable to get object list from pool " + pool
        ioctx.close()
        
    return obj_string
  
def get_object(cluster, pool, file):
    try:
        ioctx = cluster.open_ioctx(pool)
        file_content = ioctx.read(file)
    except Exception as e:
        print("error: {}".format(e))
        print("failed to get object " + file)
        return  False
    finally:
        ioctx.close()

    return file_content

def add_object(file, body, cluster, pool):
    try:
        ioctx = cluster.open_ioctx(pool)
        ioctx.write_full(file, body.encode('utf-8'))
        print("{} was successfully added.".format(file))
        response = "file successfully added\n"
    except Exception as e:
        print(e)
        print("Unable to add the object to: " + pool)
        response = "error adding the new file\n"
    ioctx.close()

    return response

def delete_object(filename, cluster, pool):
    try:
        ioctx = cluster.open_ioctx(pool)
        ioctx.remove_object(filename)
        print("{} was successfully deleted.".format(filename))
        response = "file successfully deleted\n"
    except Exception as e:
        print(e)
        print("Unable to add the object to: " + pool)
        response = "error deleting the file\n"
    ioctx.close()

    return response

def get_cluster_state(cluster, pool):
    response = ""
    try:
        ioctx = cluster.open_ioctx(pool)
        status = ioctx.get_stats()
        for key, value in status.items():
            response = response + str(key) + ":" + str(value) + "\n"
    except Exception as e:
        print(e)
        print("Unable to get the status")
        response = "Unable to get the status"
    ioctx.close()

    return response

    
### io ricevo il messaggio come request line, header (ultime elemento è content-length), riga vuota, body
def receive(s):
    #dim_received = int(s.recv(4096)) #ricevo la dimensione del messaggio
    data_received = s.recv(1024)
    print("data_received: {}".format(data_received))

    header = data_received.decode('utf-8')

    header = data_received.split("\n\n")[0] # selezione l'header
    l = header.split("Content-Length:")     # seleziono tutti i campi dell'header per prendere l'ultimo che corrisponde a Content-Length
    dim = l[1]
    l = int(dim.split("\r\n")[0])             # qui prendo la dimensione del body
    #missing_len = l - (1024 - len(header[0].encode('utf-8')))  # io potrei aver ricevuto parte del body di dimensio$
    missing_len = l
    body = header[1].encode('utf-8')
    print("missing_len: {}".format(missing_len))

    #potrebbe andare bene anche:                #aggiuntooggi
    #if missing_len > 0:
        #missing_data_received = s.recv(missing_len)
        #body = body + missing_data_received
    
    while missing_len > 0:
        d = 1024
        if missing_len < d:
            d = missing_len
        missing_data_received = s.recv(d)
        body = body + missing_data_received

        missing_len = missing_len -  d


    print("header: {}".format(header))
    print("l: {}".format(l))
    print("missing_len: {}".format(missing_len))
    print("body: {}".format(body))
    
    message = (header.encode('utf-8') + body.encode('utf-8'))
    return message

def send(s, m):
    dim = sys.getsizeof(m)              #aggiuntooggi
    i = 0
    while i < dim:
        if (dim - i) > 1024:
            splitted_message = m[i:i + 1023]
            i = i + 1023
            s.send(splitted_message.encode('utf-8')) #invio la risposta al server
        else:
            splitted_message = m[i:dim]
            s.send(splitted_message.encode('utf-8')) #invio la risposta al server
    
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
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("",8080))
    print("Server in ascolto")

################### TO DO : creare una classe per la costruzione dell'header e del messaggio completo
    while True:
        s.listen()
        client_socket, client_address = s.accept()
        
        cluster = rados.Rados(conffile='ceph.conf')
        cluster.connect()
        pool = create_pool_if_non_existent(cluster, "exam_data")

        request = receive(client_socket).decode('utf-8')
        splitted_request  = request.split(" ")
        
        if (request[0] ==  "GET") & (request[1] == "/objects"):
            print("sono in get_object_list")
            body = get_object_list(cluster, pool)
            ### TODO: fare un if per lo status line
            status_line = ""
            
            message = create_HTTP_response(status_line, body)
            send(client_socket, message)
        
        elif (request[0] ==  "GET") & ("/objects/" in request[1]):
            file_to_download = request[1].split('/')[2]
            
            print("file_to_download: {}".format(file_to_download))
            body = get_object(cluster, pool, file_to_download)
            if message is False:
                body = "oggetto richiesto non trovato!"
                status_line = "HTTP/1.1 404 Not Found\r\n"
            else:
                body = body.decode('utf-8')
                status_line = "HTTP/1.1 200 OK\r\n"

            message = create_HTTP_response(status_line, body)       #aggiuntooggi
            send(client_socket, message)
        
        elif (splitted_request[0] ==  "POST") & ("/objects/" in splitted_request[1]):
            file_to_upload = splitted_request[1].split('/')[2]

            print("file_to_upload: {}".format(file_to_upload))
            body = request.split("\n\n")[1]

            response = add_object(file_to_upload, body, cluster, pool)

            status_line = ""

            message = create_HTTP_response(status_line, response)
            send(client_socket, message)

        elif (splitted_request[0] ==  "DELETE") & ("/objects/" in splitted_request[1]):
            file_to_delete = splitted_request[1].split('/')[2]

            print("file_to_delete: {}".format(file_to_delete))

            response = delete_object(file_to_delete, cluster, pool)

            status_line = ""

            message = create_HTTP_response(status_line, response)
            send(client_socket, message)

        elif (splitted_request[0] ==  "GET") & ("/status" in splitted_request[1]):

            response = get_cluster_state(cluster, pool)

            status_line = ""

            message = create_HTTP_response(status_line, response)
            send(client_socket, message)

        
        else:
            print("comando errato")
            break
