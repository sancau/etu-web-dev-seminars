from .http import Request, Response
from .record import Record
import json 


def index(r):
    print('index')
    return Response.build_text_file('index.html')


def static(r):
    file_name = r.path.split('/static/')[-1].split('/').pop(0)
    return Response.build_text_file(file_name)


def invalid_method(r):
    msg = {'error': f'{r.method} method is not allowed'}
    result = json.dumps(msg), 405
    return Response.build_json(*result)


def resource_not_found(r: Request):
    msg = {'error': 'Resource Not Found'}
    result = json.dumps(msg), 404
    return Response.build_json(*result)


def get_list(r: Request):
    search_terms = r.params.get('search') or []
    assert len(search_terms) < 2, 'Multiple param values for search' \
                                  ' are not supported'
    records = Record.get_list(search_terms=search_terms)
    result = json.dumps([r.as_dict() for r in records]), 200
    return Response.build_json(*result)


def get_one(request: Request):
    pk = int(request.path.split('/')[3])
    record = Record.get(pk=pk)
    if record:
        result = json.dumps(record.as_dict()), 200
    else:
        result = json.dumps({'error': 'Object Not Found'}), 404
    return Response.build_json(*result)


def create_record(request: Request):
    title = request.data['title']
    message = request.data['message']

    record = Record(title=title, message=message)
    r = record.save()
    result = json.dumps(r), 201

    return Response.build_json(*result)


def update_one(request: Request):
    title = request.data['title']
    message = request.data['message']

    pk = int(request.path.split('/')[2])

    record = Record.get(pk=pk)
    if record:
        record.title = title
        record.message = message
        r = record.save()
        result = json.dumps(r), 202
    else:
        result = json.dumps({'error': 'Object Not Found'}), 404
    return Response.build_json(*result)


def delete_one(request: Request):
    pk = int(request.path.split('/')[2])
    record = Record.get(pk=pk)
    if record:
        record.delete()
        result = json.dumps({'result': 'OK'}), 200
    else:
        result = json.dumps({'error': 'Object Not Found'}), 404
    return Response.build_json(*result)
