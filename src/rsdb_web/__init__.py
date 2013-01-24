
# ok
# we don't stop running, now

# how to separate flask app into multiple files
# list of bits of the app
# html tabs for all the bits of the app
# mysoc lookup

# actions:
# display recipients
# tab scaffolding
# preview
# dispatch

from flask import Flask


from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
db = SQLAlchemy(app)

import routes

import os

def start(config):
    name          = config.get('server', 'name')
    db_name       = config.get('database', 'db_name')
    htpasswd_file = config.get('server', 'htpasswd_file')
    auth_realm    = config.get('server', 'http_auth_realm')
    secret_key    = config.get('server', 'secret_key')
    
    app.config['X-NAME'] = name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///%s' % db_name
    app.config['HTAUTH_REALM'] = auth_realm
    app.config['HTAUTH_HTPASSWD_PATH'] = htpasswd_file
    app.secret_key = secret_key

    app.run(debug=True)
