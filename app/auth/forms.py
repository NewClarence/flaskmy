# -*- coding: utf-8 -*-

from wtforms import StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import Required,Email,EqualTo
from flask_wtf import FlaskForm
from ..models import Users

#登录表单
class Login_Form(FlaskForm):
    name=StringField('Name',validators=[Required()])
    password=PasswordField('Password',validators=[Required()])
    submit=SubmitField('Login in')


#注册表单
class Register_Form(FlaskForm):
    name=StringField('Name',validators=[Required()])
    password=PasswordField('Password',validators=[Required(),EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    submit=SubmitField('register')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_name(self, field):
        if Users.query.filter_by(name=field.data).first():
            raise ValidationError('name already in use.')

#修改密码
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[Required()])
    submit = SubmitField('Update Password')

#重设密码
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Reset Password')
