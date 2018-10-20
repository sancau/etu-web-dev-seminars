from .http import Request, Response
from .record import Record
import json 

def invalid_method(r):
    msg = {'error': f'{r.method} method is not allowed'}
    result = json.dumps(msg), 405
    return Response.build_json(*result)


def resource_not_found(r: Request):
    msg = {'error': 'Resource Not Found'}
    result = json.dumps(msg), 404
    return Response.build_json(*result)


def get_list(request: Request):
    records = Record.get_list()
    result = json.dumps([r.as_dict() for r in records]), 200
    return Response.build_json(*result)


def get_one(request: Request):
    pk = int(request.path.split('/')[2])
    record = Record.get(pk=pk)
    if record:
        result = json.dumps(record.as_dict()), 200
    else:
        result = json.dumps({'error': 'Object Not Found'}), 404
    return Response.build_json(*result)
