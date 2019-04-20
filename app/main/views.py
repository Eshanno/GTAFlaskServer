from flask import Flask , request, render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User
from flask_login import logout_user, login_required,login_user
from flask_login import current_user
from ..decorators import admin_required, permission_required
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
    return render_template('/forums/forum.html')

@main.route('/forum/<category>/<topic>')
@login_required
def forum_category(category,topic):
    return category+topic

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('/forums/user.html', user=user)
