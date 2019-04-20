from flask_migrate import Migrate
from flask_login import UserMixin,AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

##Utilities##

def makeForum():
    def makeCategories(stringList):
        for name in stringList:
            db.session.add(Category(name))
        db.session.commit()
    def makeTopics(tuples):
        topics=[Topic(topicInfo[0],topicInfo[1]) for topicInfo in tuples]
        for x in topics:
            db.session.add(x)
        db.session.commit()
    def makeThreads(tuples):
        thread=[Thread(threadInfo[0],threadInfo[1]) for threadInfo in tuples]
        for x in thread:
            db.session.add(x)
        db.session.commit()

    def makePosts(Posts):
        for x in Posts:
            db.session.add(x)
        db.session.commit()
    user=User.query.all()[0]
    makeCategories(['Ethans Main Category'])
    makeTopics([('TopicName',1)])
    makeThreads([('ThreadName',1)])
    makePosts([Post('My First Post','Here is the main section of the posting',1,user.id,1)])
    post=Post.query.all()[0]
    p=Post()
    p.makeComment('My First Post','Here is the main section of the posting',user.id,post)
    print(p.title)
    db.session.add(p)
    db.session.commit()

#############










class Permission:
    VIEW = 1
    COMMENT = 2
    POST = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    #Perms handled with bitwise operations
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    def remove_permission(self, perm):
        if self.has_permission(perm):
                self.permissions -= perm
    def reset_permissions(self):
        self.permissions = 0
    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {'User': [Permission.VIEW, Permission.COMMENT, Permission.POST],'Moderator': [Permission.VIEW, Permission.COMMENT,Permission.POST, Permission.MODERATE],'Administrator': [Permission.VIEW, Permission.COMMENT,Permission.POST, Permission.MODERATE,Permission.ADMIN],}
        default_role ="User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name






class User(UserMixin,db.Model):
    __tablename__ = 'users'

    ### INTERNAL BOOK KEEPING ###
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    ##############################

    #FORIGEN KEY FOR forum
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    ### STUFF ABOUT THE USER FOR PROFILES ##
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    ############################################

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['GTAVOICERP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return '<User %r>' % self.username

    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)
    def is_administrator(self):
        return self.can(Permission.Administrator)
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    topics = db.relationship('Topic', backref='category', lazy='dynamic')
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    def __init__(self,name):
        self.name=name


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    threads = db.relationship('Thread', backref='topic', lazy='dynamic')
    def __init__(self,name,category_id):
        self.name=name
        self.category_id=category_id

class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    posts = db.relationship('Post', backref='thread', lazy='dynamic')
    def __init__(self,name,topic_id):
        self.name=name
        self.topic_id=topic_id

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    #Self Refrence
    parent_id = db.Column(db.Integer, db.ForeignKey('posts.id'),index=True)
    parent = db.relationship(lambda: Post,remote_side=id, backref='parrent')

    def __init__(self,title='',body='',thread_id=None,author_id=None,category_id=None):
        self.title=title
        self.body=body
        self.thread_id=thread_id
        self.author_id=author_id
        self.category_id=category_id
    def makeComment(self,title,body,author_id,parent):
        self.title=title
        self.body=body
        self.author_id=author_id
        self.parent=parent
        self.thread_id=parrent.thread_id
        self.category_id=parrent.category_id






## MAIN
login_manager.anonymous_user = AnonymousUser
