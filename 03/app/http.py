from .config import ENCODING


class Request:
    """Parses HTTP request to an object with method and path props."""
    def __init__(self, data: bytes):
        self.raw = data
        self.string = self.raw.decode(ENCODING)
        lines = self.string.split('\n')
        self.method, self.path, _ = lines[0].split(' ')


class Response:
    """Builds a toy HTTP reponse given a body and status."""
    @staticmethod
    def build(body: str, status: int):
        body = body.strip()
        response = f'HTTP/1.1 200\n'  # protocol and status
        response += 'Content-Type: text/html; charset=utf-8\n'
        response += '\n'
        response += body
        return response.encode(ENCODING)  # return bytes stream
