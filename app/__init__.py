from flask import Flask ,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

bootstrap=Bootstrap()
mail=Mail()
moment=Moment()
db=SQLAlchemy()
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
admin = Admin( name='microblog', template_mode='bootstrap3')



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from .models import User,Post,Topic
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Topic, db.session))

    # Add administrative views here




    ###ROUTES

    #Main
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #Login
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app
