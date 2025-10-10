# encryption/__init__.py
from flask import Blueprint

# Создаем blueprint здесь
encryption_bp = Blueprint('encryption', __name__)

from . import routes