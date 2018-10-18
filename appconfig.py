# -*- coding: utf-8 -*-
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = False
    SECRET_KEY = 'SECRET-key'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = '#hack@you'
    BASE_POSTS_PATH = '/var/www/FlaskApp/jdd/static/posts/'
    RECAPTCHA_PUBLIC_KEY = '12345'
    RECAPTCHA_PRIVATE_KEY = '54321'

class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

class TestingConifg(BaseConfig):
    TESTING = True
    DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'flask.db')
    DATABASE_CONNECT_OPTIONS = {}



config = {
    'development':DevelopmentConfig,
    'prodcution': ProductionConfig,
    'testing':TestingConifg
}

del os