# -*- coding: utf-8 -*-

import sys
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .. import db
from ..models import Users
from ..email import send_email
from .forms import Login_Form,Register_Form

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login',methods=['GET','POST'])
def login():
        form=Login_Form()
        if form.validate_on_submit():
            user=Users.query.filter_by(name=form.name.data).first()
 	    if user is not None and user.check_password(form.password.data):
		login_user(user)
		flash('登录成功')
                return  render_template('auth/success.html',name=form.name.data)
	    else:
		flash('用户或密码错误')
                return render_template('auth/login.html',form=form)

#用户登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        user=Users(name=form.name.data,email=form.email.data)
	user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
	token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        #flash('注册成功')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html',form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
