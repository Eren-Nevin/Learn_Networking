import sys
import my_socket

host = 'localhost'
port = 51233

# server_host = sys.argv[1]
server_host = 'localhost'
server_port = int(sys.argv[1])

socket = my_socket.UDPSocket(host, port)

while True:
    query = input("Query>: ")
    socket.connect(server_host, server_port)
    socket.send_chunk_string(query)
    response = socket.receive_chunk_string()
    print(response)
