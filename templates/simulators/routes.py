from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
import random
import time
from datetime import datetime

simulators_bp = Blueprint('simulators', __name__)

# База данных фишинг-писем
PHISHING_EMAILS = [
    {
        'id': 1,
        'sender': 'security@bank-ru.com',
        'subject': 'СРОЧНО: Ваш аккаунт будет заблокирован',
        'body': '''
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>Уважаемый клиент,</p>
            <p>Зафиксирована подозрительная активность в вашем аккаунте. 
            Для предотвращения блокировки немедленно перейдите по ссылке и подтвердите данные:</p>
            <p style="text-align: center; margin: 2rem 0;">
                <a href="http://bank-security.ru/verify" style="background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    ПОДТВЕРДИТЬ АККАУНТ
                </a>
            </p>
            <p>Если вы не выполните действия в течение 24 часов, ваш аккаунт будет заблокирован.</p>
            <p>С уважением,<br>Служба безопасности Банка</p>
        </div>
        ''',
        'is_phishing': True,
        'explanation': '🔴 ФИШИНГ: Поддельный домен bank-ru.com, создание искусственной срочности, подозрительная ссылка на неофициальный сайт'
    },
    {
        'id': 2,
        'sender': 'noreply@yandex.ru',
        'subject': 'Обновление политики конфиденциальности',
        'body': '''
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>Здравствуйте,</p>
            <p>Уведомляем вас об обновлении политики конфиденциальности Яндекс. 
            Ознакомиться с изменениями можно в вашем личном кабинете по адресу:</p>
            <p style="text-align: center; margin: 2rem 0;">
                <a href="https://yandex.ru/legal/confidential" style="color: #0066cc; text-decoration: none;">
                    https://yandex.ru/legal/confidential
                </a>
            </p>
            <p>С уважением,<br>Команда Яндекс</p>
        </div>
        ''',
        'is_phishing': False,
        'explanation': '🟢 ЛЕГИТИМНО: Официальный домен Яндекс, стандартное уведомление, безопасная ссылка'
    },
    {
        'id': 3,
        'sender': 'support@paypal-security.com',
        'subject': 'Требуется подтверждение платежа',
        'body': '''
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>Уважаемый пользователь PayPal,</p>
            <p>Мы обнаружили подозрительную активность с вашим аккаунтом. 
            Для защиты средств требуется немедленное подтверждение:</p>
            <p style="text-align: center; margin: 2rem 0;">
                <a href="http://paypal-secure-verify.com/login" style="background: #0070ba; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    ПОДТВЕРДИТЬ ПЛАТЕЖ
                </a>
            </p>
            <p>Без подтверждения ваш аккаунт будет временно ограничен.</p>
            <p>С уважением,<br>Служба безопасности PayPal</p>
        </div>
        ''',
        'is_phishing': True,
        'explanation': '🔴 ФИШИНГ: Поддельный домен paypal-security.com, имитация официального сервиса, давление срочностью'
    }
]

# База данных для социальной инженерии
SOCIAL_ENGINEERING_SCENARIOS = [
    {
        'id': 1,
        'title': 'Телефонный звонок из техподдержки',
        'scenario': '''
        <div class="scenario-content">
            <p><strong>Ситуация:</strong> Вам звонит человек, представляющийся сотрудником техподдержки вашего банка.</p>
            <div class="dialogue">
                <div class="message incoming">
                    <strong>Оператор:</strong> Здравствуйте, это служба безопасности Банка. Мы обнаружили подозрительные операции с вашей картой.
                </div>
                <div class="message outgoing">
                    <strong>Вы:</strong> Какие именно операции?
                </div>
                <div class="message incoming">
                    <strong>Оператор:</strong> Несколько попыток перевода на сумму 50,000 рублей. Для блокировки нужен код из SMS.
                </div>
            </div>
            <p><strong>Вопрос:</strong> Как вы поступите?</p>
        </div>
        ''',
        'options': [
            'Предоставлю код из SMS для защиты счета',
            'Откажусь и перезвоню в банк по официальному номеру',
            'Попрошу больше информации о подозрительных операциях'
        ],
        'correct_answer': 1,
        'explanation': '✅ Правильно! Никогда не сообщайте коды из SMS. Всегда перезванивайте по официальным номерам.'
    }
]

@simulators_bp.route('/')
@login_required
def simulators_home():
    """Главная страница симуляторов"""
    return render_template('simulators/home.html')

@simulators_bp.route('/phishing')
@login_required
def phishing_simulator():
    """Симулятор фишинга"""
    progress = session.get('phishing_progress', {
        'level': 1,
        'score': 0,
        'correct': 0,
        'total': 0
    })
    
    # Получаем email для текущего уровня
    email_data = next((e for e in PHISHING_EMAILS if e['id'] == progress['level']), PHISHING_EMAILS[0])
    
    return render_template('simulators/phishing.html',
                         level=progress['level'],
                         score=progress['score'],
                         correct=progress['correct'],
                         total=progress['total'],
                         total_levels=len(PHISHING_EMAILS),
                         email=email_data)

@simulators_bp.route('/check-phishing', methods=['POST'])
@login_required
def check_phishing():
    """Проверка ответа в фишинг симуляторе"""
    data = request.get_json()
    user_answer = data.get('answer')
    level = data.get('level', 1)
    
    # Находим email для уровня
    email_data = next((e for e in PHISHING_EMAILS if e['id'] == level), PHISHING_EMAILS[0])
    is_correct = user_answer == email_data['is_phishing']
    
    # Обновляем прогресс
    progress = session.get('phishing_progress', {
        'level': 1,
        'score': 0,
        'correct': 0,
        'total': 0
    })
    
    progress['total'] += 1
    if is_correct:
        progress['score'] += 10
        progress['correct'] += 1
    
    # Переходим на следующий уровень
    if is_correct and level < len(PHISHING_EMAILS):
        progress['level'] += 1
    
    session['phishing_progress'] = progress
    
    return jsonify({
        'correct': is_correct,
        'explanation': email_data['explanation'],
        'progress': progress
    })

@simulators_bp.route('/password-cracker')
@login_required
def password_cracker():
    """Симулятор взлома паролей"""
    return render_template('simulators/password_cracker.html')

@simulators_bp.route('/network-scanner')
@login_required
def network_scanner():
    """Симулятор сетевого сканирования"""
    return render_template('simulators/network_scanner.html')

@simulators_bp.route('/social-engineering')
@login_required
def social_engineering():
    """Симулятор социальной инженерии"""
    progress = session.get('social_progress', {
        'level': 1,
        'score': 0,
        'correct': 0,
        'total': 0
    })
    
    scenario = next((s for s in SOCIAL_ENGINEERING_SCENARIOS if s['id'] == progress['level']), SOCIAL_ENGINEERING_SCENARIOS[0])
    
    return render_template('simulators/social_engineering.html',
                         level=progress['level'],
                         score=progress['score'],
                         scenario=scenario)

@simulators_bp.route('/check-social', methods=['POST'])
@login_required
def check_social():
    """Проверка ответа в социальной инженерии"""
    data = request.get_json()
    user_answer = data.get('answer')
    level = data.get('level', 1)
    
    scenario = next((s for s in SOCIAL_ENGINEERING_SCENARIOS if s['id'] == level), SOCIAL_ENGINEERING_SCENARIOS[0])
    is_correct = int(user_answer) == scenario['correct_answer']
    
    # Обновляем прогресс
    progress = session.get('social_progress', {
        'level': 1,
        'score': 0,
        'correct': 0,
        'total': 0
    })
    
    progress['total'] += 1
    if is_correct:
        progress['score'] += 15
        progress['correct'] += 1
        progress['level'] = min(progress['level'] + 1, len(SOCIAL_ENGINEERING_SCENARIOS))
    
    session['social_progress'] = progress
    
    return jsonify({
        'correct': is_correct,
        'explanation': scenario['explanation'],
        'progress': progress
    })

@simulators_bp.route('/api/crack-password', methods=['POST'])
@login_required
def crack_password():
    """Симуляция взлома пароля"""
    data = request.get_json()
    password = data.get('password', '')
    
    # Простая симуляция времени взлома
    strength = calculate_password_strength(password)
    crack_time = simulate_crack_time(strength, len(password))
    
    return jsonify({
        'strength': strength,
        'crack_time': crack_time,
        'message': get_crack_message(strength),
        'recommendation': get_recommendation(strength)
    })

@simulators_bp.route('/api/scan-network', methods=['POST'])
@login_required
def scan_network():
    """Симуляция сетевого сканирования"""
    data = request.get_json()
    target = data.get('target', '192.168.1.1')
    
    # Симуляция сканирования
    time.sleep(2)  # Имитация задержки
    
    ports = [
        {'port': 22, 'service': 'SSH', 'status': 'open', 'vulnerability': 'Medium'},
        {'port': 80, 'service': 'HTTP', 'status': 'open', 'vulnerability': 'Low'},
        {'port': 443, 'service': 'HTTPS', 'status': 'open', 'vulnerability': 'Low'},
        {'port': 3389, 'service': 'RDP', 'status': 'open', 'vulnerability': 'High'},
        {'port': 21, 'service': 'FTP', 'status': 'closed', 'vulnerability': 'None'},
    ]
    
    return jsonify({
        'target': target,
        'ports_found': len([p for p in ports if p['status'] == 'open']),
        'ports': ports,
        'recommendations': [
            'Закройте порт 3389 (RDP) или используйте VPN',
            'Обновите SSH до последней версии',
            'Настройте брандмауэр для ограничения доступа'
        ]
    })

def calculate_password_strength(password):
    """Рассчитать сложность пароля"""
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    return min(score, 5)

def simulate_crack_time(strength, length):
    """Симулировать время взлома"""
    base_time = 0.1
    
    if strength == 1: return base_time * 10      # 1 секунда
    elif strength == 2: return base_time * 60    # 6 секунд
    elif strength == 3: return base_time * 600   # 1 минута
    elif strength == 4: return base_time * 3600  # 1 час
    else: return base_time * 86400              # 1 день

def get_crack_message(strength):
    messages = {
        1: "💀 ВЗЛОМАНО МГНОВЕННО! Пароль очень слабый",
        2: "🔥 ВЗЛОМАНО ЗА СЕКУНДЫ! Ненадежный пароль", 
        3: "⚠️ ВЗЛОМ ЗА МИНУТЫ! Можно улучшить",
        4: "🛡️ ВЗЛОМ ЗА ЧАСЫ! Хороший пароль",
        5: "🔒 ВЗЛОМ ЗА ДНИ! Отличный пароль"
    }
    return messages.get(strength, "Неизвестная сложность")

def get_recommendation(strength):
    recommendations = {
        1: "Используйте пароль длиной 12+ символов с буквами, цифрами и специальными символами",
        2: "Добавьте заглавные буквы и специальные символы",
        3: "Увеличьте длину пароля до 16+ символов",
        4: "Отличный пароль! Можете добавить специальные символы для большей надежности",
        5: "Идеальный пароль! Так держать!"
    }
    return recommendations.get(strength, "")