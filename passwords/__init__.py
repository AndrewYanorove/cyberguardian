from flask import Blueprint

passwords_bp = Blueprint('passwords', __name__, template_folder='templates', static_folder='static')

from . import routes