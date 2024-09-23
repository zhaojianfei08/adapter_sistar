from flask import Blueprint

opcua_app = Blueprint('opcua', __name__, template_folder='templates')

from . import views
from . import views_addon
