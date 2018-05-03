# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request, redirect, url_for
from user import User
from forms import LoginForm
from flask_login import login_user, logout_user, login_required
from tools import print_time


def login():
    print_time()
    print "\nroot: login\n"
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        pass_word = form.password.data
        print "账号密码：", user_name, pass_word
        user = User(user_name)
        if user.verify_password(pass_word):
            login_user(user)
            return redirect(request.args.get('next') or url_for('myblueprint.add'))
    return render_template('login.html', form=form)


@login_required
def logout():
    print_time()
    print "\nroot: logout\n"
    logout_user()
    return redirect(url_for('myblueprint.login'))
