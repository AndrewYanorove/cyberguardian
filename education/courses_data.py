from datetime import datetime

# Основные данные курсов
COURSES_DATA = {
    "cybersecurity-for-teens": {
        "id": "cybersecurity-for-teens",
        "title": "Кибербезопасность для подростков",
        "description": "Увлекательный курс по основам цифровой безопасности. Научись защищать свои данные и распознавать интернет-угрозы.",
        "difficulty": "beginner",
        "estimated_time": "1 минута",
        "rating": 4.9,
        "students_count": 25420,
        "instructor": {
            "name": "Анна Смирнова",
            "role": "Детский психолог и эксперт по кибербезопасности",
            "bio": "Специалист по цифровой грамотности детей и подростков. Автор методик безопасного поведения в интернете.",
            "rating": 4.95,
            "students": 35000,
        },
        "requirements": [
            "Базовые навыки работы с компьютером",
            "Умение пользоваться интернетом",
            "Возраст от 12 лет"
        ],
        "resources": [
            {"name": "Интерактивные задания", "icon": "play-btn"},
            {"name": "Чек-листы безопасности", "icon": "checklist"},
            {"name": "Памятки для родителей", "icon": "journal-bookmark"},
            {"name": "Игровые тесты", "icon": "controller"},
        ],
        "final_exam": True,
        "video_intro": "https://rutube.ru/video/b88c977bb0a5abf66cd4d0e959970249/?r=plwd",  # Пример видео
        "modules": [
            {
                "id": "module-1",
                "title": "Надежные пароли - твой первый щит",
                "description": "Узнай, как создавать и хранить надежные пароли, которые невозможно взломать.",
                "icon": "key",
                "difficulty": "beginner",
                "estimated_time": "5 часов",
                "completed_lessons": 0,
                "video_overview": "https://rutube.ru/video/b88c977bb0a5abf66cd4d0e959970249/?r=plwd",
                "lessons": [
                    {
                        "id": "lesson-1-1",
                        "title": "Почему пароли так важны?",
                        "description": "Узнай, зачем нужны пароли и почему их нужно защищать.",
                        "duration": 25,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "video_url": "https://rutube.ru/video/b88c977bb0a5abf66cd4d0e959970249/?r=plwd",
                        "sublessons": [
                            {
                                "id": "sub-1-1-1",
                                "title": "Что такое пароль и зачем он нужен",
                                "description": "Основные понятия о паролях",
                                "duration": 10,
                                "completed": False,
                                "content": """
                                <h3>🔐 Что такое пароль?</h3>
                                <p>Пароль - это как ключ от твоего цифрового дома. Он защищает твои:</p>
                                
                                <div class="row mt-4">
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-primary">
                                            <div class="card-body text-center">
                                                <i class="bi bi-phone" style="font-size: 2rem; color: var(--cyber-primary);"></i>
                                                <h5 class="mt-2">Соцсети</h5>
                                                <p class="mb-0">ВКонтакте, TikTok, Instagram</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body text-center">
                                                <i class="bi bi-laptop" style="font-size: 2rem; color: var(--cyber-success);"></i>
                                                <h5 class="mt-2">Игры</h5>
                                                <p class="mb-0">Minecraft, Roblox, Steam</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="alert alert-info mt-4">
                                    <h5><i class="bi bi-lightbulb"></i> Интересный факт:</h5>
                                    <p>Каждую секунду хакеры пытаются взломать 300 паролей по всему миру!</p>
                                </div>
                                """
                            },
                            {
                                "id": "sub-1-1-2",
                                "title": "Что будет, если пароль украдут?",
                                "description": "Последствия кражи паролей",
                                "duration": 15,
                                "completed": False,
                                "content": """
                                <h3>🚨 Опасность кражи паролей</h3>
                                
                                <div class="row text-center mt-4">
                                    <div class="col-md-4 mb-3">
                                        <div class="cyber-badge cyber-badge-danger p-3">
                                            <i class="bi bi-currency-dollar" style="font-size: 2rem;"></i>
                                            <h6 class="mt-2">Кража денег</h6>
                                            <small>Могут украсть деньги с игровых счетов</small>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="cyber-badge cyber-badge-warning p-3">
                                            <i class="bi bi-chat-dots" style="font-size: 2rem;"></i>
                                            <h6 class="mt-2">Рассылка спама</h6>
                                            <small>От твоего имени могут писать друзьям</small>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="cyber-badge cyber-badge-info p-3">
                                            <i class="bi bi-shield-exclamation" style="font-size: 2rem;"></i>
                                            <h6 class="mt-2">Потеря аккаунта</h6>
                                            <small>Можно потерять доступ к играм и соцсетям</small>
                                        </div>
                                    </div>
                                </div>

                                <div class="practice-preview mt-4">
                                    <h5><i class="bi bi-star"></i> Практическое задание:</h5>
                                    <p>Представь, что у тебя украли пароль от любимой игры. Что бы ты почувствовал?</p>
                                    <textarea class="form-control bg-dark text-light" rows="3" placeholder="Напиши свои мысли..."></textarea>
                                    <button class="btn btn-cyber mt-2" onclick="saveThoughts()">Сохранить</button>
                                </div>
                                """
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-2",
                        "title": "Создаем супер-пароль",
                        "description": "Научись создавать пароли, которые невозможно взломать.",
                        "duration": 35,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "video_url": "https://www.youtube.com/embed/3O8eS2XcI2Q",
                        "sublessons": [
                            {
                                "id": "sub-1-2-1",
                                "title": "Правила создания надежного пароля",
                                "description": "Из чего должен состоять хороший пароль",
                                "duration": 20,
                                "completed": False,
                                "content": """
                                <h3>🛡️ Создаем неуязвимый пароль</h3>
                                
                                <div class="row mt-4">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5 class="text-success">✅ Что должно быть:</h5>
                                                <ul>
                                                    <li>Не менее 12 символов</li>
                                                    <li>Заглавные и строчные буквы</li>
                                                    <li>Цифры</li>
                                                    <li>Специальные символы (!@#$%)</li>
                                                    <li>Бессмысленный набор символов</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-danger">
                                            <div class="card-body">
                                                <h5 class="text-danger">❌ Чего избегать:</h5>
                                                <ul>
                                                    <li>Имена и даты рождения</li>
                                                    <li>Слова из словаря</li>
                                                    <li>Простые последовательности</li>
                                                    <li>Один пароль для всех аккаунтов</li>
                                                    <li>Пароли типа "123456"</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <h4 class="mt-4">🎯 Примеры хороших паролей:</h4>
                                <div class="code-block">
                                    <code>Bl@ckPanther#2024!</code><br>
                                    <code>Minecraft$Forest_88</code><br>
                                    <code>T1kTok_St@r$h1ne</code>
                                </div>

                                <div class="interactive-element mt-4">
                                    <h5><i class="bi bi-shield-check"></i> Генератор паролей:</h5>
                                    <button class="btn btn-cyber" onclick="generatePassword()">Сгенерировать пароль</button>
                                    <div id="generatedPassword" class="mt-2 p-3 bg-dark border rounded" style="display: none;">
                                        <code id="passwordOutput"></code>
                                        <button class="btn btn-sm btn-cyber-outline ms-2" onclick="copyPassword()">Копировать</button>
                                    </div>
                                </div>
                                """
                            }
                        ],
                    },
                    {
                        "id": "lesson-1-3",
                        "title": "Храним пароли в безопасности",
                        "description": "Узнай, где и как правильно хранить свои пароли.",
                        "duration": 30,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "video_url": "https://www.youtube.com/embed/5R6k8mnD-bc",
                        "sublessons": [
                            {
                                "id": "sub-1-3-1",
                                "title": "Менеджеры паролей - твой цифровой сейф",
                                "description": "Использование менеджеров паролей",
                                "duration": 15,
                                "completed": False,
                                "content": """
                                <h3>💾 Безопасное хранение паролей</h3>
                                
                                <div class="alert alert-warning">
                                    <h5><i class="bi bi-exclamation-triangle"></i> Важно!</h5>
                                    <p>Никогда не храни пароли в заметках на телефоне или в сообщениях!</p>
                                </div>

                                <h4 class="mt-4">Лучшие способы хранения:</h4>
                                <div class="row">
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-info text-center">
                                            <div class="card-body">
                                                <i class="bi bi-safe" style="font-size: 2rem; color: var(--cyber-info);"></i>
                                                <h5 class="mt-2">Менеджеры паролей</h5>
                                                <p>Bitwarden, LastPass</p>
                                                <small class="text-success">✅ Безопасно</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-warning text-center">
                                            <div class="card-body">
                                                <i class="bi bi-journal" style="font-size: 2rem; color: var(--cyber-warning);"></i>
                                                <h5 class="mt-2">Бумажный блокнот</h5>
                                                <p>Дома в надежном месте</p>
                                                <small class="text-warning">⚠️ Умеренно безопасно</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-danger text-center">
                                            <div class="card-body">
                                                <i class="bi bi-file-text" style="font-size: 2rem; color: var(--cyber-danger);"></i>
                                                <h5 class="mt-2">Файл на компьютере</h5>
                                                <p>Текстовый документ</p>
                                                <small class="text-danger">❌ Опасно</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """
                            }
                        ],
                    }
                ],
            },
            {
                "id": "module-2",
                "title": "Фишинг: не попадись на удочку!",
                "description": "Научись распознавать мошеннические письма и сообщения.",
                "icon": "fish",
                "difficulty": "beginner",
                "estimated_time": "6 часов",
                "completed_lessons": 0,
                "video_overview": "https://www.youtube.com/embed/Y7zNlEMDm14",
                "lessons": [
                    {
                        "id": "lesson-2-1",
                        "title": "Что такое фишинг и как он работает",
                        "description": "Узнай о самых распространенных видах интернет-мошенничества.",
                        "duration": 30,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "video_url": "https://www.youtube.com/embed/R12_y2BhKbE",
                        "sublessons": [
                            {
                                "id": "sub-2-1-1",
                                "title": "Фишинг - это как рыбалка",
                                "description": "Аналогия с рыбалкой для понимания фишинга",
                                "duration": 15,
                                "completed": False,
                                "content": """
                                <h3>🎣 Фишинг = Рыбалка для хакеров</h3>
                                
                                <div class="row mt-4">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-primary">
                                            <div class="card-body">
                                                <h5 class="text-primary">Рыбак (Хакер)</h5>
                                                <ul>
                                                    <li>Бросает удочку (отправляет письмо)</li>
                                                    <li>Использует приманку (интересное предложение)</li>
                                                    <li>Ждет, когда клюнет рыба (ты перейдешь по ссылке)</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-warning">
                                            <div class="card-body">
                                                <h5 class="text-warning">Рыба (Ты)</h5>
                                                <ul>
                                                    <li>Видишь приманку (заманчивое письмо)</li>
                                                    <li>Клюешь на наживку (переходишь по ссылке)</li>
                                                    <li>Попадаешь на крючок (вводишь свои данные)</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="alert alert-info mt-4">
                                    <h5><i class="bi bi-lightbulb"></i> Запомни!</h5>
                                    <p>Фишинг - это когда мошенники притворяются кем-то другим, чтобы украсть твои данные.</p>
                                </div>
                                """
                            }
                        ],
                    },
                    {
                        "id": "lesson-2-2",
                        "title": "Распознаем фишинговые письма",
                        "description": "Научись видеть признаки мошеннических сообщений.",
                        "duration": 40,
                        "completed": False,
                        "quiz": False,
                        "practice": True,
                        "video_url": "https://www.youtube.com/embed/mKxGcM-0ig0",
                        "sublessons": [
                            {
                                "id": "sub-2-2-1",
                                "title": "5 признаков фишингового письма",
                                "description": "Ключевые признаки мошеннических писем",
                                "duration": 25,
                                "completed": False,
                                "content": """
                                <h3>🔍 Ищем признаки обмана</h3>
                                
                                <div class="steps mt-4">
                                    <div class="step">
                                        <div class="step-number">1</div>
                                        <div class="step-content">
                                            <h6>Срочность</h6>
                                            <p>"СРОЧНО!", "Счет будет заблокирован через 24 часа!"</p>
                                            <small>Мошенники создают панику</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">2</div>
                                        <div class="step-content">
                                            <h6>Подозрительный отправитель</h6>
                                            <p>support@yandex-security.ru (вместо @yandex.ru)</p>
                                            <small>Всегда проверяй адрес отправителя</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">3</div>
                                        <div class="step-content">
                                            <h6>Ошибки в тексте</h6>
                                            <p>Опечатки, плохой перевод, странные формулировки</p>
                                            <small>Крупные компании следят за грамотностью</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">4</div>
                                        <div class="step-content">
                                            <h6>Ссылки не туда</h6>
                                            <p>Наведи курсор на ссылку - увидишь настоящий адрес</p>
                                            <small>Не кликай сразу! Сначала проверь</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">5</div>
                                        <div class="step-content">
                                            <h6>Просьба о данных</h6>
                                            <p>"Подтвердите пароль", "Введите данные карты"</p>
                                            <small>Настоящие сервисы так не просят</small>
                                        </div>
                                    </div>
                                </div>

                                <style>
                                .steps {
                                    position: relative;
                                    padding-left: 3rem;
                                }
                                .steps::before {
                                    content: '';
                                    position: absolute;
                                    left: 1.5rem;
                                    top: 0;
                                    bottom: 0;
                                    width: 2px;
                                    background: var(--cyber-primary);
                                }
                                .step {
                                    position: relative;
                                    margin-bottom: 2rem;
                                }
                                .step-number {
                                    position: absolute;
                                    left: -3rem;
                                    top: 0;
                                    width: 3rem;
                                    height: 3rem;
                                    background: var(--cyber-primary);
                                    color: var(--cyber-darker);
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-weight: bold;
                                    font-size: 1.2rem;
                                }
                                .step-content {
                                    background: rgba(30, 30, 45, 0.8);
                                    padding: 1.5rem;
                                    border-radius: 10px;
                                    border: 1px solid var(--cyber-border);
                                }
                                </style>
                                """
                            }
                        ],
                    }
                ],
            },
            {
                "id": "module-3",
                "title": "Защита от вирусов и вредоносного ПО",
                "description": "Узнай, как защитить свои устройства от вирусов и вредоносных программ.",
                "icon": "shield",
                "difficulty": "beginner",
                "estimated_time": "7 часов",
                "completed_lessons": 0,
                "video_overview": "https://www.youtube.com/embed/cT4DuDdGG9g",
                "lessons": [
                    {
                        "id": "lesson-3-1",
                        "title": "Вирусы, трояны и черви - кто они?",
                        "description": "Познакомься с разными типами вредоносных программ.",
                        "duration": 35,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "video_url": "https://www.youtube.com/embed/n8mbzU0X2nQ",
                        "sublessons": [
                            {
                                "id": "sub-3-1-1",
                                "title": "Цифровые болезни компьютера",
                                "description": "Аналогия с болезнями для понимания вирусов",
                                "duration": 20,
                                "completed": False,
                                "content": """
                                <h3>🤒 Компьютерные "болезни"</h3>
                                
                                <div class="row mt-4">
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-danger">
                                            <div class="card-body text-center">
                                                <i class="bi bi-bug" style="font-size: 2rem; color: var(--cyber-danger);"></i>
                                                <h5 class="mt-2">Вирусы</h5>
                                                <p>Как грипп - заражают файлы и распространяются</p>
                                                <small class="text-muted">Нужно действие пользователя</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-warning">
                                            <div class="card-body text-center">
                                                <i class="bi bi-ticket-perforated" style="font-size: 2rem; color: var(--cyber-warning);"></i>
                                                <h5 class="mt-2">Трояны</h5>
                                                <p>Как троянский конь - прячутся в полезных программах</p>
                                                <small class="text-muted">Маскируются под легальное ПО</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card bg-dark border-info">
                                            <div class="card-body text-center">
                                                <i class="bi bi-infinity" style="font-size: 2rem; color: var(--cyber-info);"></i>
                                                <h5 class="mt-2">Черви</h5>
                                                <p>Как зараза - распространяются сами по сети</p>
                                                <small class="text-muted">Не нуждаются в пользователе</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="alert alert-success mt-4">
                                    <h5><i class="bi bi-shield-check"></i> Профилактика лучше лечения!</h5>
                                    <p>Регулярно обновляй программы, используй антивирус и не скачивай файлы из непроверенных источников.</p>
                                </div>
                                """
                            }
                        ],
                    }
                ],
            },
            {
                "id": "module-4",
                "title": "Безопасность в социальных сетях",
                "description": "Научись безопасно общаться в соцсетях и защищать свою личную информацию.",
                "icon": "people",
                "difficulty": "beginner",
                "estimated_time": "6 часов",
                "completed_lessons": 0,
                "video_overview": "https://www.youtube.com/embed/PR0c-gTlAj0",
                "lessons": [
                    {
                        "id": "lesson-4-1",
                        "title": "Что можно и нельзя публиковать в соцсетях",
                        "description": "Узнай о цифровой гигиене и защите личной информации.",
                        "duration": 40,
                        "completed": False,
                        "quiz": True,
                        "practice": False,
                        "video_url": "https://www.youtube.com/embed/NhlY3cMqo-M",
                        "sublessons": [
                            {
                                "id": "sub-4-1-1",
                                "title": "Цифровой след - что это?",
                                "description": "Понимание цифрового следа и его последствий",
                                "duration": 25,
                                "completed": False,
                                "content": """
                                <h3>👣 Твой цифровой след</h3>
                                <p>Все, что ты публикуешь в интернете, остается там навсегда. Это и есть твой цифровой след.</p>
                                
                                <div class="row mt-4">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5 class="text-success">✅ Можно публиковать</h5>
                                                <ul>
                                                    <li>Фото природы и животных</li>
                                                    <li>Рисунки и творчество</li>
                                                    <li>Мнения о книгах и фильмах</li>
                                                    <li>Достижения в учебе</li>
                                                    <li>Интересные факты</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-danger">
                                            <div class="card-body">
                                                <h5 class="text-danger">❌ Нельзя публиковать</h5>
                                                <ul>
                                                    <li>Домашний адрес и телефон</li>
                                                    <li>Фото документов</li>
                                                    <li>Геометки дома и школы</li>
                                                    <li>Интимные фото и мысли</li>
                                                    <li>Информацию о расписании</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="practice-preview mt-4">
                                    <h5><i class="bi bi-search"></i> Проверь себя:</h5>
                                    <p>Какие из этих фото можно публиковать?</p>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="photo1">
                                        <label class="form-check-label" for="photo1">Фото с табличкой школы на фоне</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="photo2">
                                        <label class="form-check-label" for="photo2">Рисунок кота, который ты нарисовал</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" id="photo3">
                                        <label class="form-check-label" for="photo3">Фото паспорта с достижением</label>
                                    </div>
                                    <button class="btn btn-cyber mt-2" onclick="checkPhotos()">Проверить ответы</button>
                                </div>
                                """
                            }
                        ],
                    }
                ],
            }
        ],
    },

    # Дополнительные курсы
    "gaming-security": {
        "id": "gaming-security",
        "title": "Безопасность в играх",
        "description": "Защити свои игровые аккаунты и не попадись на уловки мошенников.",
        "difficulty": "beginner",
        "estimated_time": "15 часов",
        "rating": 4.8,
        "students_count": 18200,
        "video_intro": "https://www.youtube.com/embed/gaming_security_video",
        "modules": []
    },

    "smartphone-security": {
        "id": "smartphone-security", 
        "title": "Безопасность смартфона",
        "description": "Научись защищать свой телефон от вирусов и мошенников.",
        "difficulty": "beginner",
        "estimated_time": "12 часов",
        "rating": 4.7,
        "students_count": 15600,
        "video_intro": "https://www.youtube.com/embed/smartphone_security_video",
        "modules": []
    }
}

def get_course(course_id):
    """Получить курс по ID"""
    return COURSES_DATA.get(course_id)

def get_all_courses():
    """Получить все курсы"""
    return COURSES_DATA

def get_course_lesson(course_id, lesson_id):
    """Получить урок из курса"""
    course = get_course(course_id)
    if not course:
        return None
    
    for module in course['modules']:
        for lesson in module['lessons']:
            if lesson['id'] == lesson_id:
                return lesson, module
    return None, None

def get_course_module(course_id, module_id):
    """Получить модуль из курса"""
    course = get_course(course_id)
    if not course:
        return None
    
    for module in course['modules']:
        if module['id'] == module_id:
            return module
    return None