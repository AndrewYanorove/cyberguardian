from flask import Blueprint, render_template

education_bp = Blueprint('education', __name__)

@education_bp.route('/')
def education_home():
    return render_template('education/home.html')