from old_version.my_tcp import *
from old_version.my_udp import *
from old_version.my_ssl import *
import requests
import sys

host = 'localhost'
cert_file_path = f'{sys.path[0]}/my_network/configs/localhost/localhost.pem'
key_file_path = f'{sys.path[0]}/my_network/configs/localhost/localhost.key'


# TODO: Fix SSL Client


def setup_client(protocol, port):
    if protocol == 'udp':
        client = MyUDPClient(host, port)
    elif protocol == 'tcp':
        client = MyTCPClient(host, port)
    elif protocol == 'ssl':
        client = MySSLClient(host, port, False)
    else:
        client = None
    return client


def send_message(protocol, port, message):
    if protocol in ['udp', 'tcp', 'ssl']:
        client = setup_client(protocol, int(port))
        client.connect()
        client.send_chunk_string(message)

    else:
        requests.get(f'{protocol}://localhost:{port}', data=message.encode(), verify=False)


send_message(sys.argv[1], sys.argv[2], sys.argv[3])
