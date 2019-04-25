from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import logout_user, login_required,login_user
from flask_login import current_user

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_administrator():
            return True
        else:
            return False

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_administrator():
            return True
        else:
            return False
class CategoryView(ModelView):
    form_excluded_columns = ['topics', 'posts']

class TopicView(ModelView):
    form_excluded_columns = ['posts', 'posts']

class PostView(ModelView):
    form_excluded_columns = ['comments', 'posts','parent']
class UserView(ModelView):
    can_create = False
