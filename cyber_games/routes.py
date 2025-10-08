from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required, current_user
import random
import time
from datetime import datetime

games_bp = Blueprint('games', __name__)

# Данные для игр
PHISHING_GAME_EMAILS = [
    {
        'id': 1,
        'sender': 'security@bank-ru.com',
        'subject': 'СРОЧНО: Подозрительная активность в вашем аккаунте',
        'content': 'Уважаемый клиент,\n\nЗафиксирована подозрительная активность в вашем банковском аккаунте. Для защиты средств требуется немедленная проверка.\n\nПерейдите по ссылке для верификации: http://bank-security-verify.ru/check\n\nНе отвечайте на это письмо. Это автоматическое уведомление.\n\nС уважением,\nСлужба безопасности Банка',
        'is_phishing': True,
        'clues': [
            'Доменное имя bank-ru.com вместо официального bank.ru',
            'Ссылка ведет на подозрительный домен',
            'Создает искусственную срочность',
            'Требует немедленных действий'
        ]
    },
    {
        'id': 2,
        'sender': 'noreply@mail.ru',
        'subject': 'Подтверждение регистрации',
        'content': 'Вы успешно зарегистрировались на сайте Mail.ru. Для завершения регистрации подтвердите ваш email.\n\nКод подтверждения: 458792\n\nЕсли вы не регистрировались, проигнорируйте это письмо.\n\nС уважением,\nКоманда Mail.ru',
        'is_phishing': False,
        'clues': [
            'Официальный домен mail.ru',
            'Не требует перехода по ссылкам',
            'Предлагает проигнорировать если не вы регистрировались',
            'Нет искусственной срочности'
        ]
    }
]

PASSWORD_STRENGTH_GAME = [
    {'password': '123456', 'strength': 5, 'time_to_crack': 'Мгновенно'},
    {'password': 'password', 'strength': 8, 'time_to_crack': 'Мгновенно'},
    {'password': 'Andrey2005', 'strength': 35, 'time_to_crack': '2 часа'},
    {'password': 'Sunshine!2024', 'strength': 65, 'time_to_crack': '3 дня'},
    {'password': 'J8$sK!23pL09@qW', 'strength': 95, 'time_to_crack': '200 лет'}
]

@games_bp.route('/')
@login_required
def games_dashboard():
    """Главная страница игр"""
    return render_template('cyber_games/dashboard.html')

@games_bp.route('/phishing-hunter')
@login_required
def phishing_hunter():
    """Игра: Охотник за фишингом"""
    return render_template('cyber_games/phishing_hunter.html')

@games_bp.route('/password-master')
@login_required
def password_master():
    """Игра: Мастер паролей"""
    return render_template('cyber_games/password_master.html')

@games_bp.route('/encryption-challenge')
@login_required
def encryption_challenge():
    """Игра: Шифровальный вызов"""
    return render_template('cyber_games/encryption_challenge.html')

@games_bp.route('/cyber-quiz')
@login_required
def cyber_quiz():
    """Квиз по кибербезопасности"""
    return render_template('cyber_games/cyber_quiz.html')

# API для игр
@games_bp.route('/api/games/phishing/emails')
def get_phishing_emails():
    """Получить emails для игры в фишинг"""
    return jsonify({'emails': PHISHING_GAME_EMAILS})

@games_bp.route('/api/games/phishing/check', methods=['POST'])
def check_phishing_game():
    """Проверить ответ в игре фишинг"""
    data = request.get_json()
    email_id = data.get('email_id')
    user_answer = data.get('is_phishing')
    
    email = next((e for e in PHISHING_GAME_EMAILS if e['id'] == email_id), None)
    if not email:
        return jsonify({'error': 'Email не найден'}), 404
    
    is_correct = (user_answer == email['is_phishing'])
    score = 100 if is_correct else 0
    
    # Сохраняем результат
    if current_user.is_authenticated:
        game_stats = session.get('game_stats', {})
        phishing_stats = game_stats.get('phishing', {'played': 0, 'won': 0, 'score': 0})
        
        phishing_stats['played'] += 1
        if is_correct:
            phishing_stats['won'] += 1
            phishing_stats['score'] += score
        
        game_stats['phishing'] = phishing_stats
        session['game_stats'] = game_stats
    
    return jsonify({
        'correct': is_correct,
        'score': score,
        'explanation': email['clues'],
        'next_level': True
    })

@games_bp.route('/api/games/password/strength')
def get_password_strength_game():
    """Получить данные для игры с паролями"""
    return jsonify({'passwords': PASSWORD_STRENGTH_GAME})

@games_bp.route('/api/games/password/check', methods=['POST'])
def check_password_game():
    """Проверить ответ в игре с паролями"""
    data = request.get_json()
    password = data.get('password')
    user_strength = data.get('strength')
    
    target_password = next((p for p in PASSWORD_STRENGTH_GAME if p['password'] == password), None)
    if not target_password:
        return jsonify({'error': 'Пароль не найден'}), 404
    
    # Расчет точности (в пределах 20 пунктов)
    difference = abs(target_password['strength'] - user_strength)
    score = max(0, 100 - difference * 2)
    
    return jsonify({
        'actual_strength': target_password['strength'],
        'user_strength': user_strength,
        'score': score,
        'time_to_crack': target_password['time_to_crack'],
        'accuracy': f"{max(0, 100 - difference)}%"
    })

@games_bp.route('/api/games/quiz/questions')
def get_quiz_questions():
    """Получить вопросы для квиза"""
    questions = [
        {
            'id': 1,
            'question': 'Что такое фишинг?',
            'options': [
                'Вид рыбалки',
                'Мошеннические письма для кражи данных',
                'Тип компьютерного вируса',
                'Способ шифрования'
            ],
            'correct': 1,
            'explanation': 'Фишинг - это рассылка писем, которые выглядят как от реальных компаний, но предназначены для кражи данных.'
        },
        {
            'id': 2,
            'question': 'Какой пароль самый надежный?',
            'options': [
                '123456',
                'password',
                'J8$sK!23pL09@qW',
                'qwerty'
            ],
            'correct': 2,
            'explanation': 'Длинные пароли с разными типами символов наиболее надежны.'
        }
    ]
    return jsonify({'questions': questions})

@games_bp.route('/api/games/stats')
@login_required
def get_game_stats():
    """Получить статистику игр"""
    game_stats = session.get('game_stats', {})
    return jsonify(game_stats)

@games_bp.route('/api/games/leaderboard')
def get_leaderboard():
    """Таблица лидеров"""
    leaders = [
        {'username': 'CyberMaster', 'score': 1250, 'games_played': 15},
        {'username': 'SecurityPro', 'score': 980, 'games_played': 12},
        {'username': 'CryptoKing', 'score': 870, 'games_played': 10},
        {'username': current_user.username, 'score': 650, 'games_played': 8},
        {'username': 'DataGuardian', 'score': 540, 'games_played': 7}
    ]
    return jsonify({'leaders': leaders})
