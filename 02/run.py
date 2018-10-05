from app import server
from app.config import HOST, PORT, MAX_CONNECTIONS


if __name__ == '__main__':
    server.serve(HOST, PORT, MAX_CONNECTIONS)
