import time

server_list = ["252.3.233.130", "252.3.234.156", "252.3.235.77"]

def select_server():
    timestamp = time.time()
    server_id = server_list[hash(timestamp) % len(server_list)]
    print(hash(timestamp))
    return server_id
