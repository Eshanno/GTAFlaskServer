import os
from app import create_app,db
from app.models import User,Role
from flask_migrate import Migrate

app=create_app('default')
migrate=Migrate(app,db)

def easy():

    db.drop_all()
    db.create_all()
    Role.insert_roles()
    u=User(confirmed=True,email="5eshannon619@gmail.com",username="Ethan",password="Pass")
    db.session.add(u)
    db.session.commit()
    from app import fake
    fake.users(10)
    fake.categories(5)
    fake.topics(10)
    fake.posts(250)
    print("Done")



@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role,easy=easy())


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
