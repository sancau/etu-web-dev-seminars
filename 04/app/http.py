from .config import ENCODING


class Request:
    """Parses HTTP request to an object with method and path props."""
    def __init__(self, data: bytes):
        self.raw = data
        self.string = self.raw.decode(ENCODING)
        lines = self.string.split('\n')
        self.method, self.path, _ = lines[0].split(' ')
        self.data = lines[-1]


class Response:
    """Builds a toy HTTP reponse given a body and status."""
    def __init__(self, data, status, content_type, encoded_data):
        self.data = data
        self.status = status
        self.content_type = content_type
        self.encoded_data = encoded_data

    @classmethod
    def _build(cls, body: str, status: int, content_type: str):
        body = body.strip()
        response = f'HTTP/1.1 {status}\n'
        response += 'Content-Type: {content_type}; charset=utf-8\n'
        response += '\n'
        response += body
        return cls(
            response,
            status,
            content_type,
            response.encode(ENCODING),
        )

    @classmethod
    def build_html(cls, body: str, status: int):
        return cls._build(body, status, content_type='text/html')

    @classmethod
    def build_json(cls, body: str, status: int): 
        return cls._build(body, status, content_type='application/json')
