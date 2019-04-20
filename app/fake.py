from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User,Post,Category,Topic,Thread

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
def catagories(count=10):
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
        topic = Topic(name=fake.name(),category_id=category[randint(0,len(category)-1)].id)
        db.session.add(topic)
        db.session.commit()

def threads(count=100):
    fake = Faker()
    category=Category.query.all()
    #Category.query.all()[0].topics.all()
    i=0
    while i<count:
        pickedCategory=category[randint(0,len(category)-1)]
        if(pickedCategory.topics.all()!=[]):
            thread = Thread(name=fake.name(),topic_id=pickedCategory.topics[randint(0,len(pickedCategory.topics.all())-1)].id)
            db.session.add(thread)
            db.session.commit()
            i+=1

def posts(count=100):
    fake = Faker()
    threads=Thread.query.all()
    users = User.query.all()
    #Category.query.all()[0].topics.all()
    i=0
    while i<count:
        pickedThread=threads[randint(0,len(threads)-1)].id
        category=Thread.query.filter_by(id=pickedThread)[0].topic.category.id
        user=users[randint(0,len(users)-1)].id
        post = Post(title=fake.name(),body=fake.text(),thread_id=pickedThread,category_id=category,author_id=user)
        db.session.add(post)
        db.session.commit()
        i+=1
