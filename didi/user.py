from datetime import datetime
from flask_login import UserMixin
import uuid
from db import select_db


class User(UserMixin):
    def __init__(self, username=None, password=None,id=None):
        self.username = None
        self.password = None
        self.id = None
        if username:
            self.username = username
            self.password, self.id = self.get_password_uid_by_username()
        elif id:
            self.id = id
            self.username, self.password = self.get_username_password_by_id()

    def get_password_uid_by_username(self):
        sql = "select pass_word,uid from user where user_name='%s'" % self.username
        res = select_db(sql)
        if res:
            return res[0][0], res[0][1]
        else:
            return None, None

    def get_username_password_by_id(self):
        sql = "select user_name,pass_word from user where uid='%s'" % self.id
        res = select_db(sql)
        if res:
            return res[0][0], res[0][1]
        else:
            return None, None

    def verify_password(self, password):
        if self.password is None:
            return False
        return self.password == password

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        return User(id=user_id)
