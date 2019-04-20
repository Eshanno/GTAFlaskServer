import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask_admin import Admin
class Config():

    SECRET_KEY=os.environ['SECRET_FLASK']
    EMAIL_HEADER = '[GTA Voice RP]'
    EMAIL_ADDR = '5eshannon619@gmail.com'
    GTAVOICERP_ADMIN = '5eshannon619@gmail.com'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_ADMIN_SWATCH = 'cerulean'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI =\
    'sqlite:///' + os.path.join(basedir, 'deveopmentData.sqlite')

class TestingConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI =\
    'sqlite:///' + os.path.join(basedir, 'test.sqlite')

class ProductionConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,

'default': DevelopmentConfig
}
