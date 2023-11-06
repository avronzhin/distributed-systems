import xmlrpc.client

stats_server: xmlrpc.client.ServerProxy


def init():
    global stats_server
    try:
        print("Connecting to stats server...")
        stats_server = xmlrpc.client.ServerProxy("http://localhost:8072")
        print("Success connected")
    except():
        print("Connection is fail")
        stats_server = None


def stats_server_is_available():
    return stats_server is not None


def get_operation_types():
    result = stats_server.get_operation_types()
    result = list(map(lambda it: {"id": it[0], "title": it[1]}, result))
    return result


def get_logs_in_period_group_by_operation_type(start_date, end_date):
    rows = stats_server.get_in_period(start_date, end_date)
    result = list(map(lambda row: {"operation_type_id": row[1], "created": row[2], "duration": row[3]}, rows))
    return result
