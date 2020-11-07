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

from database import *
from flask import session as login_session
##################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'flaskrocks'

############

############# chat app
#socketio = SocketIO(app)


# @app.route('/chat')
# def sessions():
#    return render_template('session.html')





#def messageReceived():
 #   print('message was received!!!')


#@socketio.on('my event')
#def handle_my_custom_event(json):
#    print('received my event: ' + str(json))
#    socketio.emit('my response', json, callback=messageReceived)


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
            entry = Names(email=request.form['email'], password=request.form['password'],name= request.form['name'])
            session.add(entry)
            session.commit()
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
            user_log = session.query(Names).filter_by(email=form.email.data).first()
            print("all right")
            print('user log' + str(user_log.password))
            print('current' + str(form.password.data))
            if form.password.data == user_log.password:
                login_session['username']=user_log.name
                return render_template(('session.html'), name=login_session['username'], messages=session.query(Messages).all())
    return render_template('login.html', form=form)

@app.route('/post',methods=['GET','POST'])
def post_message():
  if request.method=="POST":
    message1 = request.form["message"]
    print (message1)
    message2= Messages(name=login_session["username"],message=message1)
    session.add(message2)
    session.commit()
    return render_template(('session.html'), name=login_session['username'], messages=session.query(Messages).all())
  else:
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)
