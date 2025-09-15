from flask import Blueprint

passwords_bp = Blueprint('passwords', __name__)

from . import routes