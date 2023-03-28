import my_socket

host = 'localhost'
port = 9999

listening_socket = my_socket.SSLListeningSocket(
    host, port, 'configs/localhost/localhost.pem', 'configs/localhost/localhost.key')

listening_socket.start_listening()

connected_socket = listening_socket.accept_connection()

while True:
    data = connected_socket.receive_chunk()
    connected_socket.send_chunk(data)