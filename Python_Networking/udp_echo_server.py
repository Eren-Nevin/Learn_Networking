import my_socket

host = 'localhost'
port = 9999

socket = my_socket.UDPSocket(host, port)

while True:
    (byte_data, client_send_address) = socket.receive_chunk_with_address()
    socket.connect(client_send_address[0], client_send_address[1])
    socket.send_chunk(byte_data)

