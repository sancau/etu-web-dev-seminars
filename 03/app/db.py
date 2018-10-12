import sqlite3


class DB:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(self.path, isolation_level=None)  # autocommit
        self.cursor = self.connection.cursor()
        self.init()

    def init(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """)

    def sql(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return [
            {col[0]: x for col, x in zip(self.cursor.description, row)}
            for row in self.cursor.fetchall()
        ]

