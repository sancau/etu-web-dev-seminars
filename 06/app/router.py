import re

from . import views


ALLOWED_METHODS = [
    'GET', 'POST', 'PUT', 'DELETE',
]


def is_pk_url(url):
    regex = re.compile(r'/api/records/[0-9]+/?')
    return regex.match(url) is not None


def is_collection_url(url):
    return url in ['/api/records/', '/api/records']


def route(request):
    if request.method not in ALLOWED_METHODS:
        return views.invalid_method(request)

    if request.method == 'GET' and request.path == '/':
        return views.index(request)

    if request.method == 'GET' and '/static/' in request.path:
        return views.static(request)

    if is_collection_url(request.path):
        logic_map = {
          'GET': views.get_list,
          'POST': views.create_record,
        }
        resolver = logic_map.get(
            request.method,
            views.invalid_method,
        )
        return resolver(request)

    if is_pk_url(request.path):
        logic_map = {
          'GET': views.get_one,
          'PUT': views.update_one,
          'DELETE': views.delete_one,
        }
        resolver = logic_map.get(
            request.method,
            views.invalid_method,
        )
        return resolver(request)

    return views.resource_not_found(request)
