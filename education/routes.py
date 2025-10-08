from flask import render_template, request, jsonify, session
from flask_login import login_required, current_user
from . import education_bp
from datetime import datetime
import json

# Расширенная база курсов с очень подробным содержанием
COURSES = {
    'cybersecurity-basics': {
        'id': 'cybersecurity-basics',
        'title': '🔐 Основы кибербезопасности',
        'description': 'Полный курс по фундаментальным принципам цифровой безопасности для начинающих. От основ до продвинутых техник защиты.',
        'icon': 'bi-shield-check',
        'difficulty': 'beginner',
        'estimated_time': '15 часов',
        'category': 'Безопасность',
        'level': 'Начальный',
        'rating': 4.8,
        'students_count': 12500,
        'final_exam': {
            'title': 'Финальный экзамен по основам кибербезопасности',
            'duration': 60,
            'passing_score': 70,
            'questions': [
                {
                    'question': 'Какой из перечисленных методов является наиболее эффективным против фишинговых атак?',
                    'options': [
                        'Использование простых паролей',
                        'Двухфакторная аутентификация',
                        'Отключение антивируса',
                        'Использование одного пароля для всех сервисов'
                    ],
                    'correct': 1,
                    'explanation': 'Двухфакторная аутентификация значительно усложняет доступ злоумышленников к вашим аккаунтам даже при утечке паролей.'
                },
                {
                    'question': 'Что означает аббревиатура VPN?',
                    'options': [
                        'Virtual Private Network',
                        'Very Protected Network', 
                        'Virtual Public Network',
                        'Verified Private Network'
                    ],
                    'correct': 0,
                    'explanation': 'VPN (Virtual Private Network) - это технология, создающая защищенное соединение поверх публичной сети.'
                },
                {
                    'question': 'Какой тип атаки использует социальную инженерию?',
                    'options': [
                        'DDoS атака',
                        'Фишинг',
                        'SQL инъекция',
                        'XSS атака'
                    ],
                    'correct': 1,
                    'explanation': 'Фишинг использует методы социальной инженерии для манипуляции людьми и получения конфиденциальной информации.'
                },
                {
                    'question': 'Что такое ботнет?',
                    'options': [
                        'Антивирусная программа',
                        'Сеть зараженных компьютеров',
                        'Тип шифрования',
                        'Метод резервного копирования'
                    ],
                    'correct': 1,
                    'explanation': 'Ботнет - это сеть компьютеров, зараженных вредоносным ПО и управляемых злоумышленником для проведения атак.'
                },
                {
                    'question': 'Какой протокол шифрования самый безопасный для Wi-Fi?',
                    'options': [
                        'WEP',
                        'WPA',
                        'WPA2',
                        'WPA3'
                    ],
                    'correct': 3,
                    'explanation': 'WPA3 - самый современный и безопасный протокол шифрования для беспроводных сетей.'
                }
            ]
        },
        'modules': [
            {
                'id': 'module-1',
                'title': 'Введение в кибербезопасность',
                'description': 'Базовые понятия, терминология и принципы цифровой безопасности. Изучите фундаментальные концепции защиты информации.',
                'order': 1,
                'lessons': [
                    {
                        'id': 'lesson-1-1',
                        'title': 'Что такое кибербезопасность и почему это важно?',
                        'type': 'text',
                        'duration': 45,
                        'order': 1,
                        'content': [
                            {'type': 'text', 'content': 'Кибербезопасность - это практика защиты систем, сетей, программ и данных от цифровых атак. Эти атаки обычно направлены на получение доступа, изменение или уничтожение конфиденциальной информации, вымогательство денег у пользователей или прерывание нормального процесса бизнеса.'},
                            {'type': 'tip', 'content': 'Современные кибератаки становятся все более изощренными и могут нанести значительный ущерб как отдельным пользователям, так и крупным корпорациям.'},
                            {'type': 'warning', 'content': 'По данным исследований, ущерб от киберпреступности к 2025 году может достигнуть 10.5 триллионов долларов ежегодно.'},
                            {'type': 'text', 'content': 'Основные цели кибербезопасности (триада CIA):'},
                            {'type': 'text', 'content': '• 🔒 Конфиденциальность - защита данных от несанкционированного доступа'},
                            {'type': 'text', 'content': '• ✅ Целостность - обеспечение точности и полноты данных'},
                            {'type': 'text', 'content': '• ⚡ Доступность - гарантия доступа к данным и системам, когда это необходимо'}
                        ],
                        'quiz': [
                            {
                                'question': 'Какая из перечисленных целей НЕ является основной целью кибербезопасности?',
                                'options': [
                                    'Конфиденциальность',
                                    'Скорость обработки данных',
                                    'Целостность данных', 
                                    'Доступность систем'
                                ],
                                'correct': 1,
                                'explanation': 'Скорость обработки данных важна для производительности, но не является основной целью кибербезопасности.'
                            },
                            {
                                'question': 'Какой годовой ущерб прогнозируется от киберпреступности к 2025 году?',
                                'options': [
                                    '1 миллиард долларов',
                                    '500 миллиардов долларов',
                                    '10.5 триллионов долларов',
                                    '100 миллионов долларов'
                                ],
                                'correct': 2,
                                'explanation': 'Согласно исследованиям, ущерб может достигнуть 10.5 триллионов долларов, что делает кибербезопасность критически важной.'
                            }
                        ]
                    },
                    {
                        'id': 'lesson-1-2', 
                        'title': 'История развития киберугроз и эволюция защиты',
                        'type': 'text',
                        'duration': 60,
                        'order': 2,
                        'content': [
                            {'type': 'text', 'content': 'Эволюция киберугроз прошла длинный путь от простых вирусов до сложных целевых атак. Понимание истории помогает предсказать будущие тенденции.'},
                            {'type': 'text', 'content': '📅 1970-1980-е годы: Зарождение кибербезопасности'},
                            {'type': 'text', 'content': '• 1971: Первый компьютерный вирус Creeper'},
                            {'type': 'text', 'content': '• 1986: Вирус Brain - первый вирус для ПК'},
                            {'type': 'text', 'content': '• 1988: Червь Морриса - первая масштабная сетевая атака'},
                            {'type': 'text', 'content': '📅 1990-е годы: Эра массовых атак'},
                            {'type': 'text', 'content': '• 1995: Макровирусы для Microsoft Office'},
                            {'type': 'text', 'content': '• 1999: Вирус Melissa - массовая рассылка по email'},
                            {'type': 'tip', 'content': 'История показывает, что киберугрозы постоянно эволюционируют, и защита должна быть проактивной.'}
                        ],
                        'quiz': [
                            {
                                'question': 'В каком году появился первый компьютерный вирус?',
                                'options': [
                                    '1965',
                                    '1971',
                                    '1980',
                                    '1990'
                                ],
                                'correct': 1,
                                'explanation': 'Первый компьютерный вирус Creeper появился в 1971 году в сети ARPANET.'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 'module-2',
                'title': 'Безопасность паролей и аутентификация',
                'description': 'Создание и управление надежными паролями, современные методы аутентификации и защита учетных записей.',
                'order': 2,
                'lessons': [
                    {
                        'id': 'lesson-2-1',
                        'title': 'Искусство создания надежных паролей',
                        'type': 'text',
                        'duration': 55,
                        'order': 1,
                        'content': [
                            {'type': 'text', 'content': 'Пароль - это первая и часто единственная линия защиты ваших учетных записей. Слабые пароли являются причиной 80% успешных взломов.'},
                            {'type': 'tip', 'content': '🎯 Характеристики надежного пароля:'},
                            {'type': 'text', 'content': '• 📏 Длина не менее 12 символов (рекомендуется 16+)'},
                            {'type': 'text', 'content': '• 🔤 Комбинация заглавных и строчных букв'},
                            {'type': 'text', 'content': '• 🔢 Наличие цифр и специальных символов'},
                            {'type': 'example', 'content': '✅ Пример надежного пароля: J8$sK!23pL09@qW\n❌ Пример слабого пароля: 123456 или password'},
                            {'type': 'warning', 'content': '🚨 Никогда не используйте одинаковые пароли для разных сервисов! При утечке одного пароля злоумышленники получат доступ ко всем вашим аккаунтам.'}
                        ],
                        'quiz': [
                            {
                                'question': 'Какая минимальная длина рекомендуется для надежного пароля?',
                                'options': [
                                    '6 символов',
                                    '8 символов', 
                                    '12 символов',
                                    '16 символов'
                                ],
                                'correct': 2,
                                'explanation': '12 символов считается минимальной длиной для обеспечения достаточной безопасности в современных условиях.'
                            }
                        ]
                    }
                ]
            }
        ]
    },
    'phishing-protection': {
        'id': 'phishing-protection',
        'title': '🎣 Защита от фишинга и социальной инженерии',
        'description': 'Полное руководство по распознаванию и защите от мошеннических атак. Научитесь выявлять фишинг и защищать свои данные.',
        'icon': 'bi-envelope-exclamation', 
        'difficulty': 'beginner',
        'estimated_time': '12 часов',
        'category': 'Социальная инженерия',
        'level': 'Начальный',
        'rating': 4.9,
        'students_count': 8900,
        'final_exam': {
            'title': 'Финальный тест по защите от фишинга',
            'duration': 45,
            'passing_score': 75,
            'questions': [
                {
                    'question': 'Какой из этих признаков наиболее точно указывает на фишинг-письмо?',
                    'options': [
                        'Наличие логотипа компании',
                        'Срочные требования действий',
                        'Грамотная орфография',
                        'Официальный адрес отправителя'
                    ],
                    'correct': 1,
                    'explanation': 'Срочные требования действий - классический признак фишинга, так как мошенники создают искусственное давление.'
                }
            ]
        },
        'modules': [
            {
                'id': 'module-1',
                'title': 'Основы фишинга и социальной инженерии',
                'description': 'Что такое фишинг, как он работает и почему он эффективен. Изучите механизмы социальной инженерии.',
                'order': 1,
                'lessons': [
                    {
                        'id': 'lesson-1-1',
                        'title': 'Как распознать фишинг-письмо: полное руководство',
                        'type': 'text', 
                        'duration': 55,
                        'order': 1,
                        'content': [
                            {'type': 'text', 'content': 'Фишинг-письма становятся все более изощренными и сложными для распознавания. Научитесь выявлять их по ключевым признакам.'},
                            {'type': 'warning', 'content': '🚩 Срочные требования - "Ваш аккаунт будет заблокирован через 24 часа!" или "Срочно обновите данные!"'},
                            {'type': 'warning', 'content': '🚩 Грамматические ошибки - профессиональные компании тщательно проверяют тексты перед отправкой'},
                            {'type': 'warning', 'content': '🚩 Подозрительные ссылки - наведите курсор на ссылку, чтобы увидеть реальный URL (не кликайте!)'},
                            {'type': 'tip', 'content': '💡 Всегда проверяйте адрес отправителя и URL сайта перед вводом каких-либо данных.'}
                        ],
                        'quiz': [
                            {
                                'question': 'Что должно насторожить вас в полученном письме?',
                                'options': [
                                    'Официальный логотип компании в шапке',
                                    'Срочные требования немедленных действий',
                                    'Наличие контактной информации в подвале', 
                                    'Профессиональное оформление письма'
                                ],
                                'correct': 1,
                                'explanation': 'Мошенники часто создают искусственную срочность, чтобы вы не успели критически оценить ситуацию.'
                            }
                        ]
                    }
                ]
            }
        ]
    },
    'network-security': {
        'id': 'network-security',
        'title': '🌐 Безопасность сетей и Wi-Fi',
        'description': 'Защита домашних и корпоративных сетей, безопасное использование Wi-Fi, VPN и современных сетевых технологий.',
        'icon': 'bi-wifi',
        'difficulty': 'intermediate', 
        'estimated_time': '18 часов',
        'category': 'Сетевая безопасность',
        'level': 'Средний',
        'rating': 4.7,
        'students_count': 6700,
        'final_exam': {
            'title': 'Экзамен по безопасности сетей',
            'duration': 75,
            'passing_score': 80,
            'questions': [
                {
                    'question': 'Какой протокол шифрования является наиболее безопасным для Wi-Fi сетей?',
                    'options': [
                        'WEP',
                        'WPA',
                        'WPA2',
                        'WPA3'
                    ],
                    'correct': 3,
                    'explanation': 'WPA3 - самый современный и безопасный протокол шифрования для беспроводных сетей.'
                }
            ]
        },
        'modules': [
            {
                'id': 'module-1',
                'title': 'Основы сетевой безопасности',
                'description': 'Принципы защиты сетевой инфраструктуры, настройка безопасных сетей и защита от сетевых атак.',
                'order': 1,
                'lessons': [
                    {
                        'id': 'lesson-1-1',
                        'title': 'Защита домашней Wi-Fi сети: полное руководство',
                        'type': 'text',
                        'duration': 80,
                        'order': 1,
                        'content': [
                            {'type': 'text', 'content': 'Домашняя Wi-Fi сеть - это входная дверь в вашу цифровую жизнь. Неправильная настройка может привести к серьезным последствиям, включая кражу данных и несанкционированный доступ.'},
                            {'type': 'tip', 'content': '🎯 Ключевые шаги для защиты Wi-Fi:'},
                            {'type': 'text', 'content': '1. 🔐 Измените пароль администратора роутера по умолчанию'},
                            {'type': 'text', 'content': '2. 🛡️ Используйте WPA3 или WPA2 шифрование (никогда WEP!)'},
                            {'type': 'text', 'content': '3. 🔑 Создайте надежный пароль для Wi-Fi сети (12+ символов)'},
                            {'type': 'warning', 'content': '🚨 Никогда не используйте открытые Wi-Fi сети для передачи конфиденциальной информации без VPN!'}
                        ],
                        'quiz': [
                            {
                                'question': 'Какой протокол шифрования следует использовать для максимальной безопасности Wi-Fi?',
                                'options': [
                                    'WEP',
                                    'WPA',
                                    'WPA2', 
                                    'WPA3'
                                ],
                                'correct': 3,
                                'explanation': 'WPA3 обеспечивает современное шифрование и защиту от атак перебора паролей.'
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
    
    percentage = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
    
    return {
        'completed': completed_lessons,
        'total': total_lessons,
        'percentage': percentage
    }

def get_user_course_completion(course_id):
    """Проверить, завершен ли курс пользователем - используем только user_progress"""
    if not current_user.is_authenticated:
        return False
    
    # Вместо отдельной таблицы проверяем, завершены ли все уроки курса
    progress = get_course_progress(course_id)
    return progress['percentage'] == 100

def find_module_for_lesson(course_id, lesson_id):
    """Найти модуль для урока"""
    course = COURSES.get(course_id)
    if course:
        for module in course['modules']:
            for lesson in module['lessons']:
                if lesson['id'] == lesson_id:
                    return module['id']
    return None

@education_bp.route('/')
def education_home():
    """Главная страница обучения"""
    progress_data = {}
    completion_data = {}
    
    if current_user.is_authenticated:
        for course_id in COURSES:
            progress_data[course_id] = get_course_progress(course_id)
            completion_data[course_id] = get_user_course_completion(course_id)
    
    return render_template('education/home.html', 
                         courses=COURSES, 
                         progress=progress_data,
                         completions=completion_data)

@education_bp.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    """Страница курса с модулями"""
    course = COURSES.get(course_id)
    if not course:
        return "Курс не найден", 404
    
    progress = get_course_progress(course_id)
    course_completed = get_user_course_completion(course_id)
    
    return render_template('education/course.html', 
                         course=course,
                         progress=progress,
                         course_completed=course_completed)

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

@education_bp.route('/course/<course_id>/final-exam')
@login_required
def final_exam(course_id):
    """Страница финального экзамена"""
    course = COURSES.get(course_id)
    if not course or 'final_exam' not in course:
        return "Экзамен не найден", 404
    
    # Проверяем, завершены ли все уроки
    progress = get_course_progress(course_id)
    if progress['percentage'] < 100:
        return "Завершите все уроки перед сдачей экзамена", 403
    
    # Проверяем, не сдан ли уже экзамен
    if get_user_course_completion(course_id):
        return "Экзамен уже сдан", 403
    
    return render_template('education/final_exam.html',
                         course=course,
                         exam=course['final_exam'])

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
        time_spent = data.get('time_spent', 300)
        
        # Находим модуль для этого урока
        module_id = find_module_for_lesson(course_id, lesson_id)
        if not module_id:
            return jsonify({'error': 'Модуль не найден для данного урока'}), 400
        
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
                module_id=module_id,
                lesson_id=lesson_id
            )
        
        progress.completed = True
        progress.score = score
        progress.completed_at = datetime.utcnow()
        progress.time_spent = time_spent
        
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

@education_bp.route('/api/submit-final-exam', methods=['POST'])
@login_required
def submit_final_exam():
    """Обработать результаты финального экзамена"""
    try:
        from database import db
        from education.models import UserProgress
        
        data = request.get_json()
        course_id = data.get('course_id')
        answers = data.get('answers', [])
        
        course = COURSES.get(course_id)
        if not course or 'final_exam' not in course:
            return jsonify({'error': 'Курс или экзамен не найден'}), 404
        
        # Проверяем ответы
        exam_questions = course['final_exam']['questions']
        correct_answers = 0
        
        for i, user_answer in enumerate(answers):
            if i < len(exam_questions) and int(user_answer) == exam_questions[i]['correct']:
                correct_answers += 1
        
        score = int((correct_answers / len(exam_questions)) * 100)
        
        # Создаем фиктивный урок для отметки завершения экзамена
        exam_lesson_id = f"{course_id}-final-exam"
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            course_id=course_id,
            lesson_id=exam_lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                course_id=course_id,
                module_id=f"{course_id}-exam-module",
                lesson_id=exam_lesson_id
            )
        
        progress.completed = True
        progress.score = score
        progress.completed_at = datetime.utcnow()
        progress.time_spent = course['final_exam']['duration'] * 60
        
        db.session.add(progress)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': len(exam_questions),
            'passed': score >= course['final_exam']['passing_score']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/api/complete-course', methods=['POST'])
@login_required
def complete_course():
    """Отметить курс как завершенный"""
    try:
        from database import db
        from education.models import UserProgress
        
        data = request.get_json()
        course_id = data.get('course_id')
        
        course = COURSES.get(course_id)
        if not course:
            return jsonify({'error': 'Курс не найден'}), 404
        
        # Создаем запись о завершении курса как специальный урок
        course_completion_id = f"{course_id}-course-completion"
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            course_id=course_id,
            lesson_id=course_completion_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                course_id=course_id,
                module_id=f"{course_id}-completion-module",
                lesson_id=course_completion_id
            )
        
        progress.completed = True
        progress.score = 100
        progress.completed_at = datetime.utcnow()
        progress.time_spent = 0
        
        db.session.add(progress)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Курс успешно завершен!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/achievements')
@login_required
def achievements():
    """Страница достижений пользователя"""
    completed_courses = []
    total_courses = len(COURSES)
    completed_count = 0
    
    # Собираем информацию о завершенных курсах
    for course_id in COURSES:
        if get_user_course_completion(course_id):
            completed_count += 1
            completed_courses.append({
                'course_id': course_id,
                'title': COURSES[course_id]['title'],
                'final_score': 100
            })
    
    return render_template('education/achievements.html',
                         completed_courses=completed_courses,
                         total_courses=total_courses,
                         completed_count=completed_count,
                         courses=COURSES,
                         completions={course_id: get_user_course_completion(course_id) for course_id in COURSES},
                         progress={course_id: get_course_progress(course_id) for course_id in COURSES})
