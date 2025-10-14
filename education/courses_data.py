from datetime import datetime

# Основные данные курсов
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
                                <p><strong>Кибербезопасность</strong> — это практика защиты систем, сетей и программ от цифровых атак.</p>
                                
                                <div class="alert alert-info">
                                    <h5><i class="bi bi-info-circle"></i> Ключевые аспекты:</h5>
                                    <ul>
                                        <li><strong>Конфиденциальность</strong> — защита информации от несанкционированного доступа</li>
                                        <li><strong>Целостность</strong> — обеспечение точности и полноты данных</li>
                                        <li><strong>Доступность</strong> — гарантия доступа к информации и системам, когда это необходимо</li>
                                    </ul>
                                </div>

                                <h4>Почему это важно?</h4>
                                <p>В современном мире кибербезопасность критически важна для:</p>
                                <ul>
                                    <li>Защиты личных данных</li>
                                    <li>Обеспечения бизнес-непрерывности</li>
                                    <li>Сохранения национальной безопасности</li>
                                    <li>Предотвращения финансовых потерь</li>
                                </ul>

                                <div class="row mt-4">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5 class="text-success">Защита данных</h5>
                                                <p>Предотвращение утечки конфиденциальной информации</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-warning">
                                            <div class="card-body">
                                                <h5 class="text-warning">Бизнес-риски</h5>
                                                <p>Снижение финансовых и репутационных потерь</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                """,
                            },
                            {
                                "id": "sub-1-1-2",
                                "title": "Триада CIA",
                                "description": "Конфиденциальность, целостность, доступность",
                                "duration": 20,
                                "completed": False,
                                "content": """
                                <h3>Триада CIA (Confidentiality, Integrity, Availability)</h3>
                                <p>Это фундаментальная модель кибербезопасности, которая определяет три ключевых принципа защиты информации.</p>

                                <div class="row text-center mt-4">
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-primary">
                                            <div class="card-body">
                                                <h4 class="text-primary">C</h4>
                                                <h5>Конфиденциальность</h5>
                                                <p>Доступ к информации только для авторизованных лиц</p>
                                                <small>Пример: шифрование данных</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h4 class="text-success">I</h4>
                                                <h5>Целостность</h5>
                                                <p>Защита от несанкционированного изменения</p>
                                                <small>Пример: цифровые подписи</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-warning">
                                            <div class="card-body">
                                                <h4 class="text-warning">A</h4>
                                                <h5>Доступность</h5>
                                                <p>Обеспечение доступа к системам когда нужно</p>
                                                <small>Пример: защита от DDoS-атак</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <h4 class="mt-4">Практические примеры:</h4>
                                <div class="table-responsive">
                                    <table class="table table-dark table-striped">
                                        <thead>
                                            <tr>
                                                <th>Принцип</th>
                                                <th>Угроза</th>
                                                <th>Метод защиты</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>Конфиденциальность</td>
                                                <td>Утечка данных</td>
                                                <td>Шифрование, контроль доступа</td>
                                            </tr>
                                            <tr>
                                                <td>Целостность</td>
                                                <td>Изменение данных</td>
                                                <td>Хэширование, цифровые подписи</td>
                                            </tr>
                                            <tr>
                                                <td>Доступность</td>
                                                <td>DDoS-атаки</td>
                                                <td>Резервирование, балансировка нагрузки</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                """,
                            },
                            {
                                "id": "sub-1-1-3",
                                "title": "Эволюция киберугроз",
                                "description": "Как развивались киберугрозы с течением времени",
                                "duration": 10,
                                "completed": False,
                                "content": """
                                <h3>Эволюция киберугроз</h3>
                                <p>Киберугрозы постоянно развиваются, становясь все более изощренными и опасными.</p>

                                <div class="timeline mt-4">
                                    <div class="timeline-item">
                                        <div class="timeline-year">1980-е</div>
                                        <div class="timeline-content">
                                            <h6>Вирусы и черви</h6>
                                            <p>Простые самовоспроизводящиеся программы</p>
                                            <small>Пример: Morris Worm (1988)</small>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-year">1990-е</div>
                                        <div class="timeline-content">
                                            <h6>Макровирусы</h6>
                                            <p>Вирусы в документах Office</p>
                                            <small>Пример: Melissa (1999)</small>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-year">2000-е</div>
                                        <div class="timeline-content">
                                            <h6>Сетевые черви</h6>
                                            <p>Быстрое распространение через уязвимости</p>
                                            <small>Пример: ILOVEYOU (2000)</small>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-year">2010-е</div>
                                        <div class="timeline-content">
                                            <h6>Целевые атаки</h6>
                                            <p>APT, ransomware, социальная инженерия</p>
                                            <small>Пример: WannaCry (2017)</small>
                                        </div>
                                    </div>
                                    <div class="timeline-item">
                                        <div class="timeline-year">2020-е</div>
                                        <div class="timeline-content">
                                            <h6>ИИ и облачные атаки</h6>
                                            <p>Использование AI, атаки на облачную инфраструктуру</p>
                                            <small>Пример: SolarWinds (2020)</small>
                                        </div>
                                    </div>
                                </div>

                                <style>
                                .timeline {
                                    position: relative;
                                    padding-left: 2rem;
                                }
                                .timeline::before {
                                    content: '';
                                    position: absolute;
                                    left: 0;
                                    top: 0;
                                    bottom: 0;
                                    width: 2px;
                                    background: var(--cyber-primary);
                                }
                                .timeline-item {
                                    position: relative;
                                    margin-bottom: 2rem;
                                }
                                .timeline-year {
                                    position: absolute;
                                    left: -2rem;
                                    top: 0;
                                    background: var(--cyber-primary);
                                    color: var(--cyber-darker);
                                    padding: 0.3rem 0.8rem;
                                    border-radius: 15px;
                                    font-weight: bold;
                                    font-size: 0.8rem;
                                }
                                .timeline-content {
                                    background: rgba(30, 30, 45, 0.8);
                                    padding: 1rem;
                                    border-radius: 8px;
                                    border: 1px solid var(--cyber-border);
                                }
                                </style>
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
                                <p>Вредоносное ПО (malware) — это любая программа, созданная для нанесения ущерба компьютерам, сетям или пользователям.</p>

                                <div class="row mt-4">
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-danger h-100">
                                            <div class="card-body">
                                                <h5 class="text-danger">🦠 Вирусы</h5>
                                                <p><strong>Программы, которые распространяются и заражают другие файлы</strong></p>
                                                <ul>
                                                    <li>Требуют действия пользователя для активации</li>
                                                    <li>Распространяются через зараженные файлы</li>
                                                    <li>Могут повреждать или удалять данные</li>
                                                </ul>
                                                <small class="text-muted">Пример: CIH, Melissa</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-warning h-100">
                                            <div class="card-body">
                                                <h5 class="text-warning">🐴 Трояны</h5>
                                                <p><strong>Программы, маскирующиеся под легитимное ПО</strong></p>
                                                <ul>
                                                    <li>Не распространяются самостоятельно</li>
                                                    <li>Скрывают вредоносную функциональность</li>
                                                    <li>Создают бэкдоры для удаленного доступа</li>
                                                </ul>
                                                <small class="text-muted">Пример: Zeus, Emotet</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-info h-100">
                                            <div class="card-body">
                                                <h5 class="text-info">🐛 Черви</h5>
                                                <p><strong>Самостоятельно распространяющиеся программы</strong></p>
                                                <ul>
                                                    <li>Не требуют действий пользователя</li>
                                                    <li>Используют уязвимости сетевых служб</li>
                                                    <li>Могут создавать ботнеты</li>
                                                </ul>
                                                <small class="text-muted">Пример: WannaCry, Stuxnet</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <div class="card bg-dark border-success h-100">
                                            <div class="card-body">
                                                <h5 class="text-success">💸 Ransomware</h5>
                                                <p><strong>Программы-вымогатели, шифрующие данные</strong></p>
                                                <ul>
                                                    <li>Шифруют файлы пользователя</li>
                                                    <li>Требуют выкуп за расшифровку</li>
                                                    <li>Распространяются через фишинг и уязвимости</li>
                                                </ul>
                                                <small class="text-muted">Пример: CryptoLocker, Petya</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <h4 class="mt-4">Методы защиты</h4>
                                <div class="alert alert-success">
                                    <h6><i class="bi bi-shield-check"></i> Эффективные меры защиты:</h6>
                                    <ul>
                                        <li>Регулярное обновление антивирусного ПО</li>
                                        <li>Обновление операционной системы и приложений</li>
                                        <li>Осторожность при открытии вложений</li>
                                        <li>Резервное копирование важных данных</li>
                                        <li>Использование брандмауэров</li>
                                    </ul>
                                </div>
                                """,
                            },
                            {
                                "id": "sub-1-2-2",
                                "title": "Социальная инженерия",
                                "description": "Методы манипуляции людьми для получения конфиденциальной информации",
                                "duration": 30,
                                "completed": False,
                                "content": """
                                <h3>Социальная инженерия</h3>
                                <p>Методы психологического воздействия на людей с целью получения конфиденциальной информации или совершения определенных действий.</p>

                                <div class="table-responsive mt-4">
                                    <table class="table table-dark table-striped">
                                        <thead>
                                            <tr>
                                                <th>Метод</th>
                                                <th>Описание</th>
                                                <th>Пример</th>
                                                <th>Защита</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td><strong>Фишинг</strong></td>
                                                <td>Массовая рассылка поддельных писем</td>
                                                <td>"Ваш аккаунт заблокирован, перейдите по ссылке"</td>
                                                <td>Проверка отправителя, осторожность с ссылками</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Целевой фишинг</strong></td>
                                                <td>Целенаправленная атака на конкретных лиц</td>
                                                <td>Письмо от "руководства" с просьбой перевести деньги</td>
                                                <td>Двухфакторная аутентификация, верификация</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Претекстинг</strong></td>
                                                <td>Создание вымышленного сценария</td>
                                                <td>"Я из техподдержки, нужен ваш пароль"</td>
                                                <td>Никогда не сообщать пароли по телефону</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Тайлгейтинг</strong></td>
                                                <td>Проход за авторизованным лицом</td>
                                                <td>Проход в охраняемую зону за сотрудником</td>
                                                <td>Строгий контроль доступа, бейджи</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Кви про кво</strong></td>
                                                <td>Предложение помощи в обмен на информацию</td>
                                                <td>"Помогу решить проблему, установите эту программу"</td>
                                                <td>Установка ПО только из доверенных источников</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <h4>Практическое задание:</h4>
                                <div class="alert alert-warning">
                                    <h6><i class="bi bi-lightbulb"></i> Определите признаки фишинга:</h6>
                                    <p>Проанализируйте это письмо и найдите 5 признаков фишинга:</p>
                                    <div class="bg-dark p-3 border rounded">
                                        <p><strong>От:</strong> security@bank-support.com</p>
                                        <p><strong>Тема:</strong> СРОЧНО: Ваш аккаунт будет заблокирован!</p>
                                        <p>Уважаемый клиент,</p>
                                        <p>Мы обнаружили подозрительную активность в вашем аккаунте. Для предотвращения блокировки немедленно перейдите по ссылке и подтвердите ваши данные:</p>
                                        <p><a href="#">http://bank-secure-verify.com/login</a></p>
                                        <p>Если вы не подтвердите данные в течение 24 часов, ваш аккаунт будет заблокирован.</p>
                                        <p>С уважением,<br>Служба безопасности банка</p>
                                    </div>
                                </div>

                                <div class="mt-3">
                                    <button class="btn btn-cyber" onclick="showPhishingSolution()">Показать решение</button>
                                    <div id="phishing-solution" style="display: none;" class="mt-3">
                                        <div class="alert alert-success">
                                            <h6>Признаки фишинга:</h6>
                                            <ol>
                                                <li>Создание срочности ("СРОЧНО", "24 часа")</li>
                                                <li>Подозрительный домен (bank-support.com вместо официального)</li>
                                                <li>Требование перейти по ссылке для "подтверждения"</li>
                                                <li>Угроза блокировки аккаунта</li>
                                                <li>Обобщенное обращение ("Уважаемый клиент")</li>
                                            </ol>
                                        </div>
                                    </div>
                                </div>

                                <script>
                                function showPhishingSolution() {
                                    document.getElementById('phishing-solution').style.display = 'block';
                                }
                                </script>
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
                        "quiz": True,
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
                                <p>Подход, при котором используется несколько уровней защиты для предотвращения атак. Если один уровень fails, другие продолжают защищать.</p>

                                <div class="steps mt-4">
                                    <div class="step">
                                        <div class="step-number">1</div>
                                        <div class="step-content">
                                            <h6>Политики и обучение</h6>
                                            <p>Создание политик безопасности и обучение сотрудников</p>
                                            <small>Человеческий фактор - первая линия защиты</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">2</div>
                                        <div class="step-content">
                                            <h6>Физическая безопасность</h6>
                                            <p>Контроль доступа к помещениям и оборудованию</p>
                                            <small>Системы контроля доступа, видеонаблюдение</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">3</div>
                                        <div class="step-content">
                                            <h6>Периметровая защита</h6>
                                            <p>Фаерволы, системы обнаружения вторжений</p>
                                            <small>Защита границ сети от внешних угроз</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">4</div>
                                        <div class="step-content">
                                            <h6>Сетевая защита</h6>
                                            <p>Сегментация сети, VPN, шифрование</p>
                                            <small>Защита данных при передаче по сети</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">5</div>
                                        <div class="step-content">
                                            <h6>Защита конечных точек</h6>
                                            <p>Антивирусы, EDR системы, обновления</p>
                                            <small>Защита рабочих станций и серверов</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">6</div>
                                        <div class="step-content">
                                            <h6>Защита приложений</h6>
                                            <p>Безопасная разработка, WAF, тестирование</p>
                                            <small>Защита на уровне приложений</small>
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="step-number">7</div>
                                        <div class="step-content">
                                            <h6>Защита данных</h6>
                                            <p>Шифрование, контроль доступа, резервное копирование</p>
                                            <small>Защита самой ценной информации</small>
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

                                <h4 class="mt-4">Преимущества подхода:</h4>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="alert alert-info">
                                            <h6><i class="bi bi-check-circle"></i> Преимущества:</h6>
                                            <ul>
                                                <li>Повышенная устойчивость к атакам</li>
                                                <li>Время для обнаружения и реагирования</li>
                                                <li>Снижение единой точки отказа</li>
                                                <li>Соответствие требованиям compliance</li>
                                            </ul>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="alert alert-warning">
                                            <h6><i class="bi bi-exclamation-triangle"></i> Сложности:</h6>
                                            <ul>
                                                <li>Высокая стоимость реализации</li>
                                                <li>Сложность управления</li>
                                                <li>Возможное снижение производительности</li>
                                                <li>Необходимость постоянного обслуживания</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                """,
                            },
                            {
                                "id": "sub-1-3-2",
                                "title": "Принцип наименьших привилегий",
                                "description": "Предоставление пользователям минимально необходимых прав",
                                "duration": 25,
                                "completed": False,
                                "content": """
                                <h3>Принцип наименьших привилегий (PoLP)</h3>
                                <p>Пользователи и процессы должны иметь только те права доступа, которые необходимы для выполнения их задач.</p>

                                <div class="row mt-4">
                                    <div class="col-md-8">
                                        <h5>Как это работает?</h5>
                                        <div class="privilege-levels">
                                            <div class="privilege-item admin">
                                                <div class="privilege-badge">Администратор</div>
                                                <div class="privilege-desc">Полный доступ ко всем системам</div>
                                            </div>
                                            <div class="privilege-item user">
                                                <div class="privilege-badge">Пользователь</div>
                                                <div class="privilege-desc">Доступ к необходимым приложениям</div>
                                            </div>
                                            <div class="privilege-item guest">
                                                <div class="privilege-badge">Гость</div>
                                                <div class="privilege-desc">Ограниченный доступ для базовых задач</div>
                                            </div>
                                        </div>

                                        <h5 class="mt-4">Преимущества:</h5>
                                        <ul>
                                            <li><strong>Снижение ущерба</strong> - при компрометации аккаунта</li>
                                            <li><strong>Предотвращение ошибок</strong> - случайные изменения</li>
                                            <li><strong>Соответствие требованиям</strong> - аудит и compliance</li>
                                            <li><strong>Упрощение управления</strong> - четкие права доступа</li>
                                        </ul>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body text-center">
                                                <h4 class="text-success">✓ Правильно</h4>
                                                <p>Бухгалтер имеет доступ только к финансовым системам</p>
                                            </div>
                                        </div>
                                        <div class="card bg-dark border-danger mt-3">
                                            <div class="card-body text-center">
                                                <h4 class="text-danger">✗ Неправильно</h4>
                                                <p>Все сотрудники имеют права администратора</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <style>
                                .privilege-levels {
                                    display: flex;
                                    flex-direction: column;
                                    gap: 1rem;
                                }
                                .privilege-item {
                                    display: flex;
                                    align-items: center;
                                    padding: 1rem;
                                    border-radius: 8px;
                                    border: 2px solid;
                                }
                                .privilege-item.admin {
                                    border-color: #dc3545;
                                    background: rgba(220, 53, 69, 0.1);
                                }
                                .privilege-item.user {
                                    border-color: #0dcaf0;
                                    background: rgba(13, 202, 240, 0.1);
                                }
                                .privilege-item.guest {
                                    border-color: #198754;
                                    background: rgba(25, 135, 84, 0.1);
                                }
                                .privilege-badge {
                                    font-weight: bold;
                                    margin-right: 1rem;
                                    min-width: 120px;
                                }
                                .admin .privilege-badge { color: #dc3545; }
                                .user .privilege-badge { color: #0dcaf0; }
                                .guest .privilege-badge { color: #198754; }
                                </style>

                                <h4 class="mt-4">Практическая реализация:</h4>
                                <div class="table-responsive">
                                    <table class="table table-dark table-striped">
                                        <thead>
                                            <tr>
                                                <th>Роль</th>
                                                <th>Права доступа</th>
                                                <th>Пример</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>Администратор</td>
                                                <td>Полные права на управление системой</td>
                                                <td>Установка ПО, настройка безопасности</td>
                                            </tr>
                                            <tr>
                                                <td>Пользователь</td>
                                                <td>Стандартные права для работы</td>
                                                <td>Доступ к офисным приложениям, сетевым ресурсам</td>
                                            </tr>
                                            <tr>
                                                <td>Гость</td>
                                                <td>Ограниченные права</td>
                                                <td>Только веб-браузер, без установки ПО</td>
                                            </tr>
                                            <tr>
                                                <td>Сервисная учетная запись</td>
                                                <td>Минимальные права для конкретной службы</td>
                                                <td>Доступ только к необходимой БД или службе</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                """,
                            }
                        ],
                    }
                ],
            },
            # Модуль 2: Основы криптографии
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
                                
                                <h4>Принцип работы AES:</h4>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-info">
                                            <div class="card-body">
                                                <h5 class="text-info">Шаги шифрования:</h5>
                                                <ol>
                                                    <li>AddRoundKey</li>
                                                    <li>SubBytes</li>
                                                    <li>ShiftRows</li>
                                                    <li>MixColumns</li>
                                                </ol>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="card bg-dark border-success">
                                            <div class="card-body">
                                                <h5 class="text-success">Преимущества:</h5>
                                                <ul>
                                                    <li>Высокая скорость работы</li>
                                                    <li>Стойкость к криптоанализу</li>
                                                    <li>Эффективная реализация</li>
                                                    <li>Международный стандарт</li>
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
            # Модуль 3: Сетевая безопасность
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
                    }
                ],
            }
        ],
    },
    
    # Другие курсы...
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
            "students": 28000,
        },
        "requirements": [
            "Знание основ сетевых технологий",
            "Базовые навыки работы с Linux",
        ],
        "resources": [
            {"name": "Лабораторные среды", "icon": "cpu"},
            {"name": "Инструменты хакинга", "icon": "tools"},
        ],
        "final_exam": True,
        "modules": []  # Модули можно добавить позже
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