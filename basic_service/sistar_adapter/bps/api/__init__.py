from flask.blueprints import Blueprint

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

from . import views