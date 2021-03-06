#  MemberEdit, a basic web interface for running member lists, by Martin Keegan

#  Copyright (C) 2013  Martin Keegan
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the Apache Software Licence v2.0

from rsdb_web import db
import phonenum

class Person(db.Model):
    __tablename__ = "people_aged"

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
    mainly_a = db.Column(db.String(50))
    availability = db.Column(db.String(50))
    age = db.Column(db.Integer)
    mentor = db.Column(db.Boolean)
    yrser = db.Column(db.Boolean)
    yrs_current = db.Column(db.Boolean)
    dob = db.Column(db.Date)

    def __init__(self, id, name, email, 
                 telno, no_more_email,
                 birth_year, postcode, city,
                 notes, github_id, twitter_id,
                 mainly_a, availability, age, mentor,
                 yrser, yrs_current, dob):
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
        self.mainly_a = mainly_a
        self.availability = availability
        self.age = age
        self.mentor = mentor
        self.yrser = yrser
        self.yrs_current = yrs_current
        self.dob = dob

    def __repr__(self):
        return '<Person %r>' % self.id

    def to_dict(self):
        def hash_or_null(field_name, s):
            if s is None:
                return []
            else:
                return [ { field_name : s } ]
        def title_or_none(s):
            if s is None:
                return ""
            return s.title()
        def canonicalise_twitter_id(s):
            if s is None: return None
            if s == "": return None
            if s[0] == '@': return s[1:]
            return s
        def none_to_null(s):
            if s is None: return ""
            return s
        def format_age(a):
            if isinstance(a, float): return int(a)
            if a is None: return None
            return int(a)
        def format_bool_true(b):
            return bool(b)
        def yrs_status(current, member):
            if not member: return "Not a YRS member"
            if not current: return "YRS Alumnus"
            return "Current YRSer"
        return { 
            "name": title_or_none(self.name),
            "email": hash_or_null("email_address", self.email),
            "telno": phonenum.canonicalise(none_to_null(self.telno)),
            "id": self.id,
            "no_more_email": none_to_null(self.no_more_email),
            "birth_year": self.birth_year,
            "postcode": none_to_null(self.postcode),
            "city": none_to_null(self.city),
            "notes": none_to_null(self.notes),
            "github":  hash_or_null("github_id",  self.github_id),
            "twitter": hash_or_null("twitter_id", 
                                    canonicalise_twitter_id(self.twitter_id)),
            "mainly_a": none_to_null(self.mainly_a),
            "availability": none_to_null(self.availability),
            "age": format_age(self.age),
            "mentor": format_bool_true(self.mentor),
            "yrser": none_to_null(self.yrser),
            "yrs_status": yrs_status(self.yrs_current, self.yrser),
            "dob": self.dob
            }



class Centre(db.Model):
    __tablename__ = "centre"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(45))
    name = db.Column(db.String(45))
    email = db.Column("contactemail", db.String(90))

    def __init__(self, id, city, name, email):
        self.id = id
        self.city = city
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Centre %r>' % self.id

    def to_dict(self):
        return { 
            "name": self.name,
            "email": self.email,
            "id": self.id,
            "city": self.city
            }
