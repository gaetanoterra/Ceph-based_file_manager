import requests

def menu():
    #funzione che mostra il menu
    print("**********************MENU*******************\n"
          "Operazioni disponibili:\n"
          "get_object_list\n"
          "add_object\n"
          "get_object\n"
          "delete_object\n"
          "get_status\n"
          "exit\n"
          "**********************************************\n")

if __name__ == '__main__':
    server_id = "http://252.3.233.130:8080" # ip del container con cui comunicare
    loop = True

    while loop:

        menu()
        request = input('what do you want to do? ')

        if request == 'get_object_list':

            response = requests.get("{}/list".format(server_id))
            print(response.text)

        elif request == 'get_object':
            file_name = input('which fil do you want to download? ')

            response = requests.get("{}/object/{}".format(server_id, file_name))
            
            if response.text == "file not found":
                print("file {} not found\n".format(file_name))
            else:
                file = open(file_name, "wb")
                file.write(response.content)
                file.close()

        elif request == 'add_object':
            file_name = input('which file do you want to upload? ')
            file = open(file_name, 'rb')
            body = {'file_body' : file}

            response = requests.post("{}/object".format(server_id), files = body)
            print(response.text)
            file.close()

        elif request == 'delete_object':
            file_name = input('which file do you want to delete? ')

            response = requests.delete("{}/object/{}".format(server_id, file_name))
            print(response.text)

        elif request == 'get_status':

            response = requests.get("{}/status".format(server_id))
            print("Clusters Status: {}\n".format(response.text))

        elif request == 'exit':
            loop = False
            #r = requests.get("{}/objects/exit".format(server_id))

    print("\n")

