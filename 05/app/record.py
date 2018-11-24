from .config import db


class Record:
    def __init__(self, *, title, message, id=None):
        self.id = id
        self.title = title
        self.message = message

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message
        }

    def save(self):
        if self.id:
            print(self.id, self.title, self.message)
            db.sql("""
                UPDATE records
                SET title = :title,
                message = :message
                WHERE id = :id""", {
                    'title': self.title,
                    'message': self.message,
                    'id': self.id,
                })
        else:
            db.sql("""
            INSERT INTO records (title, message) VALUES (:title, :message);
            """, {'title': self.title, 'message': self.message})
            _ = db.sql("""
                select * from records order by id desc limit 1
            """)
            if len(_) == 1:
                return Record(**_[0])
            else:
                raise ValueError('lol')


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
    def get_list(cls, *, search_terms: [str]):
        assert len(search_terms) < 2, 'Multiple search terms not supported'
        if search_terms:
            data = db.sql("""
            SELECT * FROM records
            WHERE title LIKE :search_term
            OR message LIKE :search_term
            """, {'search_term': f'%{search_terms[0]}%'})
        else:
            data = db.sql("""
            SELECT * FROM records
            """)
        return [cls(**record) for record in data]

    def __repr__(self):
        return f'Record ({self.id or "unsaved"}): {self.title}'

    def __str__(self):
        return self.__repr__()
