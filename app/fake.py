from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User,Post,Category,Topic

def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),username=fake.user_name(),password='password',confirmed=True,name=fake.name(),location=fake.city(),about_me=fake.text(),member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
def categories(count=10):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        c = Category(name=fake.name())
        db.session.add(c)
        db.session.commit()


def topics(count=100):
    fake = Faker()
    category=Category.query.all()
    user_count = User.query.count()
    for i in range(count):
        topic = Topic(name=fake.name(),category_id=category[randint(-1,len(category)-1)].id)
        db.session.add(topic)
        db.session.commit()

def posts(count=100):
    fake = Faker()
    topics=Topic.query.all()
    users = User.query.all()
    #Category.query.all()[0].topics.all()
    i=0
    while i<count:
        pickedTopic=topics[randint(0,len(topics)-1)].id
        category=Topic.query.filter_by(id=pickedTopic)[0].category.id
        user=users[randint(-1,len(users)-1)].id
        post = Post(title=fake.name(),body=fake.text(),topic_id=pickedTopic,category_id=category,author_id=user)
        db.session.add(post)
        db.session.commit()
        i+=1


def commentPosts(count=100):
    fake = Faker()
    topics=Topic.query.all()
    users = User.query.all()
    posts = Post.query.all()

    while i<count:
        db.session.add(post)
        db.session.commit()
        i+=1
