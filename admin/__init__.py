
"""
Модуль админ-панели CyberGuardian
Обеспечивает безопасное управление пользователями и системой
"""

from flask import Blueprint

# Создаем blueprint для админ-панели

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

from . import routes

__all__ = ['admin_bp']
