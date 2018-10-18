# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, session, flash,json, abort
from jdd.services.form_validator import RegisterForm, LoginForm, ResetForm
from jdd.services.database import db_session
from jdd.models.user import User, Subscribe, Tracking
from jdd.models.post import Article
from passlib.hash import sha256_crypt
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from jdd import app,flask_mail
from datetime import datetime

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    posts = Article.query.filter().order_by(Article.id.desc())
    return render_template('general/index.html',posts=posts)

@mod.route('/register/', methods=['GET','POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            password = sha256_crypt.hash(str(form.password.data))
            x = User.query.filter_by(email=email).first()
            if x :
                flash(u'邮箱已被注册，请重试！','error')
            else:
                new_user = User(name=name,email=email,password=password)
                db_session.add(new_user)
                db_session.commit()
                new_tarck = Tracking(confirmed_at=datetime.today(),owner=new_user)
                db_session.add(new_tarck)
                db_session.commit()
                flash(u'注册完成！请登录！')
                return redirect(url_for('general.login'))
        return render_template('general/register.html',form=form)
    except Exception as e:
        app.logger.info('User fails to registered, error : %s .',e)
        return render_template('general/register.html')

@mod.route('/login/', methods=['GET','POST'])
def login():
    try:
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if  user and sha256_crypt.verify(password, user.password):
                user.last_login_at = datetime.now()
                user.last_login_ip = request.remote_addr
                if user.login_count:
                    user.login_count += 1
                else:
                    user.login_count = 1
                db_session.commit()
                session.clear()
                login_user(user, remember=True)
                session['email'] = user.email
                session['name'] = user.name
                flash(u'登录成功！')
                return redirect(request.referrer or url_for('.index'))
            else:
                flash(u'登录失败！请重试！','error')
        return render_template('general/login.html',form=form)
    except Exception as e:
        app.logger.info('User fails to login, error : %s .',e)
        return render_template('general/login.html',form=form)
        # return str(e)

@mod.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'您已经安全退出登录!')
    return redirect(request.referrer or url_for('.index'))

    
@mod.route('/reset/', methods=['GET','POST'])
def reset():
    try:
        form = ResetForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data
            newpasswd = form.newpasswd.data
            user = User.query.filter_by(email=email).first()
            if  user:
                new = sha256_crypt.hash(str(newpasswd))
                user.newpasswd = new
                db_session.commit()
                link = "https://www.jdiandian.com/reset_confirm?email="+user.email+"&rank="+new

                msg = Message("今点点-重置密码!",
                    sender=("jdiandian","qinuo.traveler@gmail.com"),
                    recipients=[email])
                assert msg.sender == "jdiandian <qinuo.traveler@gmail.com>"
                # you can add the nickname in the template
                msg.html = render_template('mail/reset.html',link=link)
                flask_mail.send(msg)

                flash(u'一封确认邮件已经发送到您的邮箱!请检查')
                return redirect(request.referrer or url_for('general.login'))
            else:
                flash(u'这个邮箱还没有注册，请先注册!')
                return redirect(url_for('general.register'))
        return render_template('general/reset.html',form=form)
    except Exception as e:
        # return str(e)
        return render_template('general/reset.html')

@mod.route('/reset_confirm')
def reset_confirm():
    email = request.args.get('email')
    rank = request.args.get('rank')
    if not email or not rank:
        return redirect(url_for('general.index'))
    user = User.query.filter_by(email=email).first()
    if user and user.newpasswd == rank:
        user.password = rank
        db_session.commit()
        flash(u'新密码已设置成功，请登录！')
        return redirect(url_for('general.login'))
    else:
        return redirect(url_for('general.index'))

@mod.route('/help')
def user_help():
    return render_template('help/index.html')



# for admin login and logout
@mod.route('/admin_login/',methods=['GET','POST'])
def admin_login():
    if session.get('admin_in',False):
        flash('You are already logged in!')
        return redirect('/admin')
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if (name == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']):
            session['admin_in'] = True
            return redirect('/admin')
        else:
            app.logger.info('ADMIN-LOGIN: %s fail to login as admin',name)
            flash('Invalid Credential!~ try agiain!')
    return render_template('admin_login.html')

@mod.route('/admin_logout/')
def admin_logout():
    if session.get('admin_in', None):
        session['admin_in'] = False
        flash("Successfully logged out")
    else:
        flash("You weren't logged in !")
    return render_template('admin_login.html')



@mod.route('/author/<int:author_id>')
def author_info(author_id):
    user = User.query.get(author_id)
    if not user.summary:
        return u'大侠已经来过，就是还没有留下足迹!',200
    else:
        return str(user.summary),200



@mod.route('/subscribe',methods=['POST'])
def new_subscriber():
    if not current_user.is_authenticated:
        return u'请先登录:3'
    req = request.get_json(force=True)
    if req:
        user_id = req.get('id',None)
        user_name = req.get('name',None)
        if user_id and user_name:
            sub_id = int(current_user.get_id())
            if int(user_id) == sub_id:
                return u'您不能订阅自己！'
            sub = Subscribe.query.filter_by(subscriber_id=sub_id,user_id=int(user_id)).first()
            if sub:
                return u'您已经订阅！若需要取消，请到用户中心。'
            else:
                user = User.query.get(user_id)
                if user.subscribe:
                    user.subscribe += 1
                else:
                    user.subscribe = 1
                db_session.commit()
                new = Subscribe(user_id=user_id,user_name=user.name,subscriber_id=sub_id,update=0)
                db_session.add(new)
                db_session.commit()
                return u'您已订阅成功',200
        else:
            return abort(400)
    else:
        return abort(404)


