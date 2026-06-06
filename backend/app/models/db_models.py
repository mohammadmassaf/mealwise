from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()   

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer , primary_key = True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String,nullable = False)
class User(Base):
    __tablename__ = "users"

class User(Base):
    __tablename__ = "users"

class User(Base):
    __tablename__ = "users"

class User(Base):
    __tablename__ = "users"
