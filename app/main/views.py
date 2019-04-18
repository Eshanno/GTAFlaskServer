from flask import Flask , request, render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User

@main.route('/home',methods=['GET','POST'])
@main.route('/',methods=['GET','POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('/homepage/home.html')

@main.route('/forum',methods=['GET','POST'])
def forum():
    return render_template('/forums/forum.html')
