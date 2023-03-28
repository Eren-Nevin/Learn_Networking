import socket
import ssl

class SocketSendMixIn:

    def get_socket(self):
        return self.socket

    # When Using Chunk Methods, Make Sure Your Data Is Smaller Than Your Socket's Buffer Size
    def send_chunk(self, byte_data):
        self.socket.send(byte_data)

    def send_chunk_string(self, string_data: str):
        self.send_chunk(string_data.encode())

    def send_response(self, byte_data, end_of_data: str):
        response_data = byte_data + end_of_data.encode()
        self.socket.sendall(byte_data)

    def send_response_string(self, string_data: str, end_of_data: str):
        self.send_response(string_data.encode(), end_of_data)

    def send_file(self, file_path, offset, length, end_of_data:str):
        file = open(file_path, 'rb')
        self.socket.sendfile(file, offset, length)
        # TODO: Does sending end_of_data separately cause any problems?
        self.send_chunk_string(end_of_data)


class SocketReceiveMixIn:

    def get_socket(self):
        return self.socket

    # All Receive Methods Are Blocking

    def receive_chunk(self):
        return self.socket.recv(4096)

    def receive_chunk_with_address(self):
        return self.socket.recvfrom(4096)

    def receive_chunk_string(self):
        return self.receive_chunk().decode()

    def receive_response(self, end_of_data: str):
        response = b''
        while True:
            chunk = self.receive_chunk()
            decoded_chunk: str = chunk.decode()
            if chunk == b'' or decoded_chunk.endswith(end_of_data):
                real_chunk = decoded_chunk.split(end_of_data)[0].encode()
                response += real_chunk
                break
            else:
                response += chunk
        return response

    def receive_response_string(self, end_of_data: str):
        self.receive_response(end_of_data).decode()


class UDPSocket(SocketReceiveMixIn, SocketSendMixIn):

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (host, port)
        self.socket.bind(self.address)

    # Be Sure To Call Connect Before Using Any Of The Sending Methods
    def connect(self, endpoint_host, endpoint_port):
        self.endpoint_address = (endpoint_host, endpoint_port)
        self.socket.connect(self.endpoint_address)


class TCPListeningSocket:

    def __init__(self, host, port, listen_queue=5):
        self.socket = socket.socket()
        self.address = (host, port)
        self.listen_queue = listen_queue

    def start_listening(self):
        self.socket.bind(self.address)
        self.socket.listen(self.listen_queue)

    def accept_connection(self):
        (accepted_socket, endpoint_address) = self.socket.accept()
        return TCPConnectedSocket(accepted_socket, endpoint_address)


class TCPConnectedSocket(SocketSendMixIn, SocketReceiveMixIn):

    def __init__(self, accepted_socket: socket.socket, endpoint_address):
        self.socket = accepted_socket
        self.endpoint_address = endpoint_address


class TCPProposeSocket:

    def __init__(self, host, port):
        self.socket = socket.socket()
        self.endpoint_address = (host, port)

    def test_connection(self):
        return self.socket.connect_ex(self.endpoint_address)

    def connect(self):
        self.socket.connect(self.endpoint_address)
        return TCPConnectedSocket(self.socket, self.endpoint_address)


class SSLListeningSocket(TCPListeningSocket):

    def __init__(self, host, port, certfile_path, keyfile_path, listen_queue=5):
        super().__init__(host, port, listen_queue)
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
        self.socket = self.ssl_context.wrap_socket(self.socket, server_side=True)

    def accept_connection(self):
        (accepted_socket, endpoint_address) = self.socket.accept()
        return SSLConnectedSocket(accepted_socket, endpoint_address)


class SSLConnectedSocket(TCPConnectedSocket):
    pass


class SSLProposeSocket(TCPProposeSocket):

    def __init__(self, host, port, secure=True):
        super().__init__(host, port)
        self.ssl_context = ssl.create_default_context()
        if secure is False:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.ssl_context.verify_mode = ssl.CERT_NONE
            self.ssl_context.check_hostname = False
        self.socket = self.ssl_context.wrap_socket(self.socket, server_hostname=host)

    def connect(self):
        self.socket.connect(self.endpoint_address)
        return SSLConnectedSocket(self.socket, self.endpoint_address)


