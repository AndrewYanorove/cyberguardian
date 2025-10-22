from flask import render_template, request, jsonify, session
from flask_login import login_required, current_user
from . import passwords_bp
import secrets
import string
import re
import math
import json
from datetime import datetime
from collections import Counter
import hashlib

class PasswordGenerator:
    @staticmethod
    def generate_strong_password(length=16, include_special=True, include_numbers=True):
        """Генерация криптостойкого пароля с расширенными настройками"""
        if length < 4:
            length = 4
            
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits if include_numbers else ""
        punctuation = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_special else ""
        
        # Гарантируем минимум по одному символу каждого типа
        password_parts = [secrets.choice(lowercase), secrets.choice(uppercase)]
        
        if include_numbers:
            password_parts.append(secrets.choice(digits))
        if include_special:
            password_parts.append(secrets.choice(punctuation))
        
        # Заполняем оставшуюся длину
        all_chars = lowercase + uppercase + digits + punctuation
        for _ in range(length - len(password_parts)):
            password_parts.append(secrets.choice(all_chars))
        
        # Перемешиваем пароль
        secrets.SystemRandom().shuffle(password_parts)
        return ''.join(password_parts)

    @staticmethod
    def generate_memorable_password(word_count=4, separator='-', capitalize=True, add_number=True):
        """Генерация запоминающегося пароля с настройками"""
        word_list = [
            'алмаз', 'берёза', 'ветер', 'гора', 'дом', 'еж', 'жар', 'зима',
            'игла', 'йог', 'кот', 'луна', 'море', 'ночь', 'огонь', 'песок',
            'река', 'солнце', 'туча', 'утро', 'флаг', 'хлеб', 'цвет', 'час',
            'шар', 'щит', 'эхо', 'юла', 'ящик', 'ключ', 'фон', 'свет', 'тень',
            'путь', 'мечта', 'сила', 'дух', 'край', 'поле', 'лес', 'речь',
            'тайна', 'волна', 'искра', 'пламя', 'небо', 'земля', 'вода', 'воздух'
        ]
        
        words = [secrets.choice(word_list) for _ in range(word_count)]
        
        if capitalize:
            words = [word.capitalize() for word in words]
            
        password = separator.join(words)
        
        if add_number and secrets.randbelow(2):
            password += str(secrets.randbelow(90) + 10)
            
        return password

    @staticmethod
    def generate_phonetic_password(length=8):
        """Генерация фонетического пароля (легко произносимого)"""
        consonants = 'bcdfghjklmnpqrstvwxz'
        vowels = 'aeiou'
        
        password = []
        for i in range(length):
            if i % 2 == 0:
                password.append(secrets.choice(consonants))
            else:
                password.append(secrets.choice(vowels))
        
        # Случайно делаем некоторые буквы заглавными
        for i in range(len(password)):
            if secrets.randbelow(4) == 0:  # 25% chance
                password[i] = password[i].upper()
                
        return ''.join(password)

    @staticmethod
    def check_password_strength(password):
        """РЕАЛИСТИЧНАЯ проверка надежности пароля"""
        if not password:
            return {
                'score': 0,
                'strength': 'Пустой пароль',
                'strength_class': 'critical',
                'feedback': ['Пароль не может быть пустым'],
                'length': 0,
                'entropy': 0,
                'crack_time': 'мгновенно',
                'score_percent': 0,
                'details': {}
            }
            
        score = 0
        max_score = 100  # Теперь 100-балльная система
        feedback = []
        details = {}

        # Анализ длины
        length = len(password)
        details['length'] = length
        
        # Баллы за длину (максимум 40 баллов)
        if length >= 20:
            score += 40
        elif length >= 16:
            score += 35
        elif length >= 14:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 10:
            score += 20
        elif length >= 8:
            score += 15
            feedback.append("Рекомендуется использовать не менее 12 символов")
        else:
            score += 5
            feedback.append("Пароль очень короткий (минимум 8 символов)")

        # Анализ разнообразия символов (максимум 40 баллов)
        char_categories = {
            'lowercase': bool(re.search(r'[a-zа-я]', password)),
            'uppercase': bool(re.search(r'[A-ZА-Я]', password)),
            'digits': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        }
        
        details['char_categories'] = char_categories
        
        category_count = sum(char_categories.values())
        # 10 баллов за каждый тип символов
        score += category_count * 10
        
        if not char_categories['lowercase']:
            feedback.append("Добавьте строчные буквы")
        if not char_categories['uppercase']:
            feedback.append("Добавьте заглавные буквы")
        if not char_categories['digits']:
            feedback.append("Добавьте цифры")
        if not char_categories['special']:
            feedback.append("Добавьте специальные символы")

        # Проверка на общие паттерны и слабости (штрафы)
        patterns_found = []
        penalty = 0
        
        # Общие последовательности
        sequences = ['123', 'abc', 'qwe', 'йцу', 'password', 'admin', 'qwerty', '123456', '111111']
        for seq in sequences:
            if seq in password.lower():
                patterns_found.append(seq)
                penalty += 15  # Большой штраф за очевидные последовательности
        
        # Повторяющиеся символы
        if re.search(r'(.)\1{3,}', password):  # 4+ повторяющихся символов
            patterns_found.append("повторяющиеся символы")
            penalty += 10
            
        # Только цифры
        if password.isdigit():
            patterns_found.append("только цифры")
            penalty += 20
            
        # Только буквы
        if password.isalpha():
            patterns_found.append("только буквы")
            penalty += 15
        
        # Простые шаблоны (дата, телефон и т.д.)
        if re.match(r'^\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4}$', password):
            patterns_found.append("шаблон даты")
            penalty += 15
            
        if re.match(r'^\+?[\d\s\-\(\)]{7,15}$', password):
            patterns_found.append("шаблон телефона")
            penalty += 15
        
        details['patterns'] = patterns_found

        # Проверка на common passwords (критический штраф)
        common_passwords = [
            '123456', 'password', 'qwerty', '111111', 'admin', '12345678', 
            '123123', '123456789', '1234567', '12345', '1234567890',
            '000000', 'abc123', 'password1', 'monkey', '1234', 'qwerty123'
        ]
        if password.lower() in common_passwords:
            penalty = 100  # Полный обнул за популярный пароль
            feedback = ["⚠️ КРИТИЧЕСКИЙ РИСК: Этот пароль в топе самых ненадежных!"]
            details['common_password'] = True
        else:
            details['common_password'] = False

        # Применяем штрафы
        score = max(0, score - penalty)

        # Бонусы за сложность (максимум 20 баллов)
        # Уникальность символов
        unique_chars = len(set(password))
        uniqueness_ratio = unique_chars / length
        details['unique_chars'] = unique_chars
        
        if uniqueness_ratio > 0.9:
            score += 10
        elif uniqueness_ratio > 0.7:
            score += 5
        elif uniqueness_ratio < 0.5:
            feedback.append("Много повторяющихся символов")
            score -= 5

        # Отсутствие словарных слов
        if not any(word in password.lower() for word in ['password', 'admin', 'qwerty', '123']):
            score += 5

        # Случайность распределения символов
        if length >= 8 and not is_too_predictable(password):
            score += 5

        # Энтропия и время взлома
        entropy = calculate_realistic_entropy(password)
        crack_time = calculate_realistic_crack_time(entropy, length)
        details['entropy'] = entropy
        details['crack_time'] = crack_time

        # Ограничиваем score
        score = max(0, min(max_score, score))
        score_percent = int(score)

        # РЕАЛИСТИЧНАЯ оценка надежности
        if score_percent >= 90:
            strength = "ИДЕАЛЬНЫЙ"
            strength_class = "perfect"
        elif score_percent >= 80:
            strength = "ОЧЕНЬ НАДЕЖНЫЙ"
            strength_class = "very-strong"
        elif score_percent >= 70:
            strength = "НАДЕЖНЫЙ"
            strength_class = "strong"
        elif score_percent >= 50:
            strength = "СРЕДНИЙ"
            strength_class = "medium"
        elif score_percent >= 30:
            strength = "СЛАБЫЙ"
            strength_class = "weak"
        else:
            strength = "ОПАСНЫЙ"
            strength_class = "critical"

        return {
            'score': score,
            'score_percent': score_percent,
            'strength': strength,
            'strength_class': strength_class,
            'feedback': feedback,
            'length': length,
            'entropy': entropy,
            'crack_time': crack_time,
            'details': details
        }

def calculate_realistic_entropy(password):
    """Реалистичное вычисление энтропии пароля в битах"""
    if not password:
        return 0
        
    char_set = 0
    # Английские буквы
    if any(c in string.ascii_lowercase for c in password):
        char_set += 26
    if any(c in string.ascii_uppercase for c in password):
        char_set += 26
    # Цифры
    if any(c in string.digits for c in password):
        char_set += 10
    # Спецсимволы (расширенный набор)
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    if any(c in special_chars for c in password):
        char_set += 33
    # Кириллица
    if any('\u0400' <= c <= '\u04FF' for c in password):
        char_set += 66
    
    if char_set == 0:
        return 0
    
    entropy = len(password) * math.log2(char_set)
    return round(entropy, 1)

def calculate_realistic_crack_time(entropy, length):
    """РЕАЛИСТИЧНЫЙ расчет времени взлома пароля"""
    # Современные хэш-каталки: 
    # - MD5: ~100 GH/s (10^11) на хорошем GPU
    # - bcrypt: ~10k H/s (10^4)
    # - Argon2: ~1k H/s (10^3)
    # Берем среднее для хэширования с солью: 10^6 попыток в секунду
    
    guesses_per_second = 10**6  # 1 миллион попыток в секунду (реалистично для защищенных систем)
    
    # Для онлайн-атак еще меньше
    online_guesses_per_second = 10  # 10 попыток в секунду (ограничения сервера)
    
    total_guesses = 2 ** entropy
    
    # Время для офлайн-атаки (более реалистичная угроза)
    seconds_offline = total_guesses / guesses_per_second
    seconds_online = total_guesses / online_guesses_per_second
    
    # Используем офлайн-атаку как основной сценарий
    seconds = seconds_offline
    
    if seconds < 1:
        return "менее секунды"
    elif seconds < 60:
        return "несколько секунд"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} минут" if minutes > 1 else "менее минуты"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} часов" if hours > 1 else "около часа"
    elif seconds < 2592000:  # 30 дней
        days = int(seconds / 86400)
        if days < 7:
            return f"{days} дней"
        else:
            weeks = days // 7
            return f"{weeks} недель" if weeks > 1 else "около недели"
    elif seconds < 31536000:  # год
        months = int(seconds / 2592000)
        return f"{months} месяцев" if months > 1 else "около месяца"
    elif seconds < 315360000:  # 10 лет
        years = int(seconds / 31536000)
        return f"{years} лет" if years > 1 else "около года"
    elif seconds < 3153600000:  # 100 лет
        return "десятилетия"
    elif seconds < 31536000000:  # 1000 лет
        return "столетия"
    else:
        return "тысячелетия"

def is_too_predictable(password):
    """Проверка на предсказуемость пароля"""
    # Проверка простых последовательностей
    sequences = [
        '123456', 'abcdef', 'qwerty', 'йцукен', 'asdfgh', 'zxcvbn'
    ]
    
    for seq in sequences:
        if seq in password.lower():
            return True
    
    # Проверка на клавиатурные шаблоны
    keyboard_patterns = [
        r'(.)\1{2,}',  # повторяющиеся символы
        r'[a-z]{4,}',   # только строчные
        r'[A-Z]{4,}',   # только заглавные
        r'\d{4,}',      # только цифры
    ]
    
    for pattern in keyboard_patterns:
        if re.search(pattern, password):
            return True
    
    return False

@passwords_bp.route('/')
def password_generator():
    """Главная страница генератора паролей"""
    return render_template('passwords/generator.html')

@passwords_bp.route('/generate', methods=['POST'])
def generate_password():
    """API для генерации пароля с расширенными настройками"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        password_type = data.get('type', 'strong')
        length = int(data.get('length', 16))
        options = data.get('options', {})
        
        if password_type == 'strong':
            password = PasswordGenerator.generate_strong_password(
                length=length,
                include_special=options.get('special', True),
                include_numbers=options.get('numbers', True)
            )
        elif password_type == 'memorable':
            password = PasswordGenerator.generate_memorable_password(
                word_count=max(3, min(6, length // 4)),
                capitalize=options.get('capitalize', True),
                add_number=options.get('add_number', True)
            )
        elif password_type == 'phonetic':
            password = PasswordGenerator.generate_phonetic_password(length)
        else:
            return jsonify({'error': 'Unknown password type'}), 400
        
        return jsonify({
            'password': password,
            'type': password_type,
            'length': len(password)
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка генерации: {str(e)}'}), 500

@passwords_bp.route('/check-strength', methods=['POST'])
def check_password_strength():
    """API для проверки надежности пароля"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        password = data.get('password', '')
        
        result = PasswordGenerator.check_password_strength(password)
        
        # Сохраняем в историю проверок (без реального пароля)
        if current_user.is_authenticated:
            password_checks = session.get('password_checks', [])
            password_checks.append({
                'password_mask': '*' * len(password) if password else '',
                'strength': result['strength'],
                'strength_class': result['strength_class'],
                'timestamp': datetime.now().isoformat(),
                'score': result['score'],
                'length': result['length'],
                'crack_time': result['crack_time']
            })
            # Ограничиваем историю последними 20 проверками
            session['password_checks'] = password_checks[-20:]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Ошибка проверки: {str(e)}'}), 500

@passwords_bp.route('/advanced-analysis', methods=['POST'])
def advanced_analysis():
    """Расширенный анализ пароля"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({'error': 'Password required'}), 400
            
        analysis = {
            'length': len(password),
            'character_distribution': dict(Counter(password)),
            'unique_chars': len(set(password)),
            'repeats': len(password) - len(set(password)),
            'digit_count': sum(c.isdigit() for c in password),
            'letter_count': sum(c.isalpha() for c in password),
            'special_count': sum(not c.isalnum() for c in password),
            'uppercase_count': sum(c.isupper() for c in password),
            'lowercase_count': sum(c.islower() for c in password),
        }
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@passwords_bp.route('/history')
@login_required
def password_history():
    """История проверок паролей"""
    history = session.get('password_checks', [])
    stats = {
        'total_checks': len(history),
        'strong_count': len([h for h in history if h['strength_class'] in ['strong', 'very-strong', 'perfect']]),
        'average_score': sum(h['score'] for h in history) / len(history) if history else 0
    }
    return render_template('passwords/history.html', history=history, stats=stats)

@passwords_bp.route('/analyzer')
def password_analyzer():
    """Расширенный анализатор паролей"""
    return render_template('passwords/analyzer.html')
