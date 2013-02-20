#  MemberEdit, a basic web interface for running member lists, by Martin Keegan

#  Copyright (C) 2013  Martin Keegan
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the Apache Software Licence v2.0

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
    port          = config.getint('server', 'port')
    
    
    app.config['X-NAME'] = name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///%s' % db_name
    app.config['HTAUTH_REALM'] = auth_realm
    app.config['HTAUTH_HTPASSWD_PATH'] = htpasswd_file
    app.secret_key = secret_key

    app.run(debug=True, port=port)
