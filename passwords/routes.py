from flask import render_template, request, jsonify, session
from flask_login import login_required, current_user
from . import passwords_bp
import secrets
import string
import re
from datetime import datetime

class PasswordGenerator:
    @staticmethod
    def generate_strong_password(length=16):
        """Генерация криптостойкого пароля"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def generate_memorable_password(words=4, separator='-'):
        """Генерация запоминающегося пароля из слов"""
        word_list = [
            'алмаз', 'берёза', 'ветер', 'гора', 'дом', 'еж', 'жар', 'зима',
            'игла', 'йогурт', 'кот', 'луна', 'море', 'ночь', 'огонь', 'песок',
            'река', 'солнце', 'туча', 'утро', 'флаг', 'хлеб', 'цвет', 'час',
            'шар', 'щит', 'эхо', 'юла', 'ящик'
        ]
        return separator.join(secrets.choice(word_list) for _ in range(words))

    @staticmethod
    def check_password_strength(password):
        """Проверка надежности пароля"""
        score = 0
        feedback = []
        
        # Длина пароля
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Пароль слишком короткий")
        
        # Наличие цифр
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Добавьте цифры")
        
        # Наличие символов в верхнем регистре
        if re.search(r'[A-ZА-Я]', password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")
        
        # Наличие специальных символов
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")
        
        # Проверка на common passwords
        common_passwords = ['123456', 'password', 'qwerty', '111111', 'admin']
        if password.lower() in common_passwords:
            score = 0
            feedback.append("Это один из самых ненадежных паролей!")
        
        # Оценка надежности
        if score >= 4:
            strength = "Очень надежный"
            strength_class = "very-strong"
        elif score >= 3:
            strength = "Надежный"
            strength_class = "strong"
        elif score >= 2:
            strength = "Средний"
            strength_class = "medium"
        else:
            strength = "Слабый"
            strength_class = "weak"
        
        return {
            'score': score,
            'strength': strength,
            'strength_class': strength_class,
            'feedback': feedback,
            'length': len(password),
            'entropy': calculate_entropy(password)
        }

def calculate_entropy(password):
    """Вычисление энтропии пароля"""
    char_set = 0
    if any(c in string.ascii_lowercase for c in password):
        char_set += 26
    if any(c in string.ascii_uppercase for c in password):
        char_set += 26
    if any(c in string.digits for c in password):
        char_set += 10
    if any(c in string.punctuation for c in password):
        char_set += 32
    
    if char_set == 0:
        return 0
    
    entropy = len(password) * (char_set ** 0.5)
    return round(entropy, 2)

@passwords_bp.route('/')
def password_generator():
    """Главная страница генератора паролей"""
    return render_template('passwords/generator.html')

@passwords_bp.route('/generate', methods=['POST'])
def generate_password():
    """API для генерации пароля"""
    data = request.get_json()
    password_type = data.get('type', 'strong')
    length = data.get('length', 16)
    
    if password_type == 'strong':
        password = PasswordGenerator.generate_strong_password(length)
    else:
        password = PasswordGenerator.generate_memorable_password()
    
    return jsonify({'password': password})

@passwords_bp.route('/check-strength', methods=['POST'])
def check_password_strength():
    """API для проверки надежности пароля"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Пароль не предоставлен'}), 400
    
    result = PasswordGenerator.check_password_strength(password)
    
    # Сохраняем в историю проверок
    if current_user.is_authenticated:
        session.setdefault('password_checks', []).append({
            'password': '*' * len(password),
            'strength': result['strength'],
            'timestamp': datetime.now().isoformat(),
            'score': result['score']
        })
    
    return jsonify(result)

@passwords_bp.route('/history')
@login_required
def password_history():
    """История проверок паролей"""
    history = session.get('password_checks', [])
    return render_template('passwords/history.html', history=history)

@passwords_bp.route('/analyzer')
def password_analyzer():
    """Расширенный анализатор паролей"""
    return render_template('passwords/analyzer.html')