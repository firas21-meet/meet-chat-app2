from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
Base = declarative_base() 


class Names(Base):
	__tablename__ = 'names'
	id = Column(Integer, primary_key=True)
	email = Column(String(100))
	password = Column(String(100))
	name = Column(String(100))

	def __init__(self,email,password,name):
		self.email=email
		self.password=password
		self.name=name


class Messages(Base):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	message = Column(String(100))

