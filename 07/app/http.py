import json
import os

from .config import ENCODING, STATIC_DIR


def parse_params(s):
    """Simple (and naive) implementation of a query string params parser"""
    params = {}
    assert s.count('&') + 1 == s.count('='), 'Invalid params string'
    for pair in s.split('&'):
        key, value = pair.split('=')
        if key in params:
            params[key] = params[key] + [value]
        else:
            params[key] = [value]
    return params


class Request:
    """Parses HTTP request to an object with method and path props."""
    def __init__(self, data: bytes):
        self.raw = data
        self.string = self.raw.decode(ENCODING)

        lines = self.string.split('\n')
        self.method, path_and_params, _ = lines[0].split(' ')

        split = path_and_params.split('?')
        if len(split) > 1:
            assert len(split) == 2, 'Invalid URL.'
            self.params = parse_params(split[1])
        else:
            self.params = {}

        self.path = split[0]
        self.data = lines[-1]
        if self.data:
            self.data = json.loads(self.data)


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
        response += f'Content-Type: {content_type}; charset=utf-8\n'
        response += '\n'
        response += body
        return cls(
            response,
            status,
            content_type,
            response.encode(ENCODING),
        )

    @classmethod
    def build_json(cls, body: str, status: int): 
        return cls._build(body, status, content_type='application/json')

    @classmethod
    def build_text_file(cls, file_name):
        extension = None
        name, *other = os.path.splitext(file_name)
        if other:
            extension = other[-1]

        status = 200

        path = os.path.join(STATIC_DIR, file_name)
        data = '<h1>File Not Found (404)</h1>'
        content_type = 'text/html'

        try:
            with open(path, 'r', encoding='UTF-8') as f:
                data = f.read()
        except FileNotFoundError:
            status = 404

        if status == 200:
            content_types = {
                '.css': 'text/css',
                '.html': 'text/html',
                '.js': 'application/javascript',
            }
            try:
                content_type = content_types[extension]
            except KeyError:
                return cls._build(
                    f'<h1>File type is not supported</h1>',
                    500,
                    'text/html',
                )

        return cls._build(data, status, content_type)
