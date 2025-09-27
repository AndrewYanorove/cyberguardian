from flask import render_template, request, jsonify, session
from flask_login import login_required, current_user
from . import education_bp
from datetime import datetime
import json

# База курсов
COURSES = {
    'cybersecurity-basics': {
        'id': 'cybersecurity-basics',
        'title': '🔐 Основы кибербезопасности',
        'description': 'Фундаментальные принципы цифровой безопасности для начинающих',
        'icon': 'bi-shield-check',
        'difficulty': 'beginner',
        'estimated_time': '3 часа',
        'modules': [
            {
                'id': 'module-1',
                'title': 'Введение в кибербезопасность',
                'description': 'Базовые понятия и терминология',
                'lessons': [
                    {
                        'id': 'lesson-1-1',
                        'title': 'Что такое кибербезопасность?',
                        'type': 'text',
                        'duration': 10,
                        'content': [
                            {'type': 'text', 'content': 'Кибербезопасность - это практика защиты систем, сетей и программ от цифровых атак.'},
                            {'type': 'tip', 'content': 'Цель кибератак - получение доступа, изменение или уничтожение конфиденциальной информации.'},
                            {'type': 'warning', 'content': 'Ежегодно компании теряют миллионы долларов из-за кибератак.'}
                        ],
                        'quiz': [
                            {
                                'question': 'Что является основной целью кибербезопасности?',
                                'options': [
                                    'Ускорение работы компьютера',
                                    'Защита цифровых активов',
                                    'Увеличение скорости интернета',
                                    'Улучшение дизайна сайтов'
                                ],
                                'correct': 1,
                                'explanation': 'Правильно! Кибербезопасность защищает цифровые активы от несанкционированного доступа.'
                            }
                        ]
                    },
                    {
                        'id': 'lesson-1-2', 
                        'title': 'Основные типы киберугроз',
                        'type': 'text',
                        'duration': 15,
                        'content': [
                            {'type': 'text', 'content': 'Существует множество типов киберугроз. Вот основные из них:'},
                            {'type': 'warning', 'content': 'Вирусы и malware - вредоносное ПО, которое повреждает системы.'},
                            {'type': 'warning', 'content': 'Фишинг - мошеннические письма, маскирующиеся под легитимные источники.'},
                            {'type': 'warning', 'content': 'DDoS-атаки - перегрузка серверов трафиком.'},
                            {'type': 'tip', 'content': 'Регулярно обновляйте ПО и используйте антивирусы для защиты.'}
                        ],
                        'quiz': [
                            {
                                'question': 'Что такое фишинг?',
                                'options': [
                                    'Вид рыбалки',
                                    'Мошеннические письма для кражи данных', 
                                    'Тип компьютерного вируса',
                                    'Способ шифрования данных'
                                ],
                                'correct': 1,
                                'explanation': 'Верно! Фишинг - это рассылка писем, которые выглядят как от реальных компаний, но предназначены для кражи данных.'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'module-2',
                'title': 'Безопасность паролей',
                'description': 'Создание и управление надежными паролями', 
                'lessons': [
                    {
                        'id': 'lesson-2-1',
                        'title': 'Как создать надежный пароль',
                        'type': 'text',
                        'duration': 20,
                        'content': [
                            {'type': 'text', 'content': 'Пароль - это первая линия защиты ваших учетных записей.'},
                            {'type': 'tip', 'content': 'Используйте длинные пароли (12+ символов) с комбинацией букв, цифр и специальных символов.'},
                            {'type': 'example', 'content': 'Хороший пароль: J8$sK!23pL09@qW\nПлохой пароль: 123456'},
                            {'type': 'warning', 'content': 'Не используйте одинаковые пароли для разных сервисов!'}
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
                                'explanation': 'Правильно! Длинные пароли с разными типами символов наиболее надежны.'
                            }
                        ]
                    }
                ]
            }
        ]
    },
    'phishing-protection': {
        'id': 'phishing-protection',
        'title': '🎣 Защита от фишинга',
        'description': 'Распознавание и защита от мошеннических атак',
        'icon': 'bi-envelope-exclamation', 
        'difficulty': 'beginner',
        'estimated_time': '2 часа',
        'modules': [
            {
                'id': 'module-1',
                'title': 'Основы фишинга',
                'description': 'Что такое фишинг и как он работает',
                'lessons': [
                    {
                        'id': 'lesson-1-1',
                        'title': 'Как распознать фишинг-письмо',
                        'type': 'text', 
                        'duration': 25,
                        'content': [
                            {'type': 'text', 'content': 'Фишинг-письма становятся все более изощренными. Научитесь их распознавать!'},
                            {'type': 'warning', 'content': 'Признаки фишинг-письма: срочные требования, грамматические ошибки, подозрительные ссылки.'},
                            {'type': 'tip', 'content': 'Всегда проверяйте адрес отправителя и URL сайта перед вводом данных.'},
                            {'type': 'example', 'content': 'Настоящий адрес: support@bank.com\nПоддельный: support@b4nk.com'}
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
                                'explanation': 'Верно! Мошенники часто создают искусственную срочность, чтобы вы не успели подумать.'
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

def get_course_progress(course_id):
    """Получить прогресс по курсу"""
    if not current_user.is_authenticated:
        return {'completed': 0, 'total': 0, 'percentage': 0}
    
    from database import db
    from education.models import UserProgress
    
    completed_lessons = UserProgress.query.filter_by(
        user_id=current_user.id,
        course_id=course_id,
        completed=True
    ).count()
    
    total_lessons = 0
    if course_id in COURSES:
        for module in COURSES[course_id]['modules']:
            total_lessons += len(module['lessons'])
    
    return {
        'completed': completed_lessons,
        'total': total_lessons,
        'percentage': int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
    }

@education_bp.route('/')
def education_home():
    """Главная страница обучения"""
    progress_data = {}
    if current_user.is_authenticated:
        for course_id in COURSES:
            progress_data[course_id] = get_course_progress(course_id)
    
    return render_template('education/home.html', 
                         courses=COURSES, 
                         progress=progress_data)

@education_bp.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    """Страница курса с модулями"""
    course = COURSES.get(course_id)
    if not course:
        return "Курс не найден", 404
    
    progress = get_course_progress(course_id)
    
    return render_template('education/course.html', 
                         course=course,
                         progress=progress)

@education_bp.route('/course/<course_id>/lesson/<lesson_id>')
@login_required
def lesson_page(course_id, lesson_id):
    """Страница урока"""
    course = COURSES.get(course_id)
    if not course:
        return "Курс не найден", 404
    
    # Находим урок и модуль
    lesson_data = None
    module_data = None
    for module in course['modules']:
        for lesson in module['lessons']:
            if lesson['id'] == lesson_id:
                lesson_data = lesson
                module_data = module
                break
        if lesson_data:
            break
    
    if not lesson_data:
        return "Урок не найден", 404
    
    # Получаем прогресс
    from education.models import UserProgress
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        course_id=course_id,
        lesson_id=lesson_id
    ).first()
    
    lesson_progress = {
        'completed': progress.completed if progress else False,
        'score': progress.score if progress else 0
    }
    
    return render_template('education/lesson.html',
                         course=course,
                         module=module_data,
                         lesson=lesson_data,
                         progress=lesson_progress)

@education_bp.route('/api/complete-lesson', methods=['POST'])
@login_required
def complete_lesson():
    """Отметить урок как пройденный"""
    try:
        from database import db
        from education.models import UserProgress
        
        data = request.get_json()
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')
        score = data.get('score', 100)
        
        # Сохраняем прогресс
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            course_id=course_id,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                course_id=course_id,
                lesson_id=lesson_id
            )
        
        progress.completed = True
        progress.score = score
        progress.completed_at = datetime.utcnow()
        progress.time_spent = data.get('time_spent', 300)
        
        db.session.add(progress)
        db.session.commit()
        
        # Пересчитываем прогресс курса
        course_progress = get_course_progress(course_id)
        
        return jsonify({
            'success': True,
            'progress': {
                'completed': progress.completed,
                'score': progress.score
            },
            'course_progress': course_progress
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/api/check-answer', methods=['POST'])
@login_required
def check_answer():
    """Проверить ответ на вопрос"""
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')
        question_index = data.get('question_index', 0)
        user_answer = data.get('answer')
        
        # Находим урок и вопрос
        course = COURSES.get(course_id)
        lesson_data = None
        
        for module in course['modules']:
            for lesson in module['lessons']:
                if lesson['id'] == lesson_id:
                    lesson_data = lesson
                    break
            if lesson_data:
                break
        
        if not lesson_data or 'quiz' not in lesson_data:
            return jsonify({'error': 'Тест не найден'}), 404
        
        if question_index >= len(lesson_data['quiz']):
            return jsonify({'error': 'Вопрос не найден'}), 404
        
        question = lesson_data['quiz'][question_index]
        is_correct = int(user_answer) == question['correct']
        
        return jsonify({
            'correct': is_correct,
            'explanation': question['explanation']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500