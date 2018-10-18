# -*- coding: utf-8 -*-
from jdd.services.database import Model, db_session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import backref, relation
from werkzeug import cached_property


class IClassify(Model):
    __tablename__ = 'iclassify'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    cover = Column(String(255))
    rank = Column(String(255))

    def __init__(self, **kwargs):
        super(IClassify, self).__init__(**kwargs)

    @cached_property
    def count(self):
        return self.invitation.count()

    def __repr__(self):
        return '<IClassify %r>' % (self.name)


class Invitation(Model):
    __tablename__ = 'invitation'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('iclassify.id'))
    creater = Column(Integer)
    creater_name = Column(String(20))
    title = Column(String(255))
    time = Column(DateTime())
    address = Column(String(255))
    content = Column(String(9999))
    praise = Column(Integer)
    rank = Column(String(255))

    iclassify = relation(IClassify, backref=backref(
        'invitation', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Invitation, self).__init__(**kwargs)

    def to_json(self):
        return dict(
            id=self.id,
            cid=self.cid,
            creater=self.creater,
            creater_name=self.creater_name,
            title=self.title,
            time=self.time,
            address=self.address,
            content=self.content,
            praise=self.praise,
        )

    def __repr__(self):
        return '<Invaitation %r>' % (self.title)


class IPhoto(Model):
    __tablename__ = 'iphoto'
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('invitation.id'))
    photo1 = Column(String(255))
    photo2 = Column(String(255))
    photo3 = Column(String(255))
    photo4 = Column(String(255))
    photo5 = Column(String(255))
    rank = Column(String(255))

    invite_photo = relation(
        Invitation, backref=backref('iphoto', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(IPhoto, self).__init__(**kwargs)

    def to_json(self):
        return dict(
            photo1 = self.photo1
            photo2 = self.photo2
            photo3 = self.photo3
            photo4 = self.photo4
            photo5 = self.photo5
        )


class Ijoin(Model):
    __tablename__ = 'ijoin'
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('invitation.id'))
    user_id = Column(Integer)
    user_name = Column(String(20))
    cid = Column(String(50))
    title = Column(String(255))
    time = Column(DateTime())
    address = Column(String(255))
    content = Column(String(9999))
    rank = Column(String(255))

    invite_join = relation(
        Invitation, backref=backref('ijoin', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Ijoin, self).__init__(**kwargs)

    def to_json(self):
        return dict(
            iid=self.iid
            cid=self.cid,
            title=self.title,
            time=self.time,
            address=self.address,
            content=self.content,
        )

    def __repr__(self):
        return '<Ijoin %r>' % (self.user_name)


class IComment(Model):
    __tablename__ = 'icomment'
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('invitation.id'))
    user_id = Column(Integer)
    user_name = Column(String(20))
    date = Coumn(DateTime())
    body = Column(String(255))
    rank = Column(String(255))

    invite_comment = relation(
        Invitation, backref=backref('icomment', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(IComment, self).__init__(**kwargs)

    def to_json(self):
        return dict(
            user_id=self.user_id,
            user_name=self.user_name,
            body=self.body
        )

    def __repr__(self):
        return '<IComment %r>' % (self.user_name)
