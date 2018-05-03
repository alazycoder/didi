# -*- coding: utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import os
from myblueprint import blueprint
from user import User


app = Flask(__name__)
app.register_blueprint(blueprint)
app.secret_key = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'
login_manager.init_app(app=app)


# 这个callback函数用于reload User object
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
    # app.run(host='0.0.0.0', port=8001)
