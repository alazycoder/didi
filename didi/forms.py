# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField("登录")


# 定义的表单都需要继承自FlaskForm
class LogoutForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    submit = SubmitField("退出登录")