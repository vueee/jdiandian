# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, send_from_directory, abort
from jdd.services.form_validator import NewPostForm
from jdd.services.database import db_session
from jdd.services.utils import safe_script
from jdd.models.post import Classify, Article, ArticleBody, Comment
from flask_login import current_user, login_required
from datetime import date as dt
import time
from jdd import app


mod = Blueprint('post', __name__)

@mod.route('/')
@login_required
def index():
    author_id = current_user.get_id()
    posts = Article.query.filter_by(author_id=author_id).order_by(Article.id.desc())
    return render_template('post/index.html',posts=posts)

@mod.route('/<int:post_id>')
def show_post(post_id):
    post = Article.query.get(post_id)
    if post and post.location:
        if post.views:
            count = post.views +1 
        else:
            count = 1
        post.views=count
        db_session.commit()
        return send_from_directory(app.config['BASE_POSTS_PATH'],post.location)
    else:
        post_body = ArticleBody.query.filter_by(article_id=post.id).first()
    app.logger.info('STATIC: Post %s dont have a static page!',str(post.author_id))
    return render_template('post/show_post.html',post=post,post_body=post_body)


@mod.route('/new_text/',methods=['GET','POSt'])
@login_required
def new_text():
    try:
        form = NewPostForm(request.form)
        if request.method == 'POST' and form.validate():
            post_type = 'text'
            classify = form.name.data
            cover = form.cover.data
            author_id = current_user.get_id()
            title = form.title.data
            author = session.get('name','')
            date = dt.today()
            summary = form.summary.data
            tags = form.tags.data
            body = safe_script(form.body.data)
            location = str(author_id)+'_'+str(int(time.time()))+'.html'
            c = Classify.query.filter_by(name=classify).first()
            if not c:
                new_c = Classify(name=classify)
                db_session.add(new_c)
                db_session.commit()

            new_a = Article(post_type=post_type,cover=cover,author_id=author_id,title=title,author=author,date=date,summary=summary,tags=tags,classify=c)
            db_session.add(new_a)
            db_session.commit()

            new_b = ArticleBody(body=body,owner=new_a)
            db_session.add(new_b)
            db_session.commit()
            flash('post add!')
            # convert to static html
            file_path = app.config['BASE_POSTS_PATH']+location
            url = '/post/'+str(new_a.id)
            response = app.test_client().get(url)
            if response.status_code != 200:
                app.logger.info('STATIC: Post %s make mistake in create a new static page!',str(new_a.id))
                return redirect(url_for('post.index'))
            else:
                content = response.data
                with open(file_path, 'wb') as fd:
                    fd.write(content)
            response.close()
            new = Article.query.get(new_a.id)
            new.location = location
            db_session.commit()  
            # return the static page
            return send_from_directory(app.config['BASE_POSTS_PATH'],location)
            # return the static page
        return render_template('post/new_text.html',form=form)
    except Exception as e:
        # return str(e)
        return render_template('post/new_text.html',form=form)

@mod.route('/new_md/',methods=['GET','POST'])
@login_required
def new_md():
    try:
        form = NewPostForm(request.form)
        if request.method == 'POST' and form.validate():
            post_type = 'md'
            classify = form.name.data
            cover = form.cover.data
            author_id = current_user.get_id()
            title = form.title.data
            author = session.get('name','')
            date = dt.today()
            summary = form.summary.data
            tags = form.tags.data
            body = safe_script(form.body.data)
            location = str(author_id)+'_'+str(int(time.time()))+'.html'
            c = Classify.query.filter_by(name=classify).first()
            if not c:
                new_c = Classify(name=classify)
                db_session.add(new_c)
                db_session.commit()

            new_a = Article(post_type=post_type,cover=cover,author_id=author_id,title=title,author=author,date=date,summary=summary,tags=tags,classify=c)
            db_session.add(new_a)
            db_session.commit()

            new_b = ArticleBody(body=body,owner=new_a)
            db_session.add(new_b)
            db_session.commit()
            flash('post add!')
            # convert to static html
            file_path = app.config['BASE_POSTS_PATH']+location
            url = '/post/'+str(new_a.id)
            response = app.test_client().get(url)
            if response.status_code != 200:
                app.logger.info('STATIC: Post %s make mistake in create a new static page!',str(new_a.id))
                return redirect(url_for('post.index'))
            else:
                content = response.data
                with open(file_path, 'wb') as fd:
                    fd.write(content)
            response.close()
            new = Article.query.get(new_a.id)
            new.location = location
            db_session.commit()    
            # return the static page
            return send_from_directory(app.config['BASE_POSTS_PATH'],location)
        return render_template('post/new_md.html',form=form)
    except Exception as e:
        return str(e)
        # return render_template('post/new_md.html',form=form)



@mod.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    try:
        form = NewPostForm(request.form)
        post = Article.query.get(post_id)
        if post is None or int(current_user.get_id()) != post.author_id :
            return redirect(url_for('post.index'))
        pt = post.post_type
        post_body = ArticleBody.query.filter_by(article_id=post_id).first()
        if request.method == 'POST' and form.validate():
            if post.location:
                location = post.location
            else:
                location = str(post.author_id)+'_'+str(int(time.time()))+'.html'
            post.location = ''
            post.cover = form.cover.data
            post.title = form.title.data
            post.summary = form.summary.data
            post.tags = form.tags.data
            post_body.date = dt.today()
            post_body.body = form.body.data
            db_session.commit()
            flash('post update !')
            # convert to static html
            file_path = app.config['BASE_POSTS_PATH']+location
            url = '/post/'+str(post.id)
            response = app.test_client().get(url)
            if response.status_code != 200:
                app.logger.info('STATIC: Post %s make mistake in create a new static page!',str(post.id))
                return redirect(url_for('post.index'))
            else:
                content = response.data
                with open(file_path, 'wb') as fd:
                    fd.write(content)
            response.close()
            new = Article.query.get(post.id)
            new.location = location
            db_session.commit()
            # return the static page
            return send_from_directory(app.config['BASE_POSTS_PATH'],location)
        form.cover.data = post.cover
        form.title.data = post.title
        form.summary.data = post.summary
        form.tags.data = post.tags
        form.body.data = post_body.body
        if pt == 'text':
            return render_template('post/new_text.html',form=form)
        elif pt == 'md':
            return render_template('post/new_md.html',form=form)
        else:
            return redirect(url_for('post.index'))
    except Exception as e:
        # return str(e)
        return redirect(url_for('post.index'))




@mod.route('/<int:post_id>/delete',methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Article.query.get(post_id)
    if int(current_user.get_id()) != post.author_id:
        return u'permission denied'
    if post:
        pb = ArticleBody.query.filter_by(article_id=post_id).first()
        db_session.delete(pb)
        db_session.delete(post)
        db_session.commit()
    else:
        return abort(404)
    return u'文章已经删除！',200

@mod.route('/<int:post_id>/comment/add',methods=['POST'])
def add_comment(post_id):
    if not current_user.is_authenticated:
        return u'请先登录！'
    req = request.get_json(force=True)
    if req:
        article_id = post_id
        user_id = current_user.get_id()
        user_name = session.get('name','')
        date = dt.today()
        praise = req.get('praise',None)
        body =req.get('body',None)
        if not body:
            return u'请填写评论内容!'
        if praise == 'up':
            praise = 'up'
        elif praise == 'down':
            praise = 'down'
        else:
            praise = ''
        new = Comment(article_id=article_id,user_id=user_id,user_name=user_name,date=date,praise=praise,body=body)
        db_session.add(new)
        db_session.commit()
        return u'评论成功！',200
    else:
        return abort(404)


@mod.route('/<int:post_id>/comment')    
def get_comment(post_id):
    comment = Comment.query.filter_by(article_id=post_id).order_by(Comment.date.desc()).all()
    return jsonify([{"id":c.user_id,"body":c.body ,"praise":c.praise}for c in comment])


