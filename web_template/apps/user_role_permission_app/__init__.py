from flask import Blueprint

user_role_permisson_app = Blueprint('user_role_permiss', __name__, template_folder='templates')

from . import views
from . import views_addon

