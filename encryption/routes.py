from flask import Blueprint, render_template

encryption_bp = Blueprint('encryption', __name__)

@encryption_bp.route('/')
def encryption_tools():
    return render_template('encryption/tools.html')