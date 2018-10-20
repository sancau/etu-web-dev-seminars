import socket
import sys
import time
from datetime import datetime

from .router import route
from .http import Request, Response


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


def log(started_at: datetime, req: Request, res: Response):
    now = datetime.now()
    delta = (now - started_at).microseconds / 1000  # convert to milliseconds
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S')
    print(
        f'{now_formatted} '
        f'{req.method} {req.path} received {len(req.data)} bytes => '
        f'{len(res.encoded_data)} bytes of {res.content_type} | ' 
        f'Status: {res.status} | {delta} ms'
    )


def serve(host, port, max_connections):
    # server socket creation and configuration
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    # use SO_REUSEADDR for Linux and Windows
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_socket.bind((host, port))
    server_socket.listen(max_connections)
    print(f'Listening on {host}:{port}.')

    # the main loop
    while True:
        client_socket, _ = server_socket.accept()
        data = read_all_data(client_socket)
        if data:
            started_at = datetime.now()
            request = Request(data)
            response = route(request)
            client_socket.send(response.encoded_data)
        client_socket.close()
        log(started_at, request, response)
