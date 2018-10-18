# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, session, url_for
import os
import sys
sys.path.append('..')
from jdd.services.database import db_session
from jdd.models.user import User, Tracking, Subscribe
from jdd.models.post import Article, ArticleBody
from flask_mail import Mail
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import  UploadSet,configure_uploads, IMAGES
from appconfig import config
from flaskext.markdown import Markdown


# set up APP and CONFIG
app = Flask(__name__)
config_name = config['development']
app.config.from_object(config_name)

# set up markdown filter
Markdown(app)

# set up flask-login
login_manager = LoginManager()
login_manager.login_view = 'general.login'
login_manager.login_message = u'请先登录!'
# login_manager.session_protection = "strong"
login_manager.needs_refresh_message = u'To protect your account, please refresh.'
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#  set up flask-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'qinuo.traveler@gmail.com'
app.config['MAIL_PASSWORD'] = '@hack2you'
flask_mail = Mail(app)

# set up flask-Admin
flask_admin = Admin(app, name='jdiandian', template_mode='bootstrap3')
class CheckModelView(ModelView):
    def is_accessible(self):
            if session.get('admin_in',False):
                return True
            else:
                return False
flask_admin.add_view(CheckModelView(User, db_session))
flask_admin.add_view(CheckModelView(Tracking, db_session))
flask_admin.add_view(CheckModelView(Subscribe, db_session))
flask_admin.add_view(CheckModelView(Article, db_session))
flask_admin.add_view(CheckModelView(ArticleBody, db_session))


# set up flask-uploads
app.config['UPLOADED_AVATARS_DEST'] = '/var/www/FlaskApp/jdd/static/uploads/avatars/'
app.config['UPLOADED_DONATES_DEST'] = '/var/www/FlaskApp/jdd/static/uploads/donates/'
app.config['UPLOADS_DEFAULT_DEST'] = '/var/www/FlaskApp/jdd/static/uploads/'
# there are DEFAUTL(text.doc.data,images), ALL, TEXT, IMAGES, AUDIO, DOCUMENTS, DATA, 
# SCRIPTS, ARCHIVES, EXECUTABLES for choice
avatars = UploadSet('avatars', IMAGES)
donates = UploadSet('donates',IMAGES)
configure_uploads(app, avatars)
configure_uploads(app, donates)


#error handler test
'''
@app.before_request
def load_current_user():
    pass
'''

@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def not_Found(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def not_Found(error):
    return render_template('500.html'),500



@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


# set up blueprint :register all route from routes
from jdd.routes import general, post, dashboard, invite

app.register_blueprint(general.mod)
app.register_blueprint(post.mod, url_prefix='/post')
app.register_blueprint(dashboard.mod, url_prefix='/dashboard')
app.register_blueprint(invite.mod, url_prefix='/invite')


