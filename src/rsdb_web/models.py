
from rsdb_web import db

class Person(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telno = db.Column(db.String(100))
    no_more_email = db.Column(db.Boolean)
    birth_year = db.Column('birthyear', db.Integer)
    postcode = db.Column(db.String(8))
    city = db.Column(db.String(45))

    def __init__(self, id, name, email, 
                 telno, no_more_email,
                 birth_year, postcode, city):
        self.id = id
        self.name = name
        self.email = email
        self.telno = telno
        self.no_more_email = no_more_email
        self.birth_year = birth_year
        self.postcode = postcode
        self.city = city

    def __repr__(self):
        return '<Person %r>' % self.id

    def to_dict(self):
        return { 
            "name": self.name,
            "email": self.email,
            "telno": self.telno,
            "id": self.id,
            "no_more_email": self.no_more_email,
            "birth_year": self.birth_year,
            "postcode": self.postcode,
            "city": self.city
            }
