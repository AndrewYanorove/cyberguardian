# routes.py
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)
from datetime import datetime, timedelta
import random

education_bp = Blueprint("education", __name__, url_prefix="/education")

# Расширенные данные курсов с очень подробным содержанием
COURSES_DATA = {
    # В routes.py в разделе COURSES_DATA для "cybersecurity-fundamentals"
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
            "students": 45000,
        },
        "requirements": [
            "Базовые знания работы с компьютером",
            "Понимание основ интернета",
            "Умение устанавливать программы",
            "Английский язык на уровне чтения документации",
        ],
        "resources": [
            {"name": "Презентации курса", "icon": "file-earmark-ppt"},
            {"name": "Лабораторные работы", "icon": "code-slash"},
            {"name": "Чек-листы безопасности", "icon": "checklist"},
            {"name": "Дополнительные материалы", "icon": "journal-bookmark"},
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
                        "quiz": True,  # Тест 1
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
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-2",
                        "title": "Основные угрозы информационной безопасности",
                        "description": "Вирусы, трояны, фишинг и другие киберугрозы современного мира.",
                        "duration": 60,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-1-2-1",
                                "title": "Типы вредоносного ПО",
                                "description": "Классификация вирусов, троянов, ransomware и других угроз",
                                "duration": 30,
                                "completed": False,
                                "content": """
                            <h3>Типы вредоносного программного обеспечения</h3>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="card bg-dark border-danger">
                                        <div class="card-body">
                                            <h5 class="text-danger">Вирусы</h5>
                                            <p>Программы, которые распространяются и заражают другие файлы</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card bg-dark border-warning">
                                        <div class="card-body">
                                            <h5 class="text-warning">Трояны</h5>
                                            <p>Программы, маскирующиеся под легитимное ПО</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-3",
                        "title": "Принципы защиты информации",
                        "description": "Основные методы и подходы к защите цифровых данных.",
                        "duration": 50,
                        "completed": False,
                        "quiz": True,  # Тест 2
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-1-3-1",
                                "title": "Многоуровневая защита",
                                "description": "Принцип защиты в глубину (Defense in Depth)",
                                "duration": 25,
                                "completed": False,
                                "content": """
                            <h3>Многоуровневая защита (Defense in Depth)</h3>
                            <p>Подход, при котором используется несколько уровней защиты для предотвращения атак.</p>
                            <div class="steps">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <div class="step-content">
                                        <h6>Периметровая защита</h6>
                                        <p>Фаерволы, системы обнаружения вторжений</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">2</div>
                                    <div class="step-content">
                                        <h6>Сетевая защита</h6>
                                        <p>Сегментация сети, VPN, шифрование</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">3</div>
                                    <div class="step-content">
                                        <h6>Защита конечных точек</h6>
                                        <p>Антивирусы, EDR системы</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-2",
                "title": "Основы криптографии",
                "description": "Изучение основ шифрования, хэширования и цифровых подписей.",
                "icon": "key",
                "difficulty": "beginner",
                "estimated_time": "8 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-2-1",
                        "title": "Симметричное шифрование",
                        "description": "Принципы работы симметричных алгоритмов шифрования.",
                        "duration": 55,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-2-1-1",
                                "title": "Алгоритм AES",
                                "description": "Advanced Encryption Standard - современный стандарт шифрования",
                                "duration": 30,
                                "completed": False,
                                "content": """
                            <h3>Алгоритм AES (Advanced Encryption Standard)</h3>
                            <p>Симметричный алгоритм блочного шифрования, принятый в качестве стандарта правительством США.</p>
                            <div class="table-responsive">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>Размер ключа</th>
                                            <th>Количество раундов</th>
                                            <th>Уровень безопасности</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>AES-128</td>
                                            <td>10 раундов</td>
                                            <td>Высокий</td>
                                        </tr>
                                        <tr>
                                            <td>AES-192</td>
                                            <td>12 раундов</td>
                                            <td>Очень высокий</td>
                                        </tr>
                                        <tr>
                                            <td>AES-256</td>
                                            <td>14 раундов</td>
                                            <td>Максимальный</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-2-2",
                        "title": "Асимметричное шифрование",
                        "description": "Принципы работы RSA и других асимметричных алгоритмов.",
                        "duration": 65,
                        "completed": False,
                        "quiz": True,  # Тест 3
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-2-2-1",
                                "title": "Алгоритм RSA",
                                "description": "Rivest-Shamir-Adleman - первый практический алгоритм с открытым ключом",
                                "duration": 35,
                                "completed": False,
                                "content": """
                            <h3>Алгоритм RSA</h3>
                            <p>Асимметричный криптографический алгоритм, основанный на вычислительной сложности задачи факторизации больших чисел.</p>
                            <div class="alert alert-info">
                                <h5><i class="bi bi-info-circle"></i> Ключевые этапы:</h5>
                                <ol>
                                    <li>Генерация двух больших простых чисел</li>
                                    <li>Вычисление модуля n = p × q</li>
                                    <li>Вычисление функции Эйлера φ(n)</li>
                                    <li>Выбор открытой экспоненты e</li>
                                    <li>Вычисление секретной экспоненты d</li>
                                </ol>
                            </div>
                            """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-3",
                "title": "Сетевая безопасность",
                "description": "Защита сетевой инфраструктуры и передаваемых данных.",
                "icon": "router",
                "difficulty": "beginner",
                "estimated_time": "7 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-3-1",
                        "title": "Основы сетевой безопасности",
                        "description": "Принципы защиты сетевой инфраструктуры и коммуникаций.",
                        "duration": 50,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-3-1-1",
                                "title": "Сетевые протоколы и уязвимости",
                                "description": "Анализ уязвимостей TCP/IP, DNS, HTTP и других протоколов",
                                "duration": 25,
                                "completed": False,
                                "content": """
                            <h3>Сетевые протоколы и их уязвимости</h3>
                            <p>Понимание основных сетевых протоколов и связанных с ними угроз безопасности.</p>
                            <div class="table-responsive">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>Протокол</th>
                                            <th>Назначение</th>
                                            <th>Основные угрозы</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>TCP/IP</td>
                                            <td>Основной стек протоколов интернета</td>
                                            <td>IP spoofing, TCP hijacking</td>
                                        </tr>
                                        <tr>
                                            <td>DNS</td>
                                            <td>Преобразование доменных имен</td>
                                            <td>DNS spoofing, cache poisoning</td>
                                        </tr>
                                        <tr>
                                            <td>HTTP/HTTPS</td>
                                            <td>Веб-коммуникации</td>
                                            <td>Man-in-the-middle, session hijacking</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-3-2",
                        "title": "Межсетевые экраны и VPN",
                        "description": "Настройка и управление сетевыми экранами и виртуальными частными сетями.",
                        "duration": 60,
                        "completed": False,
                        "quiz": True,  # Тест 4
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-3-2-1",
                                "title": "Типы межсетевых экранов",
                                "description": "Packet filtering, stateful inspection, application-level gateways",
                                "duration": 30,
                                "completed": False,
                                "content": """
                            <h3>Типы межсетевых экранов</h3>
                            <p>Различные подходы к фильтрации сетевого трафика для обеспечения безопасности.</p>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="card bg-dark border-primary">
                                        <div class="card-body">
                                            <h5 class="text-primary">Пакетные фильтры</h5>
                                            <p>Фильтрация на основе IP-адресов и портов</p>
                                            <small>Быстрые, но ограниченные возможности</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-dark border-success">
                                        <div class="card-body">
                                            <h5 class="text-success">Stateful Inspection</h5>
                                            <p>Отслеживание состояния соединений</p>
                                            <small>Более интеллектуальная фильтрация</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-dark border-warning">
                                        <div class="card-body">
                                            <h5 class="text-warning">Application-level</h5>
                                            <p>Анализ на уровне приложений</p>
                                            <small>Высокий уровень безопасности</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-4",
                "title": "Безопасность операционных систем",
                "description": "Защита Windows и Linux систем от кибератак.",
                "icon": "pc-display",
                "difficulty": "beginner",
                "estimated_time": "9 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-4-1",
                        "title": "Безопасность Windows",
                        "description": "Настройка безопасности в операционных системах Windows.",
                        "duration": 70,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-4-1-1",
                                "title": "Групповые политики безопасности",
                                "description": "Настройка политик безопасности в Active Directory",
                                "duration": 35,
                                "completed": False,
                                "content": """
                            <h3>Групповые политики безопасности Windows</h3>
                            <p>Использование групповых политик для централизованного управления безопасностью в доменной среде.</p>
                            <div class="alert alert-info">
                                <h5><i class="bi bi-info-circle"></i> Ключевые политики:</h5>
                                <ul>
                                    <li><strong>Политики паролей</strong> - сложность, срок действия, история</li>
                                    <li><strong>Политики блокировки учетных записей</strong> - пороги и длительность блокировки</li>
                                    <li><strong>Настройки аудита</strong> - отслеживание событий безопасности</li>
                                    <li><strong>Ограничения доступа</strong> - права пользователей и групп</li>
                                </ul>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-4-2",
                        "title": "Безопасность Linux",
                        "description": "Защита Linux-систем и серверов.",
                        "duration": 65,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-4-2-1",
                                "title": "SELinux и AppArmor",
                                "description": "Системы принудительного контроля доступа",
                                "duration": 30,
                                "completed": False,
                                "content": """
                            <h3>SELinux и AppArmor</h3>
                            <p>Системы принудительного контроля доступа для усиления безопасности Linux.</p>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="card bg-dark border-info">
                                        <div class="card-body">
                                            <h5 class="text-info">SELinux</h5>
                                            <p>Security-Enhanced Linux - система принудительного контроля доступа на основе мандатов</p>
                                            <ul>
                                                <li>Типы безопасности</li>
                                                <li>Ролевой доступ</li>
                                                <li>Политики на основе пользователей</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card bg-dark border-success">
                                        <div class="card-body">
                                            <h5 class="text-success">AppArmor</h5>
                                            <p>Application Armor - система контроля доступа на основе путей</p>
                                            <ul>
                                                <li>Профили приложений</li>
                                                <li>Политики на основе путей</li>
                                                <li>Простота настройки</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-4-3",
                        "title": "Управление обновлениями и патчами",
                        "description": "Процессы управления обновлениями безопасности для ОС.",
                        "duration": 45,
                        "completed": False,
                        "quiz": True,  # Тест 5
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-4-3-1",
                                "title": "Цикл управления обновлениями",
                                "description": "Планирование, тестирование и установка обновлений безопасности",
                                "duration": 25,
                                "completed": False,
                                "content": """
                            <h3>Цикл управления обновлениями безопасности</h3>
                            <p>Систематический подход к управлению обновлениями для поддержания безопасности систем.</p>
                            <div class="steps">
                                <div class="step">
                                    <div class="step-number">1</div>
                                    <div class="step-content">
                                        <h6>Оценка</h6>
                                        <p>Анализ критичности обновлений и их влияния на систему</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">2</div>
                                    <div class="step-content">
                                        <h6>Тестирование</h6>
                                        <p>Проверка обновлений в тестовой среде</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">3</div>
                                    <div class="step-content">
                                        <h6>Развертывание</h6>
                                        <p>Поэтапное внедрение обновлений в рабочую среду</p>
                                    </div>
                                </div>
                                <div class="step">
                                    <div class="step-number">4</div>
                                    <div class="step-content">
                                        <h6>Мониторинг</h6>
                                        <p>Контроль результатов установки и устранение проблем</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-5",
                "title": "Социальная инженерия и осведомленность",
                "description": "Защита от методов социальной инженерии и повышение осведомленности пользователей.",
                "icon": "people",
                "difficulty": "beginner",
                "estimated_time": "5 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-5-1",
                        "title": "Методы социальной инженерии",
                        "description": "Распознавание и защита от атак социальной инженерии.",
                        "duration": 55,
                        "completed": False,
                        "quiz": False,
                        "practice": False,
                        "sublessons": [
                            {
                                "id": "sub-5-1-1",
                                "title": "Фишинг и его разновидности",
                                "description": "Идентификация фишинговых атак и защита от них",
                                "duration": 30,
                                "completed": False,
                                "content": """
                            <h3>Фишинг и его разновидности</h3>
                            <p>Фишинг - один из самых распространенных методов социальной инженерии.</p>
                            <div class="table-responsive">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>Тип фишинга</th>
                                            <th>Описание</th>
                                            <th>Методы защиты</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Email фишинг</td>
                                            <td>Массовая рассылка поддельных писем</td>
                                            <td>Проверка отправителя, осторожность с ссылками</td>
                                        </tr>
                                        <tr>
                                            <td>Целевой фишинг</td>
                                            <td>Целенаправленная атака на конкретных лиц</td>
                                            <td>Двухфакторная аутентификация, обучение</td>
                                        </tr>
                                        <tr>
                                            <td>Smishing</td>
                                            <td>Фишинг через SMS сообщения</td>
                                            <td>Не отвечать на подозрительные SMS</td>
                                        </tr>
                                        <tr>
                                            <td>Vishing</td>
                                            <td>Голосовой фишинг по телефону</td>
                                            <td>Верификация звонящего, осторожность с информацией</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-5-2",
                        "title": "Создание культуры безопасности",
                        "description": "Разработка программ повышения осведомленности о безопасности.",
                        "duration": 40,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-5-2-1",
                                "title": "Обучение пользователей",
                                "description": "Эффективные методы обучения сотрудников основам безопасности",
                                "duration": 20,
                                "completed": False,
                                "content": """
                            <h3>Обучение пользователей основам безопасности</h3>
                            <p>Создание эффективной программы обучения для повышения осведомленности о кибербезопасности.</p>
                            <div class="alert alert-success">
                                <h5><i class="bi bi-lightbulb"></i> Ключевые элементы обучения:</h5>
                                <ul>
                                    <li><strong>Регулярность</strong> - постоянное обновление знаний</li>
                                    <li><strong>Практичность</strong> - реальные сценарии и кейсы</li>
                                    <li><strong>Интерактивность</strong> - вовлечение пользователей</li>
                                    <li><strong>Измеримость</strong> - оценка эффективности обучения</li>
                                </ul>
                            </div>
                            <h4>Методы обучения:</h4>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="text-center">
                                        <i class="bi bi-laptop" style="font-size: 2rem; color: var(--cyber-primary);"></i>
                                        <p>Онлайн-курсы</p>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="text-center">
                                        <i class="bi bi-people" style="font-size: 2rem; color: var(--cyber-primary);"></i>
                                        <p>Воркшопы</p>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="text-center">
                                        <i class="bi bi-envelope" style="font-size: 2rem; color: var(--cyber-primary);"></i>
                                        <p>Тестовые фишинг-рассылки</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            }
                        ],
                    },
                ],
            },
        ],
    },
    "ethical-hacking": {
        "id": "ethical-hacking",
        "title": "Этичный хакинг и тестирование на проникновение",
        "description": "Освойте методы этичного хакинга для поиска и устранения уязвимостей в системах. Практический курс с реальными кейсами.",
        "difficulty": "intermediate",
        "estimated_time": "60 часов",
        "rating": 4.9,
        "students_count": 8920,
        "instructor": {
            "name": "Мария Иванова",
            "role": "Penetration Tester",
            "bio": "Сертифицированный этичный хакер с опытом проведения тестов на проникновение для крупных корпораций. CEH, OSCP, CISSP.",
            "rating": 4.95,
            "students": 28000,
        },
        "requirements": [
            "Знание основ сетевых технологий",
            "Базовые навыки работы с Linux",
            "Понимание основ программирования",
            "Знание основ кибербезопасности",
        ],
        "resources": [
            {"name": "Лабораторные среды", "icon": "cpu"},
            {"name": "Инструменты хакинга", "icon": "tools"},
            {"name": "Чек-листы тестирования", "icon": "list-check"},
            {"name": "Примеры отчетов", "icon": "file-earmark-text"},
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
                        "description": "Юридические аспекты проведения тестов на проникновение. Получение разрешений и документация.",
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
                                """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-2",
                        "title": "Методологии тестирования",
                        "description": "OSSTMM, OWASP, NIST и другие стандарты проведения пентестов.",
                        "duration": 55,
                        "completed": False,
                        "quiz": True,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-1-2-1",
                                "title": "Фазы тестирования на проникновение",
                                "description": "Планирование, разведка, сканирование, эксплуатация, пост-эксплуатация, отчетность",
                                "duration": 30,
                                "completed": False,
                                "content": """
                                <h3>Фазы тестирования на проникновение</h3>
                                <div class="steps">
                                    <div class="step">
                                        <div class="step-number">1</div>
                                        <div class="step-content">
                                            <h6>Разведка (Reconnaissance)</h6>
                                            <p>Сбор информации о цели: домены, IP-адреса, сотрудники, технологии</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">2</div>
                                        <div class="step-content">
                                            <h6>Сканирование (Scanning)</h6>
                                            <p>Анализ сетевых служб, поиск уязвимостей, сканирование портов</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">3</div>
                                        <div class="step-content">
                                            <h6>Получение доступа (Gaining Access)</h6>
                                            <p>Эксплуатация уязвимостей для получения контроля над системами</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">4</div>
                                        <div class="step-content">
                                            <h6>Сохрание доступа (Maintaining Access)</h6>
                                            <p>Установка бэкдоров для постоянного доступа к системе</p>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">5</div>
                                        <div class="step-content">
                                            <h6>Сокрытие следов (Covering Tracks)</h6>
                                            <p>Очистка логов и удаление следов присутствия</p>
                                        </div>
                                    </div>
                                </div>
                                """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-2",
                "title": "Сбор информации и разведка",
                "description": "Пассивные и активные методы сбора информации. Инструменты OSINT.",
                "icon": "search",
                "difficulty": "intermediate",
                "estimated_time": "10 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-2-1",
                        "title": "Пассивная разведка (OSINT)",
                        "description": "Методы сбора информации из открытых источников.",
                        "duration": 60,
                        "completed": False,
                        "quiz": True,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-2-1-1",
                                "title": "Инструменты OSINT",
                                "description": "Maltego, theHarvester, Shodan, Google Dorks",
                                "duration": 35,
                                "completed": False,
                                "content": """
                                <h3>Инструменты OSINT для сбора информации</h3>
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-primary">
                                            <div class="card-body text-center">
                                                <h4><i class="bi bi-diagram-3"></i></h4>
                                                <h5>Maltego</h5>
                                                <p>Визуализация связей между различными объектами</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body text-center">
                                                <h4><i class="bi bi-search"></i></h4>
                                                <h5>theHarvester</h5>
                                                <p>Сбор email, поддоменов, IP-адресов</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-warning">
                                            <div class="card-body text-center">
                                                <h4><i class="bi bi-globe"></i></h4>
                                                <h5>Shodan</h5>
                                                <p>Поисковая система для интернета вещей</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """,
                            }
                        ],
                    }
                ],
            },
        ],
    },
    "digital-forensics": {
        "id": "digital-forensics",
        "title": "Компьютерная криминалистика и расследование инцидентов",
        "description": "Научитесь проводить цифровые расследования, собирать доказательства и анализировать киберинциденты. Практический курс с реальными кейсами.",
        "difficulty": "advanced",
        "estimated_time": "80 часов",
        "rating": 4.7,
        "students_count": 5230,
        "instructor": {
            "name": "Дмитрий Смирнов",
            "role": "Digital Forensics Expert",
            "bio": "Эксперт по компьютерной криминалистике с 15-летним опытом работы в правоохранительных органах. Свидетель-эксперт в судебных процессах.",
            "rating": 4.85,
            "students": 15000,
        },
        "requirements": [
            "Знание операционных систем Windows/Linux",
            "Понимание файловых систем",
            "Опыт работы с сетевыми технологиями",
            "Знание основ программирования",
        ],
        "resources": [
            {"name": "Форензик инструменты", "icon": "tools"},
            {"name": "Базы данных инцидентов", "icon": "database"},
            {"name": "Шаблоны отчетов", "icon": "file-earmark-medical"},
            {"name": "Кейсы для практики", "icon": "briefcase"},
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
                                """,
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-2",
                        "title": "Сбор и сохранение доказательств",
                        "description": "Правила изъятия цифровых носителей. Создание образов дисков.",
                        "duration": 70,
                        "completed": False,
                        "quiz": True,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-1-2-1",
                                "title": "Создание битовых образов",
                                "description": "Использование FTK Imager, dd, DC3DD",
                                "duration": 40,
                                "completed": False,
                                "content": """
                                <h3>Создание битовых образов дисков</h3>
                                <p>Битовый образ — точная копия исходного носителя, включая удаленные и неразмеченные области.</p>
                                
                                <h4>Форматы образов:</h4>
                                <div class="table-responsive">
                                    <table class="table table-dark table-striped">
                                        <thead>
                                            <tr>
                                                <th>Формат</th>
                                                <th>Описание</th>
                                                <th>Инструменты</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>RAW (dd)</td>
                                                <td>Сырой битовый образ</td>
                                                <td>dd, DC3DD, FTK Imager</td>
                                            </tr>
                                            <tr>
                                                <td>E01 (Expert Witness)</td>
                                                <td>Сжатый образ с проверкой целостности</td>
                                                <td>FTK Imager, EnCase</td>
                                            </tr>
                                            <tr>
                                                <td>AFF</td>
                                                <td>Advanced Forensic Format</td>
                                                <td>PyFlag, AFFLIB</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                """,
                            }
                        ],
                    },
                ],
            },
            {
                "id": "module-2",
                "title": "Анализ файловых систем",
                "description": "Исследование FAT, NTFS, ext4 и других файловых систем. Восстановление удаленных данных.",
                "icon": "hdd",
                "difficulty": "advanced",
                "estimated_time": "15 часов",
                "completed_lessons": 0,
                "lessons": [
                    {
                        "id": "lesson-2-1",
                        "title": "Анализ файловой системы NTFS",
                        "description": "MFT, ADS, журнал изменений и другие особенности NTFS.",
                        "duration": 80,
                        "completed": False,
                        "quiz": True,
                        "practice": True,
                        "sublessons": [
                            {
                                "id": "sub-2-1-1",
                                "title": "Master File Table (MFT)",
                                "description": "Структура и анализ главной файловой таблицы",
                                "duration": 45,
                                "completed": False,
                                "content": """
                                <h3>Анализ Master File Table (MFT)</h3>
                                <p>MFT — основная структура файловой системы NTFS, содержащая информацию о всех файлах и каталогах.</p>
                                
                                <h4>Структура MFT записи:</h4>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-info">
                                            <div class="card-body">
                                                <h5>Заголовок MFT</h5>
                                                <ul>
                                                    <li>Сигнатура "FILE"</li>
                                                    <li>Смещение атрибутов</li>
                                                    <li>Флаги записи</li>
                                                    <li>Размер записи</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5>Атрибуты MFT</h5>
                                                <ul>
                                                    <li>$STANDARD_INFORMATION</li>
                                                    <li>$FILE_NAME</li>
                                                    <li>$DATA</li>
                                                    <li>$BITMAP</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """,
                            }
                        ],
                    }
                ],
            },
        ],
    },
}


@education_bp.route("/course/<course_id>/module/<module_id>")
def module_detail(course_id, module_id):
    """Детальная страница модуля"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]
    module_data = None

    for module in course_data["modules"]:
        if module["id"] == module_id:
            module_data = module
            break

    if not module_data:
        return "Страница не найдена", 404

    return render_template(
        "education/module_detail.html", course=course_data, module=module_data
    )


@education_bp.route("/course/<course_id>/lesson/<lesson_id>/complete", methods=["POST"])
def complete_lesson(course_id, lesson_id):
    """API для завершения урока"""
    # В реальном приложении здесь было бы сохранение в базу данных
    return jsonify(
        {"success": True, "message": "Урок завершен", "lesson_id": lesson_id}
    )


@education_bp.route("/course/<course_id>/final-exam/submit", methods=["POST"])
def submit_final_exam(course_id):
    """API для отправки финального экзамена"""
    data = request.get_json()

    # Симуляция проверки экзамена
    score = random.randint(60, 100)
    passed = score >= 70

    return jsonify(
        {
            "success": True,
            "score": score,
            "passed": passed,
            "message": (
                "Экзамен сдан успешно"
                if passed
                else "Экзамен не сдан, попробуйте еще раз"
            ),
        }
    )


@education_bp.route("/course/<course_id>/certificate")
def course_certificate(course_id):
    """Страница сертификата курса"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]

    # Симуляция данных сертификата
    certificate_data = {
        "id": f"CERT-{random.randint(1000, 9999)}",
        "course_name": course_data["title"],
        "student_name": "Иван Иванов",  # В реальном приложении из сессии/БД
        "completion_date": datetime.now().strftime("%d.%m.%Y"),
        "score": random.randint(85, 98),
    }

    return render_template(
        "education/certificate.html", course=course_data, certificate=certificate_data
    )


@education_bp.route("/")
def education_home():
    """Главная страница модуля обучения"""
    courses = [
        {
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "difficulty": course_data["difficulty"],
            "rating": course_data["rating"],
            "students_count": course_data["students_count"],
            "estimated_time": course_data["estimated_time"],
            "progress": random.randint(0, 100),
        }
        for course_id, course_data in COURSES_DATA.items()
    ]

    return render_template(
        "education/education_home.html", courses=courses, featured_courses=courses[:3]
    )


@education_bp.route("/course/<course_id>")
def course_page(course_id):
    """Страница курса с подробным содержанием"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]

    # Симуляция прогресса пользователя
    progress = {
        "percentage": random.randint(0, 100),
        "completed": random.randint(0, 20),
        "in_progress": random.randint(0, 5),
        "total": 25,
    }

    # Добавляем информацию о завершении уроков
    for module in course_data["modules"]:
        module["completed_lessons"] = random.randint(0, len(module["lessons"]))
        for lesson in module["lessons"]:
            lesson["completed"] = random.choice([True, False])
            if "sublessons" in lesson:
                for sublesson in lesson["sublessons"]:
                    sublesson["completed"] = random.choice([True, False])

    return render_template(
        "education/course.html",
        course=course_data,
        progress=progress,
        course_completed=progress["percentage"] == 100,
    )


@education_bp.route("/course/<course_id>/lesson/<lesson_id>")
def lesson_page(course_id, lesson_id):
    """Страница урока"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]
    lesson_data = None
    module_data = None

    # Поиск урока по всем модулям
    for module in course_data["modules"]:
        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                lesson_data = lesson
                module_data = module
                break
        if lesson_data:
            break

    if not lesson_data:
        return "Страница не найдена", 404

    # Навигация между уроками
    all_lessons = []
    for module in course_data["modules"]:
        all_lessons.extend(module["lessons"])

    current_index = next(
        (i for i, lesson in enumerate(all_lessons) if lesson["id"] == lesson_id), -1
    )
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = (
        all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    )

    return render_template(
        "education/lesson.html",
        course=course_data,
        module=module_data,
        lesson=lesson_data,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
    )


@education_bp.route("/course/<course_id>/quiz/<lesson_id>")
def lesson_quiz(course_id, lesson_id):
    """Страница теста урока"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]
    lesson_data = None

    # Поиск урока
    for module in course_data["modules"]:
        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                lesson_data = lesson
                break
        if lesson_data:
            break

    if not lesson_data:
        return "Страница не найдена", 404

    # Генерация вопросов в зависимости от курса
    if course_id == "ethical-hacking":
        quiz_questions = [
            {
                "id": 1,
                "question": "Что такое OSINT?",
                "type": "multiple_choice",
                "options": [
                    "Операционная система интернета",
                    "Сбор информации из открытых источников",
                    "Метод шифрования данных",
                    "Тип сетевой атаки",
                ],
                "correct_answer": 1,
                "explanation": "OSINT (Open Source Intelligence) — сбор и анализ информации из общедоступных источников.",
            },
            {
                "id": 2,
                "question": "Какие инструменты используются для пассивной разведки?",
                "type": "multiple_select",
                "options": ["Maltego", "Nmap", "theHarvester", "Metasploit", "Shodan"],
                "correct_answers": [0, 2, 4],
                "explanation": "Maltego, theHarvester и Shodan используются для пассивной разведки, тогда как Nmap и Metasploit — для активного сканирования и эксплуатации.",
            },
        ]
    elif course_id == "digital-forensics":
        quiz_questions = [
            {
                "id": 1,
                "question": "Что такое цепочка сохранности доказательств?",
                "type": "multiple_choice",
                "options": [
                    "Метод хранения цифровых носителей",
                    "Процесс документирования доступа к доказательствам",
                    "Тип шифрования данных",
                    "Способ передачи информации",
                ],
                "correct_answer": 1,
                "explanation": "Цепочка сохранности — это процесс документирования каждого лица, которое имело доступ к доказательствам.",
            },
            {
                "id": 2,
                "question": "Какие форматы образов дисков используются в криминалистике?",
                "type": "multiple_select",
                "options": ["RAW (dd)", "JPEG", "E01 (Expert Witness)", "MP4", "AFF"],
                "correct_answers": [0, 2, 4],
                "explanation": "RAW, E01 и AFF — стандартные форматы для создания криминалистических образов дисков.",
            },
        ]
    else:
        # Общие вопросы для кибербезопасности
        quiz_questions = [
            {
                "id": 1,
                "question": "Что такое фишинг атака?",
                "type": "multiple_choice",
                "options": [
                    "Атака на физическую инфраструктуру",
                    "Метод социальной инженерии для получения конфиденциальной информации",
                    "Вид DDoS атаки",
                    "Метод шифрования данных",
                ],
                "correct_answer": 1,
                "explanation": "Фишинг — это метод социальной инженерии, при котором злоумышленник выдает себя за доверенное лицо для получения конфиденциальной информации.",
            }
        ]

    return render_template(
        "education/quiz.html",
        course=course_data,
        lesson=lesson_data,
        questions=quiz_questions,
    )


@education_bp.route("/api/progress/update", methods=["POST"])
def update_progress():
    """API для обновления прогресса обучения"""
    data = request.get_json()

    # В реальном приложении здесь было бы обновление в базе данных
    return jsonify(
        {
            "success": True,
            "message": "Прогресс обновлен",
            "progress": data.get("progress", 0),
        }
    )


@education_bp.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """API для отправки результатов теста"""
    data = request.get_json()

    # В реальном приложении здесь была бы проверка ответов и сохранение результатов
    score = random.randint(70, 100)  # Симуляция результата

    return jsonify(
        {
            "success": True,
            "score": score,
            "passed": score >= 70,
            "message": "Тест завершен успешно" if score >= 70 else "Попробуйте еще раз",
        }
    )


@education_bp.route("/certificates")
def certificates():
    """Страница сертификатов пользователя"""
    certificates_data = [
        {
            "id": 1,
            "course_name": "Основы кибербезопасности",
            "issue_date": "2024-01-15",
            "expiry_date": "2026-01-15",
            "certificate_url": "#",
            "verified": True,
        },
        {
            "id": 2,
            "course_name": "Этичный хакинг",
            "issue_date": "2024-02-20",
            "expiry_date": "2026-02-20",
            "certificate_url": "#",
            "verified": True,
        },
        {
            "id": 3,
            "course_name": "Компьютерная криминалистика",
            "issue_date": "2024-03-10",
            "expiry_date": "2026-03-10",
            "certificate_url": "#",
            "verified": True,
        },
    ]

    return render_template(
        "education/certificates.html", certificates=certificates_data
    )


@education_bp.route("/all-courses")
def all_courses():
    """Страница со всеми курсами"""
    courses = [
        {
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "difficulty": course_data["difficulty"],
            "rating": course_data["rating"],
            "students_count": course_data["students_count"],
            "estimated_time": course_data["estimated_time"],
            "progress": random.randint(0, 100),
            "instructor": course_data["instructor"],
        }
        for course_id, course_data in COURSES_DATA.items()
    ]

    return render_template("education/all_courses.html", courses=courses)


@education_bp.route("/course/<course_id>/final-exam")
def final_exam(course_id):
    """Финальный экзамен курса"""
    if course_id not in COURSES_DATA:
        return "Страница не найдена", 404

    course_data = COURSES_DATA[course_id]

    # Генерация вопросов для финального экзамена
    exam_questions = generate_final_exam_questions(course_id)

    return render_template(
        "education/final_exam.html", course=course_data, questions=exam_questions
    )


def generate_final_exam_questions(course_id):
    """Генерация вопросов для финального экзамена"""
    # Реализация генерации вопросов в зависимости от курса
    if course_id == "ethical-hacking":
        return [
            {
                "id": 1,
                "question": "Опишите этапы тестирования на проникновение согласно методологии OWASP",
                "type": "essay",
                "points": 20,
            }
            # ... другие вопросы
        ]
    # ... аналогично для других курсов
    return []


@education_bp.route("/achievements")
def achievements():
    """Страница достижений пользователя"""
    achievements_data = [
        {
            "id": 1,
            "name": "Первый шаг",
            "description": "Завершите первый урок",
            "icon": "bi-emoji-smile",
            "earned": True,
            "earned_date": "2024-01-10",
        },
        {
            "id": 2,
            "name": "Упорный ученик",
            "description": "Завершите 10 уроков",
            "icon": "bi-award",
            "earned": True,
            "earned_date": "2024-01-20",
        },
        {
            "id": 3,
            "name": "Эксперт курса",
            "description": "Завершите все уроки курса",
            "icon": "bi-trophy",
            "earned": False,
            "earned_date": None,
        },
        {
            "id": 4,
            "name": "Мастер этичного хакинга",
            "description": "Завершите курс этичного хакинга",
            "icon": "bi-shield-lock",
            "earned": False,
            "earned_date": None,
        },
        {
            "id": 5,
            "name": "Эксперт криминалистики",
            "description": "Завершите курс компьютерной криминалистики",
            "icon": "bi-search",
            "earned": False,
            "earned_date": None,
        },
    ]

    return render_template(
        "education/achievements.html", achievements=achievements_data
    )
