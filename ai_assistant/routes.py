from flask import render_template, request, jsonify, session
from . import ai_bp
from .gigachat_client import gigachat_client as ai_client
from .utils import SecurityUtils, ResponseFormatter
import time
import json

@ai_bp.route('/')
def ai_chat():
    """Чат с ИИ-помощником по кибербезопасности"""
    return render_template('ai_assistant/chat.html')

@ai_bp.route('/ask', methods=['POST'])
def ask_question():
    """Задать вопрос ИИ с оптимизацией и защитой"""
    try:
        # Проверка частоты запросов (не чаще 1 запроса в 2 секунды)
        if 'last_request' in session:
            elapsed = time.time() - session['last_request']
            if elapsed < 2:
                return jsonify({
                    'error': 'Слишком частые запросы. Подождите немного.',
                    'retry_after': 2
                }), 429
        
        session['last_request'] = time.time()
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Неверный формат данных'}), 400
            
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Вопрос не может быть пустым'}), 400
        
        if len(question) > 1000:
            return jsonify({'error': 'Слишком длинный вопрос (максимум 1000 символов)'}), 400
        
        # Очистка и проверка ввода
        sanitized_question = SecurityUtils.sanitize_input(question)
        
        # Проверка на спам/флуд
        if any(word in sanitized_question.lower() for word in [
            'http://', 'https://', '[url]', 'спам', 'реклама', 'купить', 'продать'
        ]):
            return jsonify({'error': 'Сообщение содержит запрещенные элементы'}), 400
        
        # Получаем ответ от AI
        start_time = time.time()
        response = ai_client.get_response(sanitized_question)
        processing_time = time.time() - start_time
        
        # Форматируем ответ
        formatted_response = ResponseFormatter.format_ai_response(response)
        
        # Сохраняем в историю (ограниченный размер)
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        chat_entry = {
            'question': sanitized_question,
            'response': response,
            'timestamp': time.time(),
            'processing_time': round(processing_time, 2)
        }
        
        session['chat_history'].append(chat_entry)
        
        # Ограничиваем историю последними 20 сообщениями
        if len(session['chat_history']) > 20:
            session['chat_history'] = session['chat_history'][-20:]
        
        return jsonify({
            'response': formatted_response,
            'processing_time': processing_time,
            'complexity': SecurityUtils.detect_question_complexity(sanitized_question)
        })
        
    except Exception as e:
        print(f"❌ Ошибка в ask_question: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

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

@ai_bp.route('/usage-stats')
def get_usage_stats():
    """Статистика использования токенов"""
    try:
        stats = ai_client.get_usage_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Очистка кэша AI"""
    try:
        ai_client.clear_cache()
        return jsonify({'success': True, 'message': 'Кэш очищен'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/history', methods=['GET'])
def get_chat_history():
    """Получить историю чата"""
    try:
        history = session.get('chat_history', [])
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """Очистить историю чата"""
    try:
        session.pop('chat_history', None)
        return jsonify({'success': True, 'message': 'История очищена'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/demo-info')
def demo_info():
    """Информация о режиме работы"""
    return jsonify({
        'provider': 'GigaChat',
        'optimized': True,
        'caching_enabled': True,
        'message': 'Используется оптимизированный GigaChat API с кэшированием'
    })