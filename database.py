from model import *
import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime


engine = create_engine('sqlite:///tables.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession() 



def query_by_name(their_name):

    """
   Print all the students
   in the database.
   """
    student = session.query(names).filter_by(name=their_name).first()
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
   student_object = session.query(
       Names).filter_by(
       name=name).first()
   student_object.password = password
   session.commit()

######### to udate in the database
#update_lab_status("1", '1')

def delete_student(their_name):
   """
   Delete all students with a
   certain name from the database.
   """
   session.query(Names).filter_by(
       name=their_name).delete()
   session.commit()


#delete_student("1")

def query_by_id(their_id):

    """
   Print all the students
   in the database.
   """
    student = session.query(
       Names).filter_by(
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

# firas = Names(email="firas@gmail",password="pass",name="firas")
# session.add(firas)
# session.commit()