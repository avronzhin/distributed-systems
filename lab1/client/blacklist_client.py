import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8071")

print(server.black_list_check_by_fullname(u'Петров', u'Петр', u'Петрович', "07.08.1985"))
print(server.black_list_check_by_fullname(u'Петров', u'Петр', u'Иванович', "07.08.1985"))
print(server.black_list_check_by_fullname(u'Петров', u'Петр', u'Петрович', "15.04.1985"))
print(server.black_list_check_by_fullname(u'Петров', u'Петр', u'Петрович', "01.01.2001"))
