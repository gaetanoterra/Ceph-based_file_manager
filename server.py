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


def get_prova():
    message = "GET /objects/prova HTTP/1.1\r\n"
    contentType = "Content-Type: application/x-www-form-urlencoded\r\n"
    body = "body di prova"
    messaggio_finale = message + contentType + body
    send(client_socket, messaggio_finale)    
    
def client_receive(client_socket):
    return client_socket.recv(4096).decode('utf-8')

def client_send(client_socket, m):
    #client_socket.send(str(sys.getsizeof(m)).encode('utf-8'))
    client_socket.send(m.encode('utf-8'))

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("",8080))
    print("Server in ascolto")

    while True:
        s.listen()
        clientSocket, clientAddress = s.accept()

        request = receive(clientSocket).split(" ")
        print("request: {}".format(request[0]))
        if (request[0] ==  "GET") & (request[1] == "/objects/prova"):
            print("sono in provaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n")
            get_prova(clientSocket)
        else:
            print("comando errato")
            break
