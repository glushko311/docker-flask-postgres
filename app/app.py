import time
import datetime
import os
from flask import Flask, render_template, flash, redirect, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import hashlib
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


# class students(db.Model):
#     id = db.Column('student_id', db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     city = db.Column(db.String(50))
#     addr = db.Column(db.String(200))
#
#     def __init__(self, name, city, addr):
#         self.name = name
#         self.city = city
#         self.addr = addr
# #
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
    password = db.Column('password', db.LargeBinary, nullable=False)
    salt = db.Column('salt', db.LargeBinary, nullable=False)
    reg_date = db.Column('reg_date', db.Date, nullable=False)

    @staticmethod
    def hash_password(password, salt_len=16, iterations=100001, encoding='utf-8'):
        salt = os.urandom(salt_len)
        hashed_password = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=bytes(password, encoding),
            salt=salt,
            iterations=iterations
        )
        return salt, iterations, hashed_password

    @staticmethod
    def generate_salt(salt_len):
        return

    def __init__(self, login, email, password):
        self.login = login
        hashed_data = __class__.hash_password(password)
        self.salt = hashed_data[0]
        self.password = hashed_data[2]
        self.email = email
        self.reg_date = datetime.datetime.now()

    def __str__(self):
        return "User login - {0}; Email - {1}; Registered - {2}; Password hash - {3}; Salt - {4}".\
            format(self.login, self.email, str(self.reg_date), str(self.password), str(self.salt))

    @staticmethod
    def validate_user_create_data(req_args):
        if 'password' in req_args and 'login' in req_args and 'email' in req_args:
            return True
        else:
            return False


# def database_initialization_sequence():
#     db.create_all()
#     test_rec = students(
#             'John Doe',
#             'Los Angeles',
#             '123 Foobar Ave')
#
#     db.session.add(test_rec)
#     db.session.rollback()
#     db.session.commit()

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users = list(map(lambda x: str(x), users))
    resp = Response(json.dumps(users), status=200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/user', methods=['POST'])
def create_user():
    req_args = request.args
    if User.validate_user_create_data(req_args):
        user = User(req_args['login'], req_args['email'], req_args['password'])
        msg = "USER REGISTRATION SUCCESSFUL"
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            msg = str(e)
        resp = Response(json.dumps(msg), status=200)
    else:
        msg = "REQUIRED DATA NOT VALID"
        resp = Response(json.dumps(msg), status=400)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/smoke', methods=['GET'])
def smoke():
    resp = Response(json.dumps("OK"), status=200)
    #resp = Response("OK", status=200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
    # return Response(json.dumps("OK"), status=200)
#
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#             flash('Please enter all the fields', 'error')
#         else:
#             student = students(
#                     request.form['name'],
#                     request.form['city'],
#                     request.form['addr'])
#
#             db.session.add(student)
#             db.session.commit()
#             flash('Record was succesfully added')
#             return redirect(url_for('home'))
#     return render_template('show_all.html', students=students.query.all())


if __name__ == '__main__':

    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    # database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
