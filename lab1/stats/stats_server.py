import glob
import os
import xmlrpc.server
from datetime import datetime


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8072), requestHandler=RequestHandler)
max_size = 5


def try_fix_log():
    file = open('logs/log.csv', 'r')
    line_count = len(file.readlines())
    file.close()
    if line_count >= max_size:
        os.rename('logs/log.csv', 'logs/' + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")
        new_file = open('logs/log.csv', 'x')
        new_file.close()


def log(event):
    try_fix_log()
    file = open('logs/log.csv', 'a')
    file.write(str(event) + ',' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    file.close()
    return True


def open_files_in_directory(directory_path, event):
    result = []
    for path in glob.glob(os.path.join(directory_path, '*')):
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(event + ','):
                    result.append(line)
    return result


def get_by_event(event):
    return open_files_in_directory('logs', event)


server.register_function(log, 'log')
server.register_function(get_by_event, 'get_by_event')
print("Stats server starting. Listening on port 8072...")
server.serve_forever()
