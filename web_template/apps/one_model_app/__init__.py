from flask import Blueprint

task_app = Blueprint('task', __name__, template_folder='templates')

from . import views
