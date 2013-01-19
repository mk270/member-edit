
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

db_name = "rewired_state"
app = Flask(__name__.split('.')[0])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///%s' % db_name
app.secret_key = "66ca9513726c745a1e7d546bc67e9adc6994ff08"
db = SQLAlchemy(app)

import routes

def start():

    app.run(debug=True)

if __name__ == '__main__':
    start()
