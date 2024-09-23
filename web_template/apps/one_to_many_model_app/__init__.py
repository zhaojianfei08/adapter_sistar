from flask import Blueprint

author_book_app = Blueprint('author_book', __name__, template_folder='templates')

from . import views
