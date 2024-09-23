from flask import Blueprint

student_app = Blueprint('student', __name__, template_folder='templates')

from . import views
