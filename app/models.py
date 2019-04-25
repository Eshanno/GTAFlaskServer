from flask_migrate import Migrate
from flask_login import UserMixin,AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
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


    def makePosts(Posts):
        for x in Posts:
            db.session.add(x)
        db.session.commit()
    user=User.query.all()[0]
    makeCategories(['Ethans Main Category'])
    makeTopics([('TopicName',1)])

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
    def __str__(self):
        return "{} #{}".format(self.username,self.id)
    ### INTERNAL BOOK KEEPING ###
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    ##############################

    #FORIGEN KEY FOR forum
    posts = db.relationship('Post', backref='author', lazy='dynamic' ,cascade="all")

    ### STUFF ABOUT THE USER FOR PROFILES ##
    name = db.Column(db.String(64))
    profile_picture=db.Column(db.Text())
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
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
        return self.can(Permission.ADMIN)
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

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
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
    def __str__(self):
        return "{} #{}".format(self.name,self.id)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    topics = db.relationship('Topic',single_parent=True, backref=backref('category'),  cascade="all",lazy='dynamic')
    posts = db.relationship('Post', single_parent=True, backref=backref('category'),cascade="all", lazy='dynamic')



class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    posts = db.relationship('Post', single_parent=True,backref=backref('topic'),cascade="all", lazy='dynamic')

    def __str__(self):
        return ('{} #{}'.format(self.name,str(self.id)))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    #Self Refrence
    parent_id = db.Column(db.Integer, db.ForeignKey('posts.id'),index=True)
    comments = db.relationship(lambda: Post,remote_side=id,single_parent=True, backref=backref('parent'),cascade="all",)
    def __str__(self):
        return "{} #{},by:{}".format(self.title,self.id,self.author_id)


    def makeComment(self,title,body,author_id,parent):
        self.title=title
        self.body=body
        self.author_id=author_id
        self.comments=parent
        self.topic_id=parent.topic_id
        self.category_id=parent.category_id






## MAIN
login_manager.anonymous_user = AnonymousUser
