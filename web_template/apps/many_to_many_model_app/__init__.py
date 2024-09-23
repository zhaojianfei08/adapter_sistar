from flask import Blueprint

user_role_app = Blueprint('user_role', __name__, template_folder='templates')

from . import views
