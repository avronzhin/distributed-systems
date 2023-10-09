import pickle
import xmlrpc.client
import xmlrpc.server

import pandas as pd


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8071), requestHandler=RequestHandler)


def black_list_check(surname):
    frame = pd.read_csv('bad_boys2.csv', header=0, sep=',', encoding='utf8')
    exist = any(frame['Surname'] == surname)
    if exist:
        return surname + ": " + "bad_boy"
    else:
        return surname + ": " + "good_boy"


def black_list_check_by_fullname_and_birth(surname, name, patronym, birth):
    frame = pd.read_csv('bad_boys2.csv', header=0, sep=',', encoding='utf8')
    if any((frame['Surname'] == surname) & (frame['Patronym'] == patronym) & (frame['Name'] == name) & (
            frame["Birth"] == birth)):
        return surname + " " + patronym + " " + name + " born " + birth + " is bad guy"
    else:
        return surname + " " + patronym + " " + name + " born " + birth + " not found"


def send_back_binary(bin_data):
    data = bin_data.data
    return xmlrpc.client.Binary(data)


def send_back_inversion(bin_image):
    img_arr = pickle.loads(bin_image.data)
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    if len(img_arr.shape) == 3:
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    img_arr[i][j][k] = 255 - img_arr[i][j][k]
    else:
        for i in range(height):
            for j in range(width):
                img_arr[i][j] = 255 - img_arr[i][j]

    pimg = pickle.dumps(img_arr)
    return xmlrpc.client.Binary(pimg)


def image_binarization_by_limit(bin_image, limit):
    img_arr = pickle.loads(bin_image.data)
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    if len(img_arr.shape) == 3:
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    img_arr[i][j][k] = 0 if img_arr[i][j][k] < limit else 255
    else:
        for i in range(height):
            for j in range(width):
                img_arr[i][j] = 0 if img_arr[i][j] < limit else 255

    pimg = pickle.dumps(img_arr)
    return xmlrpc.client.Binary(pimg)


def rotate_image(bin_image):
    img_arr = pickle.loads(bin_image.data)
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    if len(img_arr.shape) == 3:
        for i in range(height // 2):
            for j in range(width):
                for k in range(3):
                    temp = img_arr[i][j][k]
                    img_arr[i][j][k] = img_arr[height - i -1][j][k]
                    img_arr[height - i - 1][j][k] = temp
    else:
        for i in range(height // 2):
            for j in range(width):
                temp = img_arr[i][j]
                img_arr[i][j] = img_arr[height - i - 1][j]
                img_arr[height - i - 1][j] = temp

    pimg = pickle.dumps(img_arr)
    return xmlrpc.client.Binary(pimg)


server.register_function(black_list_check, 'black_list_check')
server.register_function(black_list_check_by_fullname_and_birth, 'black_list_check_by_fullname_and_birth')
server.register_function(send_back_binary, 'send_back_binary')
server.register_function(send_back_inversion, 'send_back_inversion')
server.register_function(image_binarization_by_limit, 'image_binarization_by_limit')
server.register_function(rotate_image, 'rotate_image')

print("Listening on port 8071...")
server.serve_forever()
print("Disconnected")
