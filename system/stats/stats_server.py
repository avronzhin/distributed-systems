import sqlite3
import xmlrpc.server


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8072), requestHandler=RequestHandler)
db_name = 'log.db'


def execute_query_and_get_rows(sql, args):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def execute_query_and_get_cursor_last_row_id(sql, args):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    cursor.fetchone()
    last_row_id = cursor.lastrowid
    cursor.close()
    conn.commit()
    conn.close()
    return last_row_id


def get_operation_type_id_by_title(title):
    sql = "SELECT id FROM operation_types WHERE title = ?"
    rows = execute_query_and_get_rows(sql, (title,))
    if len(rows) == 1:
        return rows[0][0]
    else:
        return None


def create_operation_type(operation_type_title):
    sql = "INSERT INTO operation_types VALUES (NULL, ?)"
    return execute_query_and_get_cursor_last_row_id(sql, (operation_type_title,))


def get_or_create_operation_type_id(operation_type_title):
    operation_type_id = get_operation_type_id_by_title(operation_type_title)
    if operation_type_id is None:
        operation_type_id = create_operation_type(operation_type_title)
    return operation_type_id


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
    return execute_query_and_get_rows(sql, (operation_type_id,))


def get_in_period(start_date, end_date):
    sql = "SELECT * FROM logs WHERE created >= ? AND created <= ?"
    return execute_query_and_get_rows(sql, (start_date, end_date))


def get_by_duration(min_duration, max_duration):
    sql = "SELECT * FROM logs WHERE duration >= ? AND duration <= ?"
    return execute_query_and_get_rows(sql, (min_duration, max_duration))


def get_operation_types():
    sql = "SELECT * FROM operation_types"
    return execute_query_and_get_rows(sql, ())


def get_count_in_period_group_by_operation_type(start_date, end_date):
    sql = '''
        SELECT operation_type_id, count(*) AS 'count' 
            FROM logs 
            WHERE created >= ? AND created <= ? 
            GROUP BY operation_type_id
        '''
    return execute_query_and_get_rows(sql, (start_date, end_date))


def get_count_in_period_by_operation_type(start_date, end_date, operation_type):
    operation_type_id = get_operation_type_id_by_title(operation_type)
    sql = '''
            SELECT count(*) AS 'count' 
                FROM logs 
                WHERE operation_type_id = ? AND created >= ? AND created <= ?
            '''
    return execute_query_and_get_rows(sql, (operation_type_id, start_date, end_date))[0]


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
server.register_function(get_by_operation_type, 'get_by_operation_type')
server.register_function(get_in_period, 'get_in_period')
server.register_function(get_by_duration, 'get_by_duration')
server.register_function(get_operation_types, 'get_operation_types')
server.register_function(get_count_in_period_group_by_operation_type, 'get_count_in_period_group_by_operation_type')
server.register_function(get_count_in_period_by_operation_type, "get_count_in_period_by_operation_type")

print("Stats server starting. Listening on port 8072...")
server.serve_forever()
