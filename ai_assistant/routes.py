from flask import render_template, request, jsonify, session
from . import ai_bp
from .gigachat_client import gigachat_client as ai_client
from .chat_manager import chat_manager
from .utils import SecurityUtils, ResponseFormatter
import time
import uuid

def get_user_id():
    """Генерирует ID пользователя на основе сессии"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

@ai_bp.route('/')
def ai_chat():
    """Главная страница чата"""
    return render_template('ai_assistant/chat.html')

@ai_bp.route('/chats', methods=['GET'])
def get_chats():
    """Получить все чаты пользователя"""
    try:
        user_id = get_user_id()
        chats = chat_manager.get_user_chats(user_id)
        return jsonify({'chats': chats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/chats', methods=['POST'])
def create_chat():
    """Создать новый чат"""
    try:
        user_id = get_user_id()
        chat_id = chat_manager.create_chat(user_id, "Новый чат")
        
        return jsonify({
            'success': True, 
            'chat_id': chat_id,
            'message': 'Чат создан'
        })
    except Exception as e:
        print(f"❌ Ошибка создания чата: {e}")
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Получить конкретный чат"""
    try:
        user_id = get_user_id()
        chat = chat_manager.get_chat(chat_id)
        
        if not chat or chat['user_id'] != user_id:
            return jsonify({'error': 'Чат не найден'}), 404
        
        return jsonify({'chat': chat})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """Удалить чат"""
    try:
        user_id = get_user_id()
        success = chat_manager.delete_chat(user_id, chat_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Чат не найден'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/chats/<chat_id>/rename', methods=['POST'])
def rename_chat(chat_id):
    """Переименовать чат"""
    try:
        data = request.get_json()
        new_title = data.get('title', '').strip()
        
        if not new_title:
            return jsonify({'error': 'Название не может быть пустым'}), 400
        
        success = chat_manager.rename_chat(chat_id, new_title)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Чат не найден'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/chats/<chat_id>/ask', methods=['POST'])
def ask_question(chat_id):
    """Задать вопрос в конкретном чате"""
    try:
        # Проверка частоты запросов
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
        
        # Проверяем доступ к чату
        user_id = get_user_id()
        chat = chat_manager.get_chat(chat_id)
        
        if not chat or chat['user_id'] != user_id:
            return jsonify({'error': 'Чат не найден'}), 404
        
        # Очистка и проверка ввода
        sanitized_question = SecurityUtils.sanitize_input(question)
        
        # Добавляем вопрос пользователя в чат
        chat_manager.add_message(chat_id, 'user', sanitized_question)
        
        # Получаем ответ от AI
        start_time = time.time()
        response = ai_client.get_response(sanitized_question)
        processing_time = time.time() - start_time
        
        # Добавляем ответ AI в чат
        chat_manager.add_message(chat_id, 'assistant', response)
        
        # Форматируем ответ для отображения
        formatted_response = ResponseFormatter.format_ai_response(response)
        
        return jsonify({
            'response': formatted_response,
            'processing_time': round(processing_time, 2),
            'chat_id': chat_id
        })
        
    except Exception as e:
        print(f"❌ Ошибка в ask_question: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

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