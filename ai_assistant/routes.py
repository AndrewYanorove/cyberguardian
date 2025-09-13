from flask import Blueprint, render_template

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/')
def ai_chat():
    return render_template('ai_assistant/chat.html')