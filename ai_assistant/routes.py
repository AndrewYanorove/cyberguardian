
from flask import render_template, request, jsonify
from . import ai_bp
from .openai_client import ai_client

@ai_bp.route('/')
def ai_chat():
    """Чат с ИИ-помощником"""
    return render_template('ai_assistant/chat.html')

@ai_bp.route('/ask', methods=['POST'])
def ask_question():
    """Задать вопрос ИИ"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Вопрос не может быть пустым'}), 400
        
        response = ai_client.get_response(question)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/quick-questions')
def quick_questions():
    """Быстрые вопросы для новичков"""
    questions = [
        "Как создать надежный пароль?",
        "Что такое двухфакторная аутентификация?",
        "Как распознать фишинг-письмо?",
        "Какие антивирусы самые надежные?",
        "Как безопасно пользоваться публичным Wi-Fi?",
        "Что делать если взломали аккаунт?",
        "Как настроить VPN?",
        "Что такое социальная инженерия?",
        "Как защитить smartphone от взлома?",
        "Какие привычки повышают кибербезопасность?"
    ]
    return jsonify({'questions': questions})

@ai_bp.route('/demo-info')
def demo_info():
    """Информация о демо-режиме"""
    return jsonify({
        'demo_mode': ai_client.client is None,
        'message': 'Демо-режим активен. Для полного функционала настройте OPENAI_API_KEY.'
    })
