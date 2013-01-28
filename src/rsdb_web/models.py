#  MemberEdit, a basic web interface for running member lists, by Martin Keegan

#  Copyright (C) 2013  Martin Keegan
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the Apache Software Licence v2.0

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
    notes = db.Column(db.Text)
    github_id = db.Column(db.String(100))
    twitter_id = db.Column("twitter", db.String(45))
    
    def __init__(self, id, name, email, 
                 telno, no_more_email,
                 birth_year, postcode, city,
                 notes, github_id, twitter_id):
        self.id = id
        self.name = name
        self.email = email
        self.telno = telno
        self.no_more_email = no_more_email
        self.birth_year = birth_year
        self.postcode = postcode
        self.city = city
        self.notes = notes
        self.github_id = github_id
        self.twitter_id = twitter_id

    def __repr__(self):
        return '<Person %r>' % self.id

    def to_dict(self):
        def hash_or_null(field_name, s):
            if s is None:
                return []
            else:
                return [ { field_name : s } ]
        return { 
            "name": self.name,
            "email": hash_or_null("email_address", self.email),
            "telno": self.telno,
            "id": self.id,
            "no_more_email": self.no_more_email,
            "birth_year": self.birth_year,
            "postcode": self.postcode,
            "city": self.city,
            "notes": self.notes,
            "github":  hash_or_null("github_id",  self.github_id),
            "twitter": hash_or_null("twitter_id", self.twitter_id)
            }
