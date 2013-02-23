#  MemberEdit, a basic web interface for running member lists, by Martin Keegan

#  Copyright (C) 2013  Martin Keegan
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the Apache Software Licence v2.0

import sys
import datetime

from flask import request, render_template, flash, redirect, url_for, get_flashed_messages, Flask, g
from flask.ext import htauth

import pystache

from rsdb_web import app, db
from models import *
import json

from flask.ext.wtf import Form, TextField, BooleanField, Required
from wtforms.ext.sqlalchemy.orm import model_form

auth = htauth.HTAuth(app)

class MyForm(Form):
    name = TextField('Name')
    email = TextField('Email')
    telno = TextField('Phone')
    no_more_email = BooleanField('No more email')

def render(data):
    messages = get_flashed_messages()
    data['messages'] = (len(messages) > 0)
    data['message'] = [ { 'message_text': m } for m in messages ]
    template = file('static/index.html').read() # don't cache this, really
    data['application_name'] = app.config['X-NAME']
    min_age = 7
    this_year = datetime.datetime.today().year - min_age
    data['years'] = [ { "year": str(y) } for y in xrange(this_year, 1940, -1) ]
    return pystache.render(template, data)

@app.route("/save-person/<person_id>", methods=['POST'])
@htauth.authenticated
def save(person_id):
    person = Person.query.filter(Person.id==person_id).first()
    person.name = request.form['name']
    person.email = request.form['email']
    db.session.add(person)
    try:
        db.session.commit()
        flash("Saved.")
    except:
        db.session.rollback()
        flash("Failed to save:")
        err_msg = str(sys.exc_info()[1])
        flash(err_msg)

    return redirect('/person/%s' % person_id)

@app.route("/edit/<person_id>")
@htauth.authenticated
def edit(person_id):
    model = Person.query.filter(Person.id==person_id).first()
    form = MyForm(request.form, model, csrf_enabled=False)
    form.populate_obj(model)

    return render({
            "person_update": True,
            "name": form.name,
            "email": form.email,
            "telno": form.telno,
            "id": person_id,
            "no_more_email": form.no_more_email
            })

@app.route('/person/<person_id>')
@htauth.authenticated
def person(person_id):
    return render({
            "person_details": True,
            "person": Person.query.filter(Person.id==person_id).first().to_dict()
            })

def make_order(cls, order_keys):
    orders = dict([ (i, getattr(cls, i)) for i in order_keys ])

    order_str = request.args.get('order', None)

    if order_str not in orders:
        return lambda q: q
    else:
        return lambda q: q.order_by(orders[order_str])

def transform_query(cls, order_keys, filters):
    query = cls.query
    filters.append(make_order(cls, order_keys))
    for f in filters:
        query = f(query)
    return query

def make_list(cls, cls_name, order_keys, filters):
    q = transform_query(cls, order_keys, filters)
    data = {
        (cls_name + "_list"): True,
        "summary": { 
            "table_name": cls_name.title(),
            "count": cls.query.count() 
            },
        cls_name: [ i.to_dict() for i in q ]
        }
    return render(data)

@app.route('/')
@htauth.authenticated
def people(**kwargs):
    filters = []
    search_terms = [
        ("name", "name"),
        ("location", "city")
        ]

    def add_filter(url_arg, attribute):
        if url_arg in request.args:
            val = request.args.get(url_arg)
            if val != "":
                match = getattr(Person, attribute)
                filters.append(lambda q: q.filter(match == val))

    [ add_filter(url_arg, attribute) for url_arg, attribute in search_terms ]
            
    order_keys = [ "name", "email", "telno", "twitter_id" ]
    return make_list(Person, "person", order_keys, filters)

@app.route('/centres')
@htauth.authenticated
def centres():
    filters = []
    order_keys = [ "name", "city", "email" ]
    return make_list(Centre, "centre", order_keys, filters)

