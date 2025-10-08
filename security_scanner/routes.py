from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import random
import time
import re

scanner_bp = Blueprint('scanner', __name__)

class SecurityScanner:
    @staticmethod
    def scan_password_strength(password):
        """Сканирование надежности пароля"""
        score = 0
        feedback = []
        
        # Проверка длины
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        else:
            feedback.append("❌ Слишком короткий пароль")
        
        # Проверка сложности
        if re.search(r'[A-Z]', password):
            score += 20
        else:
            feedback.append("⚠️ Добавьте заглавные буквы")
        
        if re.search(r'[a-z]', password):
            score += 20
        else:
            feedback.append("⚠️ Добавьте строчные буквы")
        
        if re.search(r'\d', password):
            score += 20
        else:
            feedback.append("⚠️ Добавьте цифры")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 15
        else:
            feedback.append("💡 Добавьте специальные символы")
        
        # Проверка на common passwords
        common_passwords = ['123456', 'password', 'qwerty', '111111', 'admin']
        if password.lower() in common_passwords:
            score = 0
            feedback = ["🚨 Один из самых ненадежных паролей!"]
        
        # Определение уровня безопасности
        if score >= 80:
            strength = "Отличная"
            color = "success"
        elif score >= 60:
            strength = "Хорошая"
            color = "warning"
        elif score >= 40:
            strength = "Слабая"
            color = "danger"
        else:
            strength = "Очень слабая"
            color = "dark"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'crack_time': SecurityScanner.calculate_crack_time(score)
        }
    
    @staticmethod
    def calculate_crack_time(score):
        """Расчет времени взлома"""
        if score >= 80:
            return "Сотни лет"
        elif score >= 60:
            return "Несколько лет"
        elif score >= 40:
            return "Несколько дней"
        elif score >= 20:
            return "Несколько часов"
        else:
            return "Мгновенно"
    
    @staticmethod
    def scan_email_security(email):
        """Проверка безопасности email"""
        issues = []
        recommendations = []
        
        # Проверка на утечки (демо)
        leaked_emails = ['test@example.com', 'demo@mail.ru']
        if email in leaked_emails:
            issues.append("⚠️ Обнаружена в утечках данных")
            recommendations.append("Смените пароль для этого email")
        
        # Проверка домена
        domain = email.split('@')[-1]
        if domain in ['gmail.com', 'yandex.ru', 'mail.ru']:
            recommendations.append("✅ Используется надежный почтовый провайдер")
        else:
            issues.append("💡 Проверьте надежность почтового провайдера")
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'score': 80 if not issues else 60
        }
    
    @staticmethod
    def network_scan(target):
        """Сканирование сети (демо)"""
        time.sleep(2)  # Имитация сканирования
        
        ports = [
            {'port': 22, 'service': 'SSH', 'status': 'open', 'security': 'medium'},
            {'port': 80, 'service': 'HTTP', 'status': 'open', 'security': 'low'},
            {'port': 443, 'service': 'HTTPS', 'status': 'open', 'security': 'high'},
            {'port': 21, 'service': 'FTP', 'status': 'closed', 'security': 'high'},
            {'port': 3389, 'service': 'RDP', 'status': 'open', 'security': 'critical'}
        ]
        
        vulnerabilities = [
            'Устаревшая версия SSL',
            'Открытый порт RDP',
            'Слабые настройки шифрования'
        ]
        
        return {
            'ports': ports,
            'vulnerabilities': vulnerabilities,
            'security_score': 65,
            'recommendations': [
                'Закройте ненужные порты',
                'Обновите SSL сертификаты',
                'Настройте брандмауэр'
            ]
        }

@scanner_bp.route('/')
@login_required
def scanner_dashboard():
    """Главная страница сканера"""
    return render_template('security_scanner/dashboard.html')

@scanner_bp.route('/password')
@login_required
def password_scanner():
    """Сканер паролей"""
    return render_template('security_scanner/password.html')

@scanner_bp.route('/email')
@login_required
def email_scanner():
    """Сканер email безопасности"""
    return render_template('security_scanner/email.html')

@scanner_bp.route('/network')
@login_required
def network_scanner():
    """Сканер сети"""
    return render_template('security_scanner/network.html')

@scanner_bp.route('/vulnerabilities')
@login_required
def vulnerability_scanner():
    """Сканер уязвимостей"""
    return render_template('security_scanner/vulnerabilities.html')

# API endpoints
@scanner_bp.route('/api/scan/password', methods=['POST'])
def scan_password():
    """API сканирования пароля"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Пароль не указан'}), 400
    
    result = SecurityScanner.scan_password_strength(password)
    return jsonify(result)

@scanner_bp.route('/api/scan/email', methods=['POST'])
def scan_email():
    """API сканирования email"""
    data = request.get_json()
    email = data.get('email', '')
    
    if not email or '@' not in email:
        return jsonify({'error': 'Некорректный email'}), 400
    
    result = SecurityScanner.scan_email_security(email)
    return jsonify(result)

@scanner_bp.route('/api/scan/network', methods=['POST'])
def scan_network():
    """API сканирования сети"""
    data = request.get_json()
    target = data.get('target', '192.168.1.1')
    
    result = SecurityScanner.network_scan(target)
    return jsonify(result)

@scanner_bp.route('/api/scan/quick')
def quick_scan():
    """Быстрое сканирование системы"""
    time.sleep(1)  # Имитация сканирования
    
    return jsonify({
        'system_security': random.randint(60, 95),
        'network_security': random.randint(50, 90),
        'password_security': random.randint(40, 85),
        'threats_found': random.randint(0, 3),
        'recommendations': [
            'Обновите антивирусные базы',
            'Проверьте настройки брандмауэра',
            'Создайте резервные копии данных'
        ]
    })
