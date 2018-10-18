# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, session, flash,json
from jdd.services.form_validator import UserInfoForm
from jdd.services.database import db_session
from jdd.models.user import User, Tracking, Subscribe
from jdd.models.post import Article
from flask_login import current_user, login_required
from jdd import app, avatars, donates
from qcloud_cos import CosConfig, CosS3Client, CosServiceError, CosClientError
import sys
import logging
import os

mod = Blueprint('dashboard', __name__)

# upload to cos
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDd8Sin6KBSckkkZse1IOJ2b4Sfo49O4va'     
secret_key = 'eDcqunYBd0CKNF1mRNBrT2Uo152rncJt'     
region = 'ap-hongkong'    
token = None   
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  
client = CosS3Client(config)
# response = client.upload_file(Bucket='jdiandian-1257713877', LocalFilePath= file_path, Key=str(user_id) +'/'+ file_name, PartSize=10, MAXThread=10)

@mod.route('/')
@login_required
def user_center():
    return render_template('dashboard/index.html')


@mod.route('/info',methods=['GEt','POST'])
@login_required
def user_info():
    try:
        form = UserInfoForm(request.form)
        uid = int(current_user.get_id())
        info = User.query.get(uid)
        track = Tracking.query.filter_by(user_id=uid).first()
        if request.method == 'POST' and form.validate():
            info.name = form.name.data
            info.summary = form.summary.data
            db_session.commit()
            phone = form.phone.data
            sex = form.sex.data
            birthday = form.birthday.data
            marriage = form.marriage.data
            hobby = ','.join(form.hobby.data)
            if phone or sex or birthday or marriage or hobby:
                track.phone = phone
                track.sex = sex
                track.birthday = birthday
                track.marriage = marriage
                track.hobby = hobby
                db_session.commit()
            flash(u'资料已更新！')
        form.name.data = info.name
        form.summary.data = info.summary
        form.phone.data = track.phone
        form.sex.data = track.sex
        form.birthday.data = track.birthday
        form.marriage.data = track.marriage
        form.hobby.data = track.hobby
        return render_template('dashboard/info.html',form=form)
    except Exception as e:
        return str(e)

#upload avatar
@mod.route('/avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    if request.method == 'POST' and 'file' in request.files:
        uid = current_user.get_id()
        f = request.files['file']
        avatar_path = app.config['UPLOADED_AVATARS_DEST']
        avatar_file_name = uid+'_'+'avatar.jpg'
        if os.path.exists(avatar_path+avatar_file_name):
            os.remove(avatar_path+avatar_file_name)
        s = avatars.save(f,name=avatar_file_name)
        response = client.upload_file(Bucket='jdiandian-1257713877', LocalFilePath= avatar_path+avatar_file_name, Key=str(uid) +'/avatar.jpg', PartSize=10, MAXThread=10)
        flash(u'头像已更新')
    return render_template('dashboard/avatar.html')


#upload donate
@mod.route('/donate', methods=['GET', 'POST'])
@login_required
def upload_donate():
    if request.method == 'POST' and 'file' in request.files:
        uid = current_user.get_id()
        f = request.files['file']
        donate_path = app.config['UPLOADED_DONATES_DEST']
        donate_file_name = uid+'_'+'donate.jpg'
        if os.path.exists(donate_path+donate_file_name):
            os.remove(donate_path+donate_file_name)
        s = donates.save(f,name=donate_file_name)
        response = client.upload_file(Bucket='jdiandian-1257713877', LocalFilePath= donate_path+donate_file_name, Key=str(uid) +'/donate.jpg', PartSize=10, MAXThread=10)
        flash(u'图片已更新')
    return render_template('dashboard/donate.html')

