import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY=os.environ['SECRET_FLASK']

    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


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
