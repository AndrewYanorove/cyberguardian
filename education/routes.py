# routes.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import random

education_bp = Blueprint('education', __name__, url_prefix='/education')

# Расширенные данные курсов с очень подробным содержанием
COURSES_DATA = {
    "cybersecurity-fundamentals": {
        "id": "cybersecurity-fundamentals",
        "title": "Основы кибербезопасности",
        "description": "Полный курс по основам кибербезопасности для начинающих. Изучите фундаментальные концепции, инструменты и методы защиты информации.",
        "difficulty": "beginner",
        "estimated_time": "40 часов",
        "rating": 4.8,
        "students_count": 15420,
        "instructor": {
            "name": "Александр Петров",
            "role": "Senior Security Engineer",
            "bio": "Опытный специалист по кибербезопасности с 10+ лет опыта. Работал в ведущих IT-компаниях и государственных структурах.",
            "rating": 4.9,
            "students": 45000
        },
        "requirements": [
            "Базовые знания работы с компьютером",
            "Понимание основ интернета",
            "Умение устанавливать программы",
            "Английский язык на уровне чтения документации"
        ],
        "resources": [
            {"name": "Презентации курса", "icon": "file-earmark-ppt"},
            {"name": "Лабораторные работы", "icon": "code-slash"},
            {"name": "Чек-листы безопасности", "icon": "checklist"},
            {"name": "Дополнительные материалы", "icon": "journal-bookmark"}
        ],
        "final_exam": True,
        "modules": [
            {
                "id": "module-1",
                "title": "Введение в кибербезопасность",
                "description": "Основные понятия и принципы кибербезопасности. Угрозы и уязвимости современного цифрового мира.",
                "icon": "shield-check",
                "difficulty": "beginner",
                "estimated_time": "6 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-1-1",
                        "title": "Что такое кибербезопасность?",
                        "description": "Основные концепции и определения. Почему кибербезопасность важна в современном мире.",
                        "duration": 45,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-1-1-1",
                                "title": "Определение кибербезопасности",
                                "description": "Что включает в себя понятие кибербезопасности",
                                "duration": 15,
                                "completed": False,
                                "content": """
                                <h3>Что такое кибербезопасность?</h3>
                                <p>Кибербезопасность — это практика защиты систем, сетей и программ от цифровых атак.</p>
                                <div class="alert alert-info">
                                    <h5><i class="bi bi-info-circle"></i> Ключевые аспекты:</h5>
                                    <ul>
                                        <li><strong>Конфиденциальность</strong> — защита информации от несанкционированного доступа</li>
                                        <li><strong>Целостность</strong> — обеспечение точности и полноты данных</li>
                                        <li><strong>Доступность</strong> — гарантия доступа к информации и системам, когда это необходимо</li>
                                    </ul>
                                </div>
                                """
                            },
                            {
                                "id": "sub-1-1-2",
                                "title": "История развития",
                                "description": "Как развивалась кибербезопасность с течением времени",
                                "duration": 20,
                                "completed": False,
                                "content": """
                                <h3>История кибербезопасности</h3>
                                <div class="timeline">
                                    <div class="timeline-item">
                                        <div class="timeline-date">1970-е</div>
                                        <div class="timeline-content">
                                            <h6>Первые компьютерные вирусы</h6>
                                            <p>Появление первых экспериментальных вирусов Creeper и Reaper</p>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-date">1980-е</div>
                                        <div class="timeline-content">
                                            <h6>Массовое распространение ПК</h6>
                                            <p>Рост числа компьютерных вирусов и первых антивирусных программ</p>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-date">1990-е</div>
                                        <div class="timeline-content">
                                            <h6>Эра интернета</h6>
                                            <p>Появление сетевых атак и первых файрволов</p>
                                        </div>
                                    </div>
                                </div>
                                """
                            }
                        ]
                    },
                    {
                        "id": "lesson-1-2",
                        "title": "Основные типы кибератак",
                        "description": "Изучение наиболее распространенных типов кибератак и методов защиты.",
                        "duration": 60,
                        "completed": False,
                        "quiz": True,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-1-2-1",
                                "title": "Фишинг и социальная инженерия",
                                "description": "Методы манипуляции людьми для получения конфиденциальной информации",
                                "duration": 25,
                                "completed": False,
                                "content": """
                                <h3>Фишинг атаки</h3>
                                <p>Фишинг — это вид интернет-мошенничества, целью которого является получение доступа к конфиденциальным данным пользователей.</p>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-danger">
                                            <div class="card-body">
                                                <h5 class="text-danger"><i class="bi bi-exclamation-triangle"></i> Типы фишинга:</h5>
                                                <ul>
                                                    <li>Массовый фишинг (спам-рассылки)</li>
                                                    <li>Целевой фишинг (spear phishing)</li>
                                                    <li>Фишинг CEO (whaling)</li>
                                                    <li>СМС-фишинг (smishing)</li>
                                                    <li>Голосовой фишинг (vishing)</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5 class="text-success"><i class="bi bi-shield-check"></i> Защита:</h5>
                                                <ul>
                                                    <li>Проверяйте URL адреса</li>
                                                    <li>Не открывайте подозрительные вложения</li>
                                                    <li>Используйте двухфакторную аутентификацию</li>
                                                    <li>Обучайте сотрудников</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """
                            }
                        ]
                    }
                ]
            },
            {
                "id": "module-2",
                "title": "Сетевые технологии и безопасность",
                "description": "Основы сетевых технологий, протоколы и методы защиты сетевой инфраструктуры.",
                "icon": "hdd-network",
                "difficulty": "beginner",
                "estimated_time": "8 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-2-1",
                        "title": "Основы сетевых технологий",
                        "description": "Изучение базовых принципов работы компьютерных сетей.",
                        "duration": 50,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-2-1-1",
                                "title": "Модель OSI и TCP/IP",
                                "description": "Сетевые модели и их уровни",
                                "duration": 30,
                                "completed": False,
                                "content": """
                                <h3>Сетевые модели OSI и TCP/IP</h3>
                                <p>Модель OSI (Open Systems Interconnection) — эталонная модель взаимодействия открытых систем.</p>
                                
                                <div class="table-responsive">
                                    <table class="table table-dark table-striped">
                                        <thead>
                                            <tr>
                                                <th>Уровень OSI</th>
                                                <th>Уровень TCP/IP</th>
                                                <th>Функции</th>
                                                <th>Примеры протоколов</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>Прикладной (7)</td>
                                                <td>Прикладной</td>
                                                <td>Доступ к сетевым службам</td>
                                                <td>HTTP, FTP, SMTP</td>
                                            </tr>
                                            <tr>
                                                <td>Представительский (6)</td>
                                                <td>Прикладной</td>
                                                <td>Представление и шифрование данных</td>
                                                <td>SSL, TLS, JPEG</td>
                                            </tr>
                                            <tr>
                                                <td>Сеансовый (5)</td>
                                                <td>Прикладной</td>
                                                <td>Управление сеансами связи</td>
                                                <td>RPC, NetBIOS</td>
                                            </tr>
                                            <tr>
                                                <td>Транспортный (4)</td>
                                                <td>Транспортный</td>
                                                <td>Надежная передача данных</td>
                                                <td>TCP, UDP</td>
                                            </tr>
                                            <tr>
                                                <td>Сетевой (3)</td>
                                                <td>Интернет</td>
                                                <td>Маршрутизация и логическая адресация</td>
                                                <td>IP, ICMP, ARP</td>
                                            </tr>
                                            <tr>
                                                <td>Канальный (2)</td>
                                                <td>Канальный</td>
                                                <td>Физическая адресация</td>
                                                <td>Ethernet, PPP</td>
                                            </tr>
                                            <tr>
                                                <td>Физический (1)</td>
                                                <td>Физический</td>
                                                <td>Передача битов по среде</td>
                                                <td>Wi-Fi, Ethernet</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                """
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "ethical-hacking": {
        "id": "ethical-hacking",
        "title": "Этичный хакинг и тестирование на проникновение",
        "description": "Освойте методы этичного хакинга для поиска и устранения уязвимостей в системах.",
        "difficulty": "intermediate",
        "estimated_time": "60 часов",
        "rating": 4.9,
        "students_count": 8920,
        "instructor": {
            "name": "Мария Иванова",
            "role": "Penetration Tester",
            "bio": "Сертифицированный этичный хакер с опытом проведения тестов на проникновение для крупных корпораций.",
            "rating": 4.95,
            "students": 28000
        },
        "requirements": [
            "Знание основ сетевых технологий",
            "Базовые навыки работы с Linux",
            "Понимание основ программирования",
            "Знание основ кибербезопасности"
        ],
        "resources": [
            {"name": "Лабораторные среды", "icon": "cpu"},
            {"name": "Инструменты хакинга", "icon": "tools"},
            {"name": "Чек-листы тестирования", "icon": "list-check"},
            {"name": "Примеры отчетов", "icon": "file-earmark-text"}
        ],
        "final_exam": True,
        "modules": [
            {
                "id": "module-1",
                "title": "Введение в этичный хакинг",
                "description": "Правовые и этические аспекты тестирования на проникновение. Методологии и стандарты.",
                "icon": "shield-lock",
                "difficulty": "intermediate",
                "estimated_time": "8 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-1-1",
                        "title": "Правовые основы этичного хакинга",
                        "description": "Юридические аспекты проведения тестов на проникновение.",
                        "duration": 40,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-1-1-1",
                                "title": "Законодательство в сфере ИБ",
                                "description": "Основные законы и нормативные акты",
                                "duration": 25,
                                "completed": False,
                                "content": """
                                <h3>Правовые основы этичного хакинга</h3>
                                <div class="alert alert-warning">
                                    <h5><i class="bi bi-exclamation-triangle"></i> Важно!</h5>
                                    <p>Проведение тестов на проникновение без письменного разрешения является незаконным и может повлечь уголовную ответственность.</p>
                                </div>
                                
                                <h4>Ключевые законодательные акты:</h4>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-info">
                                            <div class="card-body">
                                                <h5 class="text-info">Федеральный закон №187-ФЗ</h5>
                                                <p>"О безопасности критической информационной инфраструктуры РФ"</p>
                                                <small>Определяет требования к защите критически важных объектов</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-info">
                                            <div class="card-body">
                                                <h5 class="text-info">Статья 272 УК РФ</h5>
                                                <p>"Неправомерный доступ к компьютерной информации"</p>
                                                <small>Предусматривает ответственность за несанкционированный доступ</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <h4 class="mt-4">Требования к документации:</h4>
                                <ul>
                                    <li><strong>Договор на оказание услуг</strong> - основной документ</li>
                                    <li><strong>Приказ на проведение тестирования</strong> - внутренний документ заказчика</li>
                                    <li><strong>Scope of Work (SOW)</strong> - описание границ тестирования</li>
                                    <li><strong>Non-Disclosure Agreement (NDA)</strong> - соглашение о неразглашении</li>
                                </ul>
                                """
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "digital-forensics": {
        "id": "digital-forensics",
        "title": "Компьютерная криминалистика и расследование инцидентов",
        "description": "Научитесь проводить цифровые расследования, собирать доказательства и анализировать киберинциденты.",
        "difficulty": "advanced",
        "estimated_time": "80 часов",
        "rating": 4.7,
        "students_count": 5230,
        "instructor": {
            "name": "Дмитрий Смирнов",
            "role": "Digital Forensics Expert",
            "bio": "Эксперт по компьютерной криминалистике с 15-летним опытом работы в правоохранительных органах.",
            "rating": 4.85,
            "students": 15000
        },
        "requirements": [
            "Знание операционных систем Windows/Linux",
            "Понимание файловых систем",
            "Опыт работы с сетевыми технологиями",
            "Знание основ программирования"
        ],
        "resources": [
            {"name": "Форензик инструменты", "icon": "tools"},
            {"name": "Базы данных инцидентов", "icon": "database"},
            {"name": "Шаблоны отчетов", "icon": "file-earmark-medical"},
            {"name": "Кейсы для практики", "icon": "briefcase"}
        ],
        "final_exam": True,
        "modules": [
            {
                "id": "module-1",
                "title": "Основы цифровой криминалистики",
                "description": "Принципы и методологии компьютерной криминалистики. Юридические аспекты сбора доказательств.",
                "icon": "search",
                "difficulty": "advanced",
                "estimated_time": "10 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-1-1",
                        "title": "Принципы цифровой криминалистики",
                        "description": "Фундаментальные принципы и стандарты проведения цифровых расследований.",
                        "duration": 55,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-1-1-1",
                                "title": "Цепочка сохранности доказательств",
                                "description": "Процесс документирования и сохранения цифровых доказательств",
                                "duration": 30,
                                "completed": False,
                                "content": """
                                <h3>Цепочка сохранности доказательств (Chain of Custody)</h3>
                                <p>Цепочка сохранности — это процесс документирования каждого лица, которое имело доступ к доказательствам, с указанием даты, времени и цели доступа.</p>
                                
                                <div class="alert alert-info">
                                    <h5><i class="bi bi-info-circle"></i> Ключевые требования:</h5>
                                    <ul>
                                        <li><strong>Непрерывность</strong> - доказательства всегда должны находиться под контролем</li>
                                        <li><strong>Документирование</strong> - все действия должны быть запротоколированы</li>
                                        <li><strong>Целостность</strong> - доказательства не должны быть изменены</li>
                                        <li><strong>Юридическая сила</strong> - доказательства должны быть допустимы в суде</li>
                                    </ul>
                                </div>
                                
                                <h4>Процесс цепочки сохранности:</h4>
                                <div class="steps">
                                    <div class="step">
                                        <div class="step-number">1</div>
                                        <div class="step-content">
                                            <h6>Обнаружение и изъятие</h6>
                                            <p>Обнаружение цифровых носителей и их безопасное изъятие</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">2</div>
                                        <div class="step-content">
                                            <h6>Упаковка и маркировка</h6>
                                            <p>Правильная упаковка и маркировка с указанием реквизитов</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">3</div>
                                        <div class="step-content">
                                            <h6>Транспортировка</h6>
                                            <p>Безопасная доставка в лабораторию с сопроводительными документами</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">4</div>
                                        <div class="step-content">
                                            <h6>Хранение</h6>
                                            <p>Сохранение в защищенном месте с ограниченным доступом</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">5</div>
                                        <div class="step-content">
                                            <h6>Анализ</h6>
                                            <p>Проведение анализа с использованием сертифицированных инструментов</p>
                                        </div>
                                    </div>
                                </div>
                                """
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

@education_bp.route('/')
def education_home():
    """Главная страница модуля обучения"""
    courses = [
        {
            'id': course_id,
            'title': course_data['title'],
            'description': course_data['description'],
            'difficulty': course_data['difficulty'],
            'rating': course_data['rating'],
            'students_count': course_data['students_count'],
            'estimated_time': course_data['estimated_time'],
            'progress': random.randint(0, 100)
        }
        for course_id, course_data in COURSES_DATA.items()
    ]
    
    return render_template('education/education_home.html', 
                         courses=courses,
                         featured_courses=courses[:3])

@education_bp.route('/course/<course_id>')
def course_page(course_id):
    """Страница курса с подробным содержанием"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404
    
    course_data = COURSES_DATA[course_id]
    
    # Симуляция прогресса пользователя
    progress = {
        'percentage': random.randint(0, 100),
        'completed': random.randint(0, 20),
        'in_progress': random.randint(0, 5),
        'total': 25
    }
    
    # Добавляем информацию о завершении уроков
    for module in course_data['modules']:
        module['completed_lessons'] = random.randint(0, len(module['lessons']))
        for lesson in module['lessons']:
            lesson['completed'] = random.choice([True, False])
            if 'sublessons' in lesson:
                for sublesson in lesson['sublessons']:
                    sublesson['completed'] = random.choice([True, False])
    
    return render_template('education/course.html',
                         course=course_data,
                         progress=progress,
                         course_completed=progress['percentage'] == 100)

@education_bp.route('/course/<course_id>/lesson/<lesson_id>')
def lesson_page(course_id, lesson_id):
    """Страница урока"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404
    
    course_data = COURSES_DATA[course_id]
    lesson_data = None
    module_data = None
    
    # Поиск урока по всем модулям
    for module in course_data['modules']:
        for lesson in module['lessons']:
            if lesson['id'] == lesson_id:
                lesson_data = lesson
                module_data = module
                break
        if lesson_data:
            break
    
    if not lesson_data:
        return "Страница не найдена", 404
    
    # Навигация между уроками
    all_lessons = []
    for module in course_data['modules']:
        all_lessons.extend(module['lessons'])
    
    current_index = next((i for i, lesson in enumerate(all_lessons) if lesson['id'] == lesson_id), -1)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    return render_template('education/lesson.html',
                         course=course_data,
                         module=module_data,
                         lesson=lesson_data,
                         prev_lesson=prev_lesson,
                         next_lesson=next_lesson)

@education_bp.route('/course/<course_id>/quiz/<lesson_id>')
def lesson_quiz(course_id, lesson_id):
    """Страница теста урока"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404
    
    course_data = COURSES_DATA[course_id]
    lesson_data = None
    
    # Поиск урока
    for module in course_data['modules']:
        for lesson in module['lessons']:
            if lesson['id'] == lesson_id:
                lesson_data = lesson
                break
        if lesson_data:
            break
    
    if not lesson_data:
        return "Страница не найдена", 404
    
    # Пример вопросов для теста
    quiz_questions = [
        {
            'id': 1,
            'question': 'Что такое фишинг атака?',
            'type': 'multiple_choice',
            'options': [
                'Атака на физическую инфраструктуру',
                'Метод социальной инженерии для получения конфиденциальной информации',
                'Вид DDoS атаки',
                'Метод шифрования данных'
            ],
            'correct_answer': 1,
            'explanation': 'Фишинг — это метод социальной инженерии, при котором злоумышленник выдает себя за доверенное лицо для получения конфиденциальной информации.'
        },
        {
            'id': 2,
            'question': 'Какие из перечисленных мер помогают защититься от фишинга?',
            'type': 'multiple_select',
            'options': [
                'Использование двухфакторной аутентификации',
                'Проверка URL адресов перед вводом данных',
                'Установка последних обновлений ОС',
                'Обучение сотрудников распознаванию фишинговых писем'
            ],
            'correct_answers': [0, 1, 3],
            'explanation': 'Все перечисленные меры, кроме установки обновлений ОС (которая важна для защиты от других угроз), непосредственно помогают против фишинга.'
        }
    ]
    
    return render_template('education/quiz.html',
                         course=course_data,
                         lesson=lesson_data,
                         questions=quiz_questions)

@education_bp.route('/api/progress/update', methods=['POST'])
def update_progress():
    """API для обновления прогресса обучения"""
    data = request.get_json()
    
    # В реальном приложении здесь было бы обновление в базе данных
    return jsonify({
        'success': True,
        'message': 'Прогресс обновлен',
        'progress': data.get('progress', 0)
    })

@education_bp.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """API для отправки результатов теста"""
    data = request.get_json()
    
    # В реальном приложении здесь была бы проверка ответов и сохранение результатов
    score = random.randint(70, 100)  # Симуляция результата
    
    return jsonify({
        'success': True,
        'score': score,
        'passed': score >= 70,
        'message': 'Тест завершен успешно' if score >= 70 else 'Попробуйте еще раз'
    })

@education_bp.route('/certificates')
def certificates():
    """Страница сертификатов пользователя"""
    certificates_data = [
        {
            'id': 1,
            'course_name': 'Основы кибербезопасности',
            'issue_date': '2024-01-15',
            'expiry_date': '2026-01-15',
            'certificate_url': '#',
            'verified': True
        },
        {
            'id': 2,
            'course_name': 'Этичный хакинг',
            'issue_date': '2024-02-20',
            'expiry_date': '2026-02-20',
            'certificate_url': '#',
            'verified': True
        }
    ]
    
    return render_template('education/certificates.html',
                         certificates=certificates_data)

@education_bp.route('/achievements')
def achievements():
    """Страница достижений пользователя"""
    achievements_data = [
        {
            'id': 1,
            'name': 'Первый шаг',
            'description': 'Завершите первый урок',
            'icon': 'bi-emoji-smile',
            'earned': True,
            'earned_date': '2024-01-10'
        },
        {
            'id': 2,
            'name': 'Упорный ученик',
            'description': 'Завершите 10 уроков',
            'icon': 'bi-award',
            'earned': True,
            'earned_date': '2024-01-20'
        },
        {
            'id': 3,
            'name': 'Эксперт курса',
            'description': 'Завершите все уроки курса',
            'icon': 'bi-trophy',
            'earned': False,
            'earned_date': None
        }
    ]
    
    return render_template('education/achievements.html',
                         achievements=achievements_data)