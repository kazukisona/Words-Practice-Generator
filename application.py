#import sqlite3
import pdfkit
import miningwords
from flask import Flask, request, session, g, redirect, url_for, render_template, make_response

# configuration
# DATABASE = 'words.db'
DEBUG = True # should be True if in test or in development
#SECRET_KEY = 'your_secret_key'
#USERNAME = 'your_username'
#PASSWORD = 'your_password'

POSTGRES = {
    'user': 'kazuki',
    'pw': '11ea487t',
    'db': 'words',
    'host': 'localhost',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(app)

class GRE(db.Model):
    __tablename__ = 'gre'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100))
    meaning = db.Column(db.String(400))



# create app   
application = Flask(__name__)
application.config.from_object(__name__)


### database ###
# connect to database
def connect_db():
    conn = sqlite3.connect(application.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# create database
def init_db():
    with application.app_context():
        db = get_db()
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            # fill a table with data
            miningwords.loadData(db)
        
        db.commit()

# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close database connection
@application.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@application.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


### Routing ###
@application.route('/')
def index():
    return render_template("index.html")

# Display a full listing of words
@application.route('/list')
def word_list():
    db = get_db()
    # selectiong all words and their meaning in ascending order
    cur = db.execute("SELECT * FROM words ORDER BY word;")
    words = cur.fetchall()

    return render_template("word_list.html", words=words)


@application.route('/practice', methods=['POST'])
def practice_template():
    db = get_db()
    # selecting words randomly
    cur = db.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT ?;", [request.form.get('numofwords')])
    words = cur.fetchall()

    # either word to meaning or meaning to word
    t_type = request.form.get('testing')

    # get a result of html file rendered words data
    rendered = render_template('practice_sheet.html', words=words, type=t_type)
    
    # setting options for pdf
    options={'page-size':'letter', 'dpi':1200}
    # False if you want to do something after creating pdf object
    pdf = pdfkit.from_string(rendered, False, css='static/style.css', options=options)

    # make a response with the pdf
    res = make_response(pdf)
    # specify Content-Type
    res.headers['Content-Type'] = 'application/pdf'
    # specifying Content-Disposition with 'inline' means you can review pdf file on browser 
    res.headers['Content-Disposition'] = 'inline; filename=wordlist.pdf'

    return res


if __name__ == "__main__":
    init_db()
    application.run()