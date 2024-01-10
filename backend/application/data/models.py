from application.data.database import db
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager
from sqlalchemy import inspect
import datetime
import jwt
from functools import wraps
from flask import request, jsonify

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(msg="Token is missing")
        try:
            data = jwt.decode(token, "SECRET", algorithms=["HS256"])
            current_user = User.query.filter_by(id=int(data['sub'][0])).first()
        except:
            return jsonify(msg="token is invalid"), 401
        return f(current_user)

    return decorated


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    city = db.Column(db.String, nullable=True)
    profession = db.Column(db.String, nullable=True)
    doj = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow())
    dob = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    last_post = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean(), default=1)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    def encode_auth_token(self,user_id, user_name):
        try :
            payload = {
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=1800),
                'iat' : datetime.datetime.utcnow(),
                'sub' : [user_id, user_name]
            }
            return jwt.encode(
                payload,
                "SECRET",
                algorithm='HS256'
            )
        except Exception as e:
            return e  
class PostItems(db.Model):
    __tablename__ = 'postItems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)
    imagelink = db.Column(db.String, nullable=True)
    likes = db.Column(db.Integer)
    likers = db.Column(db.JSON(), default=[])
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=True)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Followers(db.Model):
    __tablename__ = 'followers'
    user_id = db.Column(db.Integer(), primary_key=True)
    followers = db.Column(db.JSON())

class Following(db.Model):
    __tablename__ = 'following'
    user_id = db.Column(db.Integer(), primary_key=True)
    following = db.Column(db.JSON())
