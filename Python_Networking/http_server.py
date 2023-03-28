#! /usr/bin/env python3

import socket

listening_socket = socket.socket()

listening_socket.bind(('localhost', 8989))

listening_socket.listen(1)

try:
    while True:
        connected_socket, address = listening_socket.accept()
        recevied_data = connected_socket.recv(4096).decode()
        parsed_raw = recevied_data.split("\r\n")
        request_line = parsed_raw[0]
        headerlines = []
        for i in parsed_raw[1: ]:
            if len(i) != 0:
                headerlines.append(i)
            else:
                break

        body = "\r\n".join(parsed_raw[len(headerlines)+2:]).encode()

        response_status_line = "HTTP/1.1 200 OK\r\n"
        response_header_1 = "Server: Custom Python Server\r\n"
        blank_line = "\r\n"

        print(request_line)


        if 'img' in request_line:
            response_header_2 = "Content-Type: image/png\r\n"
            body = open("./Dude.png", "r+b").read()
        else:
            response_header_2 = "Content-Type: text\r\n"
            body = (request_line + "\n" + '\n'.join(headerlines)).encode()

        response_header_3 = f"Content-Length: {len(body)}\r\n"

        response = response_status_line + response_header_1 + response_header_2 \
            + response_header_3 \
            + blank_line

        print(response)

        connected_socket.send(response.encode() + body)

        connected_socket.close()

except Exception:
    listening_socket.close()




