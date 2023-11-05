import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8072")


logs = server.get_in_period(1699199985, 1699499448)
print(logs)

logs = server.get_by_duration(2000, 3000)
print(logs)