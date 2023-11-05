import sqlite3
import xmlrpc.server


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8072), requestHandler=RequestHandler)
db_name = 'log.db'


def log(action_type, start, duration):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs VALUES (NULL, ?, ?, ?)", (str(action_type), start, duration))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def execute_query(sql, args):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_by_event(event):
    sql = "SELECT * FROM logs WHERE action_type = ?"
    return execute_query(sql, (event,))


def get_in_period(start_date, end_date):
    sql = "SELECT * FROM logs WHERE created >= ? AND created <= ?"
    return execute_query(sql, (start_date, end_date))


def get_by_duration(min_duration, max_duration):
    sql = "SELECT * FROM logs WHERE duration >= ? AND duration <= ?"
    return execute_query(sql, (min_duration, max_duration))


def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            action_type TEXT NOT NULL,
            created TEXT NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# UNIX time
#
create_table()
server.register_function(log, 'log')
server.register_function(get_by_event, 'get_by_event')
server.register_function(get_in_period, 'get_in_period')
server.register_function(get_by_duration, 'get_by_duration')
print("Stats server starting. Listening on port 8072...")
server.serve_forever()

