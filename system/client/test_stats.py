import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8072")

logs = server.get_by_event('send_back_inversion')
print(logs)

logs = server.get_in_period('2023-10-04 22:42:28', '2023-10-10 23:20:25')
print(logs)

logs = server.get_by_duration(7, 8)
print(logs)