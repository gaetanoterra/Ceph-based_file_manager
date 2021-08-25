import rados
from flask import Flask
from flask import request

app = Flask(__name__)

def create_pool_if_non_existent(cluster, pool):
    if cluster.pool_exists(pool) is False:
        cluster.create_pool(pool)

    return pool

def handle_request(func, *args):

    cluster = rados.Rados(conffile='ceph.conf')
    cluster.connect()
    pool = create_pool_if_non_existent(cluster, "exam_data")
    result = func(*args, cluster, pool)
    cluster.shutdown()
    return result

@app.route('/list', methods=['GET'])
def get_object_list():  # noqa: E501
    return handle_request(get_object_list)

def get_object_list(cluster, pool):
    obj_string = ""
    try:
        ioctx = cluster.open_ioctx(pool)
        objects = list(ioctx.list_objects())
        obj_string = "lista oggetti server 1:\n"
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

@app.route('/object/<path:file_name>', methods=['GET'])
def get_object(file_name):  # noqa: E501
    return handle_request(get_object, file_name)

def get_object(file_name, cluster, pool):
    try:
        ioctx = cluster.open_ioctx(pool)
        file_content = ioctx.read(file_name, int(10e8))
    except Exception as e:
        print("error: {}".format(e))
        print("failed to get object " + file_name)
        return "file not found"
    finally:
        ioctx.close()
        
    return file_content

@app.route('/object', methods=['POST'])
def add_object():  # noqa: E501
    file = request.files['file_body']
    file_name = file.filename
    file_body = file.read()

    return handle_request(add_object, file_name, file_body)

def add_object(file, body, cluster, pool):
    try:
        ioctx = cluster.open_ioctx(pool)
        ioctx.write_full(file, body)
        print("{} was successfully added.".format(file))
        response = "file successfully added\n"
    except Exception as e:
        print(e)
        print("Unable to add the object to: " + pool)
        response = "error adding the new file\n"
    ioctx.close()

    return response

@app.route('/object/<path:file_name>', methods=['DELETE'])
def delete_object(file_name):  # noqa: E501
    return handle_request(delete_object, file_name)

def delete_object(file_name, cluster, pool):
    try:
        ioctx = cluster.open_ioctx(pool)
        ioctx.remove_object(file_name)
        print("{} was successfully deleted.".format(file_name))
        response = "file successfully deleted\n"
    except Exception as e:
        print(e)
        print("Unable to add the object to: " + pool)
        response = "error deleting the file\n"
    ioctx.close()

    return response

@app.route('/status', methods=['GET'])
def get_cluster_state():  # noqa: E501
    return handle_request(get_cluster_state)

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

if __name__ == '__main__':
    print("server in ascolto")
    app.run(host='0.0.0.0', port=8080)
