import sys

from flask import request, render_template, flash, redirect, url_for, get_flashed_messages, Flask, g
from flask.ext import htauth

import pystache

from rsdb_web import app, db
from models import *
import json
import os

from flask.ext.wtf import Form, TextField, BooleanField, Required
from wtforms.ext.sqlalchemy.orm import model_form

htpasswd_file = 'htpasswd'
auth_realm = 'Rewired State DB'
HTPASSWD = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        htpasswd_file)

app.config['HTAUTH_HTPASSWD_PATH'] = HTPASSWD
app.config['HTAUTH_REALM'] = auth_realm

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
            "person": Person.query.filter(Person.id==person_id).first()
            })


@app.route('/')
@htauth.authenticated
def people():
    return render({
            "people_list": True,
            "person": [ i.to_dict() for i in Person.query.all() ]
            })
