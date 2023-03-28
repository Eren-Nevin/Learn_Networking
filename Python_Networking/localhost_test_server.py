from old_version.my_udp import *
from old_version.my_tcp import *
from old_version.my_ssl import *
from my_http_https import *


import sys


host = 'localhost'
cert_file_path = f'{sys.path[0]}/configs/localhost/localhost.pem'
key_file_path = f'{sys.path[0]}/configs/localhost/localhost.key'

def start_server(protocol, port):

    if protocol == 'udp':
        server = MyUDPServer(host, port)
    elif protocol == 'tcp':
        server = MyTCPServer(host, port)
    elif protocol == 'ssl':
        server = MySSLServer(host, port, cert_file_path, key_file_path)
    elif protocol == 'http':
        server = MyHTTPServer(host, port)
    elif protocol == 'https':
        server = MyHTTPSServer(host, port, cert_file_path, key_file_path)

    server.start_listening()


start_server(sys.argv[1], int(sys.argv[2]))

