from flask import Flask , request, render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User,Category,Topic,Post
from flask_login import logout_user, login_required,login_user
from flask_login import current_user
from ..decorators import admin_required, permission_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

@main.route('/home',methods=['GET','POST'])
@main.route('/',methods=['GET','POST'])
def index():
    #user_agent = request.headers.get('User-Agent')
    return render_template('/homepage/home.html')


@main.route('/forum',methods=['GET','POST'])
@login_required
def forum():
    #Bad Logic But Hooks break stuff so sending it
    ## BAD LOGIC
    if current_user.confirmed==False:
        return redirect(url_for('auth.unconfirmed'))
    current_user.ping()
    ## BAD LOGIC

    ##
    #DATABASE CALLS#
    categories=Category.query.all()
    print('\n\n')
    class ForumContext:
        def __init__(self,category,someTopics,numTopics,numPosts,recentPost):
            self.category=category
            self.someTopics=someTopics
            self.numTopics=numTopics
            self.numPosts=numPosts
            self.recentPost=recentPost

    contextList=list()
    for category in categories:
        categoryTopics=Topic.query.filter_by(category_id = category.id).all()
        #Num topics
        context=ForumContext(category,[],0,0,[])

        if(categoryTopics!=[] and categoryTopics!=None):
            context.numTopics=(len(categoryTopics))
            context.someTopics=categoryTopics
        if len(context.someTopics) > 5:
            context.someTopics=context.someTopics[0:5]
        numPosts=(len(Post.query.filter_by(category_id=category.id).all()))
        context.numPosts=numPosts
        if numPosts>0:
            context.recentPost=category.posts.all()[-1].body
            if len(context.recentPost)>55:
                context.recentPost=context.recentPost[0:50]+'...'


        contextList.append(context)
    print(context)

    ## Lets think about how to make this look nicer JSON WISE
    ##
    return render_template('/forums/forum.html',context=contextList)

@main.route('/forum/<category>/<topic>')
@login_required
def forum_category(category,topic):
    categoryContext=Category.query.filter_by(name=category).all()[0]
    topic=Topic.query.filter_by(id=int(topic)).all()[0]
    posts=(topic.posts.filter_by(parent=None)).all()
    # TOO IMPLEMENT REPLYS IN ORDER
    return render_template('/forums/topic.html',topic=topic,category=categoryContext,posts=posts)

#@main.route('/admin')
#@login_required
#@admin_required
#def for_admins_only():
#    return "For administrators!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('/forums/user.html', user=user)
