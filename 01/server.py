# basic server that can handle HTTP GET requests in pure Python

import socket
import sys
import time


PORT = 5000
HOST = '0.0.0.0'
MAX_CONNECTIONS = 0
ENCODING = 'UTF-8'


def render_python():
    return """
    <div style="border: 10px solid #ae6f7a; margin: 50px; padding: 20px; border-radius: 50px;
                color: #ddd; background-color: #444; width: 500px; font-size: 150%;
                -webkit-box-shadow: 51px 32px 58px 8px rgba(41,37,41,1);
                -moz-box-shadow: 51px 32px 58px 8px rgba(41,37,41,1);
                box-shadow: 51px 32px 58px 8px rgba(41,37,41,1);">
        <h1>Pure</h1>
        <img src="https://www.python.org/static/img/python-logo@2x.png" />
        <h1>HTTP Server</h1>
    </div>
    """

class Request:
    def __init__(self, data: bytes):
        self.raw = data
        self.string = self.raw.decode(ENCODING)
        lines = self.string.split('\n')
        self.method, self.path, _ = lines[0].split(' ')


def read_all_data(client_socket: socket.socket) -> bytes:
    chunk_size = 4096  # bytes
    timeout = 0.25  # seconds
    delay = 0.1 # seconds
    data: bytes = b''

    client_socket.setblocking(False)

    until = time.time() + timeout
    while True:
        try:
            chunk: bytes = client_socket.recv(chunk_size)  # try get next chunk of data
            if chunk:
                data += chunk
                until = time.time() + timeout  # reset timer
        except BlockingIOError:  # no data yet
            if time.time() > until:  # timeout reached
                break
            time.sleep(delay)  # add some throttling
    return data


def build_response(request: Request) -> bytes:
    def _html_response(status, body: str):
        body = body.strip()
        response = f'HTTP/1.1 {status}\n'  # protocol and status
        response += 'Content-Type: text/html; charset=utf-8\n'
        response += '\n'
        response += body
        return response.encode(ENCODING)  # return bytes stream

    if not request.method == 'GET':
        return _html_response(status=405, body=f'<h1>{request.method} method is not allowed.')
    elif request.path in ['/python', '/python/']:
        return _html_response(status=200, body=render_python())
    else:
        return _html_response(status=200, body=f'<h1>You requested {request.path} page</h1>')


def main():
    # server socket creation and configuration
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f'Listening on {HOST}:{PORT}. Encoding: {ENCODING}.')

    # the main loop
    while True:
        client_socket, (client_ip, client_port) = server_socket.accept()
        data = read_all_data(client_socket)
        if data:
            request = Request(data)
            response = build_response(request)
            client_socket.send(response)
        client_socket.close()


if __name__ == '__main__':
    main()
