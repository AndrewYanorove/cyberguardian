from flask import render_template, request, jsonify, session
from flask_login import login_required, current_user
from . import education_bp
from datetime import datetime
# База знаний уроков
LESSONS = {
    'passwords': {
        'id': 'passwords',
        'title': '🔐 Безопасность паролей',
        'description': 'Узнайте как создавать и хранить надежные пароли',
        'icon': 'bi-key',
        'difficulty': 'beginner',
        'estimated_time': '15 мин',
        'content': [
            {
                'type': 'text',
                'content': 'Пароли - это первая линия защиты ваших цифровых данных. Слабый пароль подобен слабому замку на двери.'
            },
            {
                'type': 'warning',
                'content': '80% взломов происходят из-за слабых или украденных паролей'
            },
            {
                'type': 'tip',
                'content': 'Используйте длинные пароли (12+ символов) с комбинацией букв, цифр и специальных символов'
            },
            {
                'type': 'example',
                'content': 'Хороший пароль: J8$sK!23pL09@qW\nПлохой пароль: 123456'
            }
        ],
        'quiz': [
            {
                'question': 'Какой пароль самый надежный?',
                'options': [
                    '123456',
                    'password',
                    'J8$sK!23pL09@qW',
                    'qwerty'
                ],
                'correct': 2,
                'explanation': 'Надежный пароль должен быть длинным и содержать разные типы символов'
            }
        ]
    },
    'phishing': {
        'id': 'phishing',
        'title': '🎣 Фишинг атаки',
        'description': 'Научитесь распознавать мошеннические письма и сайты',
        'icon': 'bi-envelope-exclamation',
        'difficulty': 'beginner',
        'estimated_time': '20 мин',
        'content': [
            {
                'type': 'text',
                'content': 'Фишинг - это вид интернет-мошенничества, целью которого является получение доступа к конфиденциальным данным пользователей.'
            },
            {
                'type': 'warning',
                'content': 'Фишинг-атаки становятся все более изощренными и сложными для распознавания'
            },
            {
                'type': 'tip',
                'content': 'Всегда проверяйте URL сайта и адрес отправителя перед вводом личных данных'
            }
        ],
        'quiz': [
            {
                'question': 'Что должно насторожить в письме?',
                'options': [
                    'Официальный логотип компании',
                    'Срочные требования действий',
                    'Грамотный русский язык',
                    'Контактная информация'
                ],
                'correct': 1,
                'explanation': 'Мошенники часто создают искусственную срочность чтобы вы не успели подумать'
            }
        ]
    },
    'encryption': {
        'id': 'encryption',
        'title': '🔒 Основы шифрования',
        'description': 'Поймите как работает шифрование данных',
        'icon': 'bi-lock',
        'difficulty': 'intermediate',
        'estimated_time': '25 мин',
        'content': [
            {
                'type': 'text',
                'content': 'Шифрование - это процесс преобразования информации в форму, недоступную для понимания без специального ключа.'
            },
            {
                'type': 'tip',
                'content': 'Используйте end-to-end шифрование для важных переписок'
            }
        ]
    },
    'social_engineering': {
        'id': 'social_engineering',
        'title': '👥 Социальная инженерия',
        'description': 'Защититесь от манипуляций',
        'icon': 'bi-people',
        'difficulty': 'intermediate',
        'estimated_time': '30 мин',
        'content': [
            {
                'type': 'text',
                'content': 'Социальная инженерия - это метод манипуляции людьми для получения конфиденциальной информации.'
            }
        ]
    }
}

@education_bp.route('/')
def education_home():
    """Главная страница обучения"""
    progress = session.get('learning_progress', {})
    return render_template('education/home.html', 
                         lessons=LESSONS, 
                         progress=progress)

@education_bp.route('/lesson/<lesson_id>')
@login_required
def lesson(lesson_id):
    """Страница урока"""
    lesson_data = LESSONS.get(lesson_id)
    if not lesson_data:
        return "Урок не найден", 404
    
    # Получаем прогресс пользователя
    progress = session.get('learning_progress', {})
    lesson_progress = progress.get(lesson_id, {'completed': False, 'score': 0})
    
    return render_template('education/lesson.html',
                         lesson=lesson_data,
                         progress=lesson_progress)

@education_bp.route('/api/complete-lesson/<lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    """Отметить урок как пройденный"""
    if lesson_id not in LESSONS:
        return jsonify({'error': 'Урок не найден'}), 404
    
    # Обновляем прогресс в сессии
    progress = session.get('learning_progress', {})
    progress[lesson_id] = {
        'completed': True,
        'completed_at': datetime.now().isoformat(),
        'score': request.json.get('score', 100)
    }
    session['learning_progress'] = progress
    
    # Здесь можно также обновить прогресс в базе данных
    # if current_user.is_authenticated:
    #     current_user.add_completed_lesson(lesson_id)
    
    return jsonify({'success': True, 'progress': progress})

@education_bp.route('/api/check-answer/<lesson_id>', methods=['POST'])
def check_answer(lesson_id):
    """Проверить ответ на вопрос викторины"""
    lesson_data = LESSONS.get(lesson_id)
    if not lesson_data or 'quiz' not in lesson_data:
        return jsonify({'error': 'Тест не найден'}), 404
    
    user_answer = request.json.get('answer')
    question_index = request.json.get('question_index', 0)
    
    if question_index >= len(lesson_data['quiz']):
        return jsonify({'error': 'Вопрос не найден'}), 404
    
    question = lesson_data['quiz'][question_index]
    is_correct = user_answer == question['correct']
    
    return jsonify({
        'correct': is_correct,
        'explanation': question['explanation'] if is_correct else None
    })