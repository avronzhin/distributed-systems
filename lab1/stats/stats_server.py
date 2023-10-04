import glob
import os
import xmlrpc.server
from datetime import datetime

import pandas


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


def open_files_in_directory(directory_path):
    csv_files = glob.glob(directory_path + "/*.csv")
    all_rows = []
    for file in csv_files:
        df = pandas.read_csv(file, header=None)
        all_rows += df.itertuples(index=False, name=None)
    return all_rows


def get_by_event(event):
    all_rows = open_files_in_directory('logs')
    return list(filter(lambda row: row[0] == event, all_rows))


def get_in_period(start, end):
    all_rows = open_files_in_directory('logs')
    return list(filter(lambda row: end >= row[1] >= start, all_rows))



server.register_function(log, 'log')
server.register_function(get_by_event, 'get_by_event')
server.register_function(get_in_period, 'get_in_period')
print("Stats server starting. Listening on port 8072...")
server.serve_forever()
