import my_socket

host = 'localhost'
port = 9999

propose_socket = my_socket.TCPProposeSocket(host, port)

connected_socket = propose_socket.connect()

while True:
    query = input()
    connected_socket.send_chunk_string(query)
    response = connected_socket.receive_chunk_string()
    print(response)