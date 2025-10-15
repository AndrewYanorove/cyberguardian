from flask import Blueprint, render_template, jsonify, request, session
from flask_login import login_required, current_user
import random
import time
from datetime import datetime
import base64
import hashlib

# Импортируем данные из отдельных модулей
from cyber_games.games_data.phishing_data import PHISHING_GAME_EMAILS
from cyber_games.games_data.password_data import PASSWORD_STRENGTH_GAME
from cyber_games.games_data.encryption_data import ENCRYPTION_CHALLENGES
from cyber_games.games_data.quiz_data import QUIZ_QUESTIONS

games_bp = Blueprint('games', __name__)

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

@games_bp.route('/api/games/password/tips')
def get_password_tips():
    """Получить советы по безопасности паролей"""
    from games_data.password_data import PASSWORD_SECURITY_TIPS
    return jsonify({'tips': PASSWORD_SECURITY_TIPS})

@games_bp.route('/api/games/password/cracking-methods')
def get_cracking_methods():
    """Получить методы взлома паролей"""
    from games_data.password_data import PASSWORD_CRACKING_METHODS
    return jsonify({'methods': PASSWORD_CRACKING_METHODS})

@games_bp.route('/api/games/password/analysis/<password>')
def analyze_password(password):
    """Проанализировать пароль"""
    # Простой анализ пароля
    analysis = {
        'length': len(password),
        'has_uppercase': any(c.isupper() for c in password),
        'has_lowercase': any(c.islower() for c in password),
        'has_numbers': any(c.isdigit() for c in password),
        'has_symbols': any(not c.isalnum() for c in password),
        'is_common': password in ['123456', 'password', 'qwerty', 'admin']  # и т.д.
    }
    
    return jsonify({'analysis': analysis})

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
    # Перемешиваем письма для разнообразия
    shuffled_emails = random.sample(PHISHING_GAME_EMAILS, min(5, len(PHISHING_GAME_EMAILS)))
    return jsonify({'emails': shuffled_emails})

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
        phishing_stats = game_stats.get('phishing', {'played': 0, 'won': 0, 'score': 0, 'total_emails': 0})
        
        phishing_stats['played'] += 1
        phishing_stats['total_emails'] += 1
        if is_correct:
            phishing_stats['won'] += 1
            phishing_stats['score'] += score
        
        game_stats['phishing'] = phishing_stats
        session['game_stats'] = game_stats
    
    return jsonify({
        'correct': is_correct,
        'score': score,
        'explanation': email['clues'],
        'is_phishing': email['is_phishing'],
        'next_level': True
    })

@games_bp.route('/api/games/password/strength')
def get_password_strength_game():
    """Получить данные для игры с паролями"""
    # Выбираем случайные пароли для игры
    selected_passwords = random.sample(PASSWORD_STRENGTH_GAME, min(5, len(PASSWORD_STRENGTH_GAME)))
    return jsonify({'passwords': selected_passwords})

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
    
    # Сохраняем результат
    if current_user.is_authenticated:
        game_stats = session.get('game_stats', {})
        password_stats = game_stats.get('password', {'played': 0, 'total_score': 0, 'rounds_played': 0})
        
        password_stats['played'] += 1
        password_stats['rounds_played'] += 1
        password_stats['total_score'] += score
        
        game_stats['password'] = password_stats
        session['game_stats'] = game_stats
    
    return jsonify({
        'actual_strength': target_password['strength'],
        'user_strength': user_strength,
        'score': score,
        'time_to_crack': target_password['time_to_crack'],
        'feedback': target_password['feedback'],
        'accuracy': f"{max(0, 100 - difference)}%"
    })

@games_bp.route('/api/games/password/generate', methods=['POST'])
def generate_password():
    """Сгенерировать случайный пароль"""
    data = request.get_json()
    length = data.get('length', 12)
    
    # Генерация случайного пароля
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Оценка сложности
    strength = min(95, 30 + length * 5)
    
    return jsonify({
        'password': password,
        'strength': strength,
        'length': length
    })

@games_bp.route('/api/games/encryption/challenges')
def get_encryption_challenges():
    """Получить задания по шифрованию"""
    # Выбираем случайные задания
    selected_challenges = random.sample(ENCRYPTION_CHALLENGES, min(3, len(ENCRYPTION_CHALLENGES)))
    return jsonify({'challenges': selected_challenges})

@games_bp.route('/api/games/encryption/check', methods=['POST'])
def check_encryption_game():
    """Проверить ответ в игре шифрования"""
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    user_answer = data.get('answer')
    
    challenge = next((c for c in ENCRYPTION_CHALLENGES if c['id'] == challenge_id), None)
    if not challenge:
        return jsonify({'error': 'Задание не найдено'}), 404
    
    is_correct = (user_answer.strip().upper() == challenge['encrypted_text'])
    score = 100 if is_correct else 0
    
    # Сохраняем результат
    if current_user.is_authenticated:
        game_stats = session.get('game_stats', {})
        encryption_stats = game_stats.get('encryption', {'played': 0, 'won': 0, 'score': 0})
        
        encryption_stats['played'] += 1
        if is_correct:
            encryption_stats['won'] += 1
            encryption_stats['score'] += score
        
        game_stats['encryption'] = encryption_stats
        session['game_stats'] = game_stats
    
    return jsonify({
        'correct': is_correct,
        'score': score,
        'expected': challenge['encrypted_text'],
        'user_answer': user_answer
    })

@games_bp.route('/api/games/encryption/encode', methods=['POST'])
def encode_text():
    """Закодировать текст различными методами"""
    data = request.get_json()
    text = data.get('text')
    method = data.get('method')
    
    result = ""
    
    if method == 'caesar':
        shift = data.get('shift', 3)
        result = ""
        for char in text.upper():
            if char.isalpha():
                shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result += shifted
            else:
                result += char
                
    elif method == 'base64':
        result = base64.b64encode(text.encode()).decode()
        
    elif method == 'hash':
        result = hashlib.sha256(text.encode()).hexdigest()
    
    return jsonify({'encoded': result})

@games_bp.route('/api/games/quiz/questions')
def get_quiz_questions():
    """Получить вопросы для квиза"""
    # Выбираем 10 случайных вопросов из 15
    selected_questions = random.sample(QUIZ_QUESTIONS, min(10, len(QUIZ_QUESTIONS)))
    return jsonify({'questions': selected_questions})

@games_bp.route('/api/games/quiz/check', methods=['POST'])
def check_quiz_game():
    """Проверить ответы в квизе"""
    data = request.get_json()
    user_answers = data.get('answers', {})
    
    total_score = 0
    results = {}
    
    for question_id, user_answer in user_answers.items():
        question = next((q for q in QUIZ_QUESTIONS if q['id'] == int(question_id)), None)
        if question:
            is_correct = (user_answer == question['correct'])
            score = 100 if is_correct else 0
            total_score += score
            
            results[question_id] = {
                'correct': is_correct,
                'explanation': question['explanation'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'question_text': question['question'],
                'options': question['options']
            }
    
    # Сохраняем результат
    if current_user.is_authenticated:
        game_stats = session.get('game_stats', {})
        quiz_stats = game_stats.get('quiz', {'played': 0, 'best_score': 0, 'total_score': 0})
        
        quiz_stats['played'] += 1
        quiz_stats['total_score'] += total_score
        quiz_stats['best_score'] = max(quiz_stats['best_score'], total_score)
        
        game_stats['quiz'] = quiz_stats
        session['game_stats'] = game_stats
    
    return jsonify({
        'total_score': total_score,
        'max_score': len(user_answers) * 100,
        'percentage': int((total_score / (len(user_answers) * 100)) * 100) if user_answers else 0,
        'results': results
    })

@games_bp.route('/api/games/stats')
@login_required
def get_game_stats():
    """Получить статистику игр"""
    game_stats = session.get('game_stats', {})
    
    # Добавляем общую статистику
    total_games = 0
    total_score = 0
    games_won = 0
    
    for game, stats in game_stats.items():
        total_games += stats.get('played', 0)
        total_score += stats.get('score', 0) + stats.get('total_score', 0)
        games_won += stats.get('won', 0)
    
    game_stats['overall'] = {
        'total_games': total_games,
        'total_score': total_score,
        'games_won': games_won,
        'win_rate': int((games_won / total_games * 100)) if total_games > 0 else 0
    }
    
    return jsonify(game_stats)

@games_bp.route('/api/games/leaderboard')
def get_leaderboard():
    """Таблица лидеров"""
    leaders = [
        {'username': 'CyberMaster', 'score': 1250, 'games_played': 15, 'avatar': '👑'},
        {'username': 'SecurityPro', 'score': 980, 'games_played': 12, 'avatar': '🛡️'},
        {'username': 'CryptoKing', 'score': 870, 'games_played': 10, 'avatar': '🔐'},
        {'username': current_user.username if current_user.is_authenticated else 'Вы', 'score': 650, 'games_played': 8, 'avatar': '🎯'},
        {'username': 'DataGuardian', 'score': 540, 'games_played': 7, 'avatar': '🔒'},
        {'username': 'PhishBuster', 'score': 480, 'games_played': 6, 'avatar': '🎣'},
        {'username': 'CodeBreaker', 'score': 420, 'games_played': 5, 'avatar': '💻'}
    ]
    return jsonify({'leaders': leaders})

@games_bp.route('/api/games/reset', methods=['POST'])
@login_required
def reset_game_stats():
    """Сбросить статистику игр"""
    session['game_stats'] = {}
    return jsonify({'success': True, 'message': 'Статистика сброшена'})