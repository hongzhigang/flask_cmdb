from . import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # 转换密码用到的库
from flask_login import UserMixin
from datetime import datetime

# from flask_security import RoleMixin,UserMixin#登录和角色需要继承的对象

# 角色<-->用户，多对多关联表
roles_users = db.Table(
    'role_user',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


# 角色表
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role_id:{0}>".format(self.id)


# 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 多对多关联
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "<User_id:{0}>".format(self.id)

    # 这个方法是用于用户登录后返回数据库的ID到session中用来登录
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @property
    def password(self):
        raise AttributeError("密码不允许读取,请使用check_password_hash()进行验证密码")
        return

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


# 邮箱服务器分类
class Emailserver(db.Model):
    __tablename__ = 'emailserver'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    pop = db.Column(db.String(80))
    pop_port = db.Column(db.Integer())
    smtp = db.Column(db.String(80))
    smtp_port = db.Column(db.Integer())
    email = db.relationship('Email', backref='email_server', lazy='dynamic')

    def __repr__(self):
        return "<Emailserver:{0}>".format(self.id)


# 邮箱存放表
class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    description = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    emailserver_id = db.Column(db.Integer, db.ForeignKey('emailserver.id'))

    def __repr__(self):
        return "<Email_id:{0}>".format(self.id)


# 邮箱运营商存放表
class EmailDomain(db.Model):
    __tablename__ = 'emaildomain'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(80))
    web = db.Column(db.String(80))
    operator = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<emaildomain_id:{0}>".format(self.id)


# IP分类,一对多
class Ip_Category(db.Model):
    __tablename__ = 'ip_category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.relationship('Ip_Addres', backref='ip_categorys', lazy='dynamic')

    def __repr__(self):
        return "<ip_class:{0}>".format(self.id)

# IP地址
class Ip_Addres(db.Model):
    __tablename__ = 'ip_addres'
    id = db.Column(db.Integer(), primary_key=True)
    ip = db.Column(db.String(80))
    mac = db.Column(db.String(80))
    hostname = db.Column(db.String(80))
    enable = db.Column(db.Boolean(), default=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_category = db.Column(db.Integer, db.ForeignKey('ip_category.id'))

    def __repr__(self):
        return "<ip_addres:{0}>".format(self.id)
