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
    
def receive(s, b):
    #dim_received = int(s.recv(4096)) #ricevo la dimensione del messaggio
    if b == True:
        data_received = s.recv(4096)
    else:
        data_received = s.recv(4096).decode('utf-8') #ricevo il messaggio
    
    return data_received

def send(s, m, b):
    #s.send(str(sys.getsizeof(m)).encode('utf-8')) #invio la dimensione della risposta al server
    if b == True:
        s.send(m)
    else:
        s.send(m.encode('utf-8')) #invio la risposta al server


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("",8080))
    binary_obj = False
    print("Server in ascolto")

################### TO DO : creare una classe per la costruzione dell'header e del messaggio completo
    while True:
        s.listen()
        clientSocket, clientAddress = s.accept()
        
        cluster = rados.Rados(conffile='ceph.conf')
        cluster.connect()
        pool = create_pool_if_non_existent(cluster, "exam_data")

        binary_obj = False #voglio ricevere una stringa => decodifico dal binary
        request = receive(client_socket, binary_obj).split(" ")
        print("request: {}".format(request[0]))
        if (request[0] ==  "GET") & (request[1] == "/objects"):
            print("sono in get_object_list")
            get_object_list(cluster, pool)
            print("obj: {}".format(message))
            
            binary_obj = False #invio la lista come stringa
            send(client_socket, message, binary_obj)
        
        elif (request[0] ==  "GET") & ("/objects/" in request[1]):
            file_to_download = request[1].split('/')[2]
            
            print("file_to_download: {}".format(file_to_download))
            message = get_object(cluster, pool, file_to_download)
            if message is False:
                binary_obj = False
                message = "oggetto richiesto non trovato!"
            else:
                binary_obj = True #invio l'oggetto come insieme di byte

            send(client_socket, message, binary_obj)
        
        else:
            print("comando errato")
            break
