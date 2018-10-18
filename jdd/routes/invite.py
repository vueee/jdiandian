# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from jdd.services.form_validator import UserInfoForm
from jdd.services.database import db_session
from jdd.models.user import User, Subscribe
from flask_login import current_user, login_required
from jdd import app

mod = Blueprint('invite', __name__)


@mod.route('/')
@login_required
def invite():
    return render_template('invite/index.html')

