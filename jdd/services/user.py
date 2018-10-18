# -*- coding: utf-8 -*-
from database import Model, db_session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import backref, relation
from flask_login import UserMixin
# from sqlalchemy.event import listen

class User(UserMixin, Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column('email', String(255),unique=True)
    name = Column(String(20))
    password = Column(String(255))
    newpasswd = Column(String(255))
    subscribe = Column(Integer)
    summary = Column(String(9999))
    ijcoin = Column(Integer)
    setting = Column(String(999))
    last_login_at = Column(DateTime())
    last_login_ip = Column(String(128))
    login_count = Column(Integer)
    active = Column(Boolean())
    rank = Column(String(255))


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % (self.email)

class Tracking(Model):
    __tablename__ = 'tracking'
    id = Column(Integer(),primary_key=True)
    user_id = Column(Integer(),ForeignKey('user.id'))
    sex = Column(String(10))
    phone = Column(String(26))
    address = Column(String(255))
    birthday = Column(DateTime())
    marriage = Column(String(10))
    hobby = Column(String(999))
    confirmed_at = Column(DateTime())
    rank = Column(String(255))

    owner = relation(User, backref=backref('tracking',lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Tracking, self).__init__(**kwargs)

    def __repr__(self):
        return '<Tracking %r>' % (self.id)

class Subscribe(Model):
    __tablename__ = 'subscribe'
    id = Column(Integer, primary_key=True )
    user_id = Column(Integer)
    user_name = Column(String(20))
    subscriber_id = Column(Integer)
    update = Column(Integer)
    rank = Column(String(255))

    def __init__(self, **kwargs):
        super(Subscribe, self).__init__(**kwargs)

    def __repr__(self):
        return '<Subscribe %r>' % (self.id)  