# coding: utf-8
from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'adm'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    user_type = Column(String, default='normal')
    password = Column(String, nullable=False)
    token = Column(String, nullable=False)
