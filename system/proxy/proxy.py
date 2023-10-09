import xmlrpc.client
import xmlrpc.server
from datetime import datetime


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8073), requestHandler=RequestHandler)
origin_server = xmlrpc.client.ServerProxy("http://localhost:8071")
stats_server = xmlrpc.client.ServerProxy("http://localhost:8072")


def proxy(action, action_type, args):
    start = datetime.now()
    result = action(*args)
    duration = datetime.now() - start
    stats_server.log(action_type, start.strftime("%Y-%m-%d %H:%M:%S"), str(duration.seconds))
    return result


def black_list_check(*args):
    return proxy(origin_server.black_list_check, "black_list_check", args)


def black_list_check_by_fullname_and_birth(*args):
    return proxy(origin_server.black_list_check_by_fullname_and_birth, "black_list_check_by_fullname_and_birth", args)


def send_back_binary(*args):
    return proxy(origin_server.send_back_binary, "send_back_binary", args)


def send_back_inversion(*args):
    return proxy(origin_server.send_back_inversion, "send_back_inversion", args)


def image_binarization_by_limit(*args):
    return proxy(origin_server.image_binarization_by_limit, "image_binarization_by_limit", args)


def rotate_image(*args):
    return proxy(origin_server.rotate_image, "rotate_image", args)


server.register_function(black_list_check, 'black_list_check')
server.register_function(black_list_check_by_fullname_and_birth, 'black_list_check_by_fullname_and_birth')
server.register_function(send_back_binary, 'send_back_binary')
server.register_function(send_back_inversion, 'send_back_inversion')
server.register_function(image_binarization_by_limit, 'image_binarization_by_limit')
server.register_function(rotate_image, 'rotate_image')

print("Proxy server starting. Listening on port 8073...")
server.serve_forever()
print("Disconnected")
