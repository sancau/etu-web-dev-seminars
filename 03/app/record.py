from .config import db


class Record:
    def __init__(self, *, title, message, id=None):
        self.id = id
        self.title = title
        self.message = message

    def save(self):
        db.sql("""
        INSERT INTO records (title, message) VALUES (:title, :message);
        """, {'title': self.title, 'message': self.message})

    def delete(self):
        if self.id:
           db.sql("""
           DELETE FROM records WHERE id = :id
           """, {'id': self.id}) 

    @classmethod
    def get(cls, pk):
        data = db.sql("""
        SELECT * FROM records WHERE id = :id
        """, {'id': pk})
        if len(data) == 1:
            return cls(**data[0])

    @classmethod
    def get_list(cls, **args):
        return db.sql("""
        SELECT * FROM records;
        """)

    def __repr__(self):
        return f'Record ({self.id or "unsaved"}): {self.title}'

    def __str__(self):
        return self.__repr__()
