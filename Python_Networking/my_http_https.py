from http.server import *
import http.client
import socket
import ssl
import sys


class NoResponseRequestHandler(BaseHTTPRequestHandler):

    def print_and_respond_ok(self):
        print(self.headers.as_string())
        request_data = self.rfile.read(int(self.headers.get('content-length'))).decode()
        print(request_data)
        self.send_response(http.HTTPStatus.OK)
        self.end_headers()

    def do_POST(self):
        self.print_and_respond_ok()

    def do_GET(self):
        self.print_and_respond_ok()


    def do_HEAD(self):
        self.print_and_respond_ok()


    def do_PUT(self):
        self.print_and_respond_ok()



class MyHTTPServer:

    def __init__(self, host, port, http_request_handler_class=NoResponseRequestHandler):
        self.server_address = (host, port)
        self.server = HTTPServer(self.server_address, http_request_handler_class)

    def start_listening(self):
        self.server.serve_forever()


class MyHTTPSServer:

    def __init__(self, host, port, cert_file_path, key_file_path):
        self.https_server = MyHTTPServer(host, port)
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile=cert_file_path, keyfile=key_file_path)
        self.https_server.server.socket = \
            self.ssl_context.wrap_socket(self.https_server.server.socket,server_side=True)

    def start_listening(self):
        self.https_server.start_listening()
