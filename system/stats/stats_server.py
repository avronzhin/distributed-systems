import sqlite3
import xmlrpc.server


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8072), requestHandler=RequestHandler)
db_name = 'log.db'


def execute_query(sql, args):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_or_create_operation_type_id(operation_type_title):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operation_types WHERE title = ?", (operation_type_title,))
    row = cursor.fetchone()
    new_id = None
    if row is None:
        cursor.execute("INSERT INTO operation_types VALUES (NULL, ?)", (operation_type_title,))
        cursor.fetchone()
        new_id = cursor.lastrowid
    else:
        new_id = row[0]
    cursor.close()
    conn.commit()
    conn.close()
    return new_id


def create_log(operation_type_id, created, duration):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs VALUES (NULL, ?, ?, ?)", (operation_type_id, created, duration))
    cursor.close()
    conn.commit()
    conn.close()


def log(operation_type_title, created, duration):
    operation_type_id = get_or_create_operation_type_id(operation_type_title)
    create_log(operation_type_id, created, duration)
    return True


def get_by_operation_type(operation_type_id):
    sql = "SELECT * FROM logs WHERE operation_type_id = ?"
    return execute_query(sql, (operation_type_id,))


def get_in_period(start_date, end_date):
    sql = "SELECT * FROM logs WHERE created >= ? AND created <= ?"
    return execute_query(sql, (start_date, end_date))


def get_by_duration(min_duration, max_duration):
    sql = "SELECT * FROM logs WHERE duration >= ? AND duration <= ?"
    return execute_query(sql, (min_duration, max_duration))


def get_operation_types():
    sql = "SELECT * FROM operation_types"
    return execute_query(sql, ())


def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_types (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL UNIQUE
        )    
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            operation_type_id INTEGER NOT NULL,
            created INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            
            CONSTRAINT fk_operation_type
                FOREIGN KEY (operation_type_id) REFERENCES operation_types (id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


create_table()

server.register_function(log, 'log')
server.register_function(get_operation_types, 'get_operation_types')
server.register_function(get_by_operation_type, 'get_by_operation_type')
server.register_function(get_in_period, 'get_in_period')
server.register_function(get_by_duration, 'get_by_duration')

print("Stats server starting. Listening on port 8072...")
server.serve_forever()

