from flask import Blueprint

auth = Blueprint('admin',__name__)

from . import views
