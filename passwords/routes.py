from flask import Blueprint, render_template

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/')
def password_generator():
    return render_template('passwords/generator.html')