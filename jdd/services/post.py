# -*- coding: utf-8 -*-
from database import Model, db_session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import backref, relation
from werkzeug import cached_property, http_date

class Classify(Model):
    __tablename__ = 'classify'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    rank = Column(String(255))

    def __init__(self, **kwargs):
        super(Classify, self).__init__(**kwargs)

    def __repr__(self):
        return '<Classify %r>' % (self.name)

    @cached_property
    def count(self):
        return self.article.count()

class Article(Model):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    post_type = Column(String(10))
    classify_id = Column(Integer, ForeignKey('classify.id'))
    author_id = Column(Integer)
    author = Column(String(255))
    cover = Column(String(255))
    title = Column(String(255))
    date = Column(DateTime())
    summary = Column(String(9999))
    tags = Column(String(255))
    views = Column(Integer)
    location = Column(String(255))
    praise = Column(String(10))
    rank = Column(String(255))


    classify = relation(Classify, backref=backref('article',lazy='dynamic'))
    body = relation('ArticleBody', backref=backref('article',uselist=False))

    def __init__(self, **kwargs):
        super(Article, self).__init__(**kwargs)

    def __repr__(self):
        return '<Article %r>' % (self.title)

class ArticleBody(Model):
    __tablename__ = 'article_body'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    date = Column(DateTime())
    body = Column(Text)
    rank = Column(String(255))

    owner = relation(Article, backref=backref('articlebody'))

    def __init__(self, **kwargs):
        super(ArticleBody, self).__init__(**kwargs)

    def __repr__(self):
        return '<ArticleBody %r>' % (self.id)

class Comment(Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    user_id = Column(Integer)
    user_name = Column(String(20))
    date = Column(DateTime())
    body = Column(Text)
    praise =Column(String(10))
    rank = Column(String(255))

    article = relation(Article, backref=backref('comment',lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)

    def to_json(self):
        return dict(id=self.user_id,
                    name=self.user_name,
                    body=self.body,
                    praise=self.praise
        )

    def __repr__(self):
        return '<Comment %r>' % (self.comment_id)









