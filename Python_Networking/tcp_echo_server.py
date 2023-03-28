import my_socket

host = 'localhost'
port = 9999

listening_socket = my_socket.TCPListeningSocket(host, port)

listening_socket.start_listening()

connected_socket = listening_socket.accept_connection()

while True:
    data = connected_socket.receive_chunk()
    connected_socket.send_chunk(data)

