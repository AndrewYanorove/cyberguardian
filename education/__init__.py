from flask import Blueprint

education_bp = Blueprint('education', __name__)

# Импорты должны быть после создания Blueprint
from . import routes