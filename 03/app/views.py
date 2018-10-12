from .record import Record


def invalid_method(r):
    return f'<h1>{r.method} method is not allowed.</h1>', 405


def generic_page(r):
    return f'<h1>You requested {r.path} page</h1>', 200


def show_records(r):
    records = Record.get_list()
    out = '<hr />'
    out += '<ol>'
    for r in records:
        out += f'<li>Title: {r["title"]} | Message: {r["message"]}</li>'
    out += '</ol>'
    return out, 200


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
    """, 200
