from .config import ENCODING

from . import views


def route(request):
    if not request.method == 'GET':
        return views.invalid_method(request)
    elif request.path in ['/python', '/python/']:
        return views.render_python()
    elif request.path in ['/records', '/records/']:
        return views.show_records(request)
    else:
        return views.generic_page(request)
