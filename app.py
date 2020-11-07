from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from wtforms import Form, BooleanField, PasswordField, StringField, validators
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, AnyOf
from flask_socketio import SocketIO
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##################
app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

app.config['SECRET_KEY'] = 'flaskrocks'
db = SQLAlchemy(app)

############


############# chat app
socketio = SocketIO(app)


# @app.route('/chat')
# def sessions():
#    return render_template('session.html')





def messageReceived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


##-----------------------------------------------------------------------


###### log in and sigh up
class registrants(FlaskForm):
    email = StringField('email', validators=[InputRequired('A email is required!')], render_kw={"placeholder": "email"})
    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25,
                                                                                                      message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25,
                                                                                                        message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"),
                                                             EqualTo('password', message="Passwords must match")])

    def validate_username(self, username):
        user_object = names.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")


class names(db.Model):
    __tablename__ = 'signedusers'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

def query_by_name(their_name):

    """
   Print all the students
   in the database.
   """
    student = db.session.query(names).filter_by(name=their_name).first()
    return student

######### find info by the name of the student >>>>>
#studentname_ofStusent = 'firas'
#print(query_by_name(name_ofStusent).name)
#print(query_by_name(name_ofStusent).password)
#print(query_by_name(name_ofStusent).email)


def update_lab_status(name, password):
   """
   Update a student in the database, with
   whether or not they have finished the lab
   """
   student_object = db.session.query(
       names).filter_by(
       name=name).first()
   student_object.password = password
   db.session.commit()

######### to udate in the database
#update_lab_status("1", '1')

def delete_student(their_name):
   """
   Delete all students with a
   certain name from the database.
   """
   db.session.query(names).filter_by(
       name=their_name).delete()
   db.session.commit()


#delete_student("1")

def query_by_id(their_id):

    """
   Print all the students
   in the database.
   """
    student = db.session.query(
       names).filter_by(
       id=their_id).first()
    return student
#### for loop to show you the all student i our app
def for_allStudent():
    z=1
    for i in range(20):
        if z!= 7:
            print('ID : '+str(query_by_id(z).id)+' ------name: ' + query_by_id(z).name+' password : '+query_by_id(z).password+' email : '+query_by_id(z).email)
            z+=1
        else:
            z+=1
#for_allStudent()

print ("done")

@app.route('/<username>')
def index(username):
    return 'hello %s' % username


@app.route('/test')
def test():
    return render_template('signup.html')


#@app.route('/')
#def defult():

#    return render_template('das.html')


@app.route('/signup', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            registered = names.query.all()
            return render_template('request.html', registered=registered)
        else:
            entry = names(request.form['email'], request.form['password'], request.form['name'])
            db.session.add(entry)
            db.session.commit()
            print(request.form['email'] + '' + request.form['password'] + request.form['name'])
            return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    form = registrants()

    print("not yet")
    if request.method == 'POST':
        req = request.form
        print("post")
        if req['submit_button'] == 'Log_In':
            print(req["email"])
            user_log = db.session.query(names).filter_by(email=form.email.data).first()
            print("all right")
            print('user log' + str(user_log.password))
            print('current' + str(form.password.data))
            if form.password.data == user_log.password:
                return render_template(('session.html'), name=form.email.data)
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)
