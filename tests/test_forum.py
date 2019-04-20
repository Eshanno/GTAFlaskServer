import unittest
from app.models import User,Permission,Role,AnonymousUser,db,Category,Topic,Thread,Post


class ForumTestCase(unittest.TestCase):
    def test_forum(self):
        category=Category()
        category.name="Main Category"
        category.id=1

        db.session.add(category)
