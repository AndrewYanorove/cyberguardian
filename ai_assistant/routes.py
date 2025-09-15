from flask import render_template, request, jsonify
from . import ai_bp
import openai
import os

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def get_response(self, message, context=None):
        """Получение ответа от ИИ"""
        try:
            if not self.api_key:
                return "API ключ не настроен. Пожалуйста, добавьте OPENAI_API_KEY в .env файл"
            
            # Формируем промпт с контекстом кибербезопасности
            system_prompt = """Ты эксперт по кибербезопасности. Отвечай на вопросы четко, профессионально, 
            но доступным языком. Давай практические советы и рекомендации. Если вопрос не по теме, 
            вежливо отклони ответ."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message['content'].strip()
            
        except Exception as e:
            return f"Ошибка при обращении к ИИ: {str(e)}"

ai_assistant = AIAssistant()

@ai_bp.route('/')
def ai_chat():
    """Чат с ИИ-помощником"""
    return render_template('ai_assistant/chat.html')

@ai_bp.route('/ask', methods=['POST'])
def ask_question():
    """Задать вопрос ИИ"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Вопрос не может быть пустым'}), 400
        
        response = ai_assistant.get_response(question)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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