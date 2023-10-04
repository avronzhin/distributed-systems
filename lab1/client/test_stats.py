import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8072")

logs = server.get_by_event('creating event')
print(logs)

server.log('creating event')
server.log('creating event2')
server.log('creating event3')