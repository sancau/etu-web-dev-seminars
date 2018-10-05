from .db import DB


PORT = 5000
HOST = '0.0.0.0'
MAX_CONNECTIONS = 0
ENCODING = 'UTF-8'


DB_PATH = './records.db'


db = DB(path=DB_PATH)
