import time
import datetime
from flask import Flask, render_template, flash, redirect, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import json

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr
#
# class User(db.Model):
#     id = db.Column('id', db.Integer, primary_key=True)
#     login = db.Column('login', db.String, unique=True, not_null=True)
#     email = db.Column('email', db.String, unique=True, not_null=True)
#     password = db.Column('password', db.String, not_null=True)
#     reg_date = db.Column('reg_date', db.Date, not_null=True)
#     first_name = db.Column('first_name', db.String)
#     last_name = db.Column('last_name', db.String)
#     telephone = db.Column('telephone', db.String)
#     last_login_date = db.Column('reg_date', db.Date, not_null=True)
#     def __init__(self, login, email, password):
#         self.login = login
#         self.password = password
#         self.email = email
#         self.reg_date = datetime.datetime.now()

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.String(100), unique=True, nullable=False)
    email = db.Column('email', db.String, unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    reg_date = db.Column('reg_date', db.Date, nullable=False)
    def __init__(self, login, email, password):
        self.login = login
        self.password = password
        self.email = email
        self.reg_date = datetime.datetime.now()

def database_initialization_sequence():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route('/user', methods=['POST'])
def create_user():
    return Response(json.dumps("Create new user - OK"), status=200)

@app.route('/smoke', methods=['GET'])
def smoke():
    resp = Response(json.dumps("OK"), status=200)
    #resp = Response("OK", status=200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
    # return Response(json.dumps("OK"), status=200)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(
                    request.form['name'],
                    request.form['city'],
                    request.form['addr'])

            db.session.add(student)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('show_all.html', students=students.query.all())


if __name__ == '__main__':

    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
