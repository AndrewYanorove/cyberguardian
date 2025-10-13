from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import random
import time
import re
import requests
import hashlib
import socket
from urllib.parse import urlparse
import subprocess
import platform
import datetime

scanner_bp = Blueprint('scanner', __name__)

class SecurityScanner:
    @staticmethod
    def scan_password_strength(password):
        """Реальное сканирование надежности пароля"""
        if not password:
            return {'error': 'Пароль не указан'}
        
        score = 0
        feedback = []
        
        # Проверка длины
        length = len(password)
        if length >= 16:
            score += 25
            feedback.append("✅ Отличная длина пароля")
        elif length >= 12:
            score += 20
            feedback.append("✅ Хорошая длина пароля")
        elif length >= 8:
            score += 10
            feedback.append("⚠️ Пароль можно сделать длиннее")
        else:
            score += 0
            feedback.append("❌ Слишком короткий пароль")
        
        # Проверка сложности символов
        has_upper = re.search(r'[A-ZА-Я]', password)
        has_lower = re.search(r'[a-zа-я]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>\[\]\\/]', password)
        
        char_types = sum([bool(has_upper), bool(has_lower), bool(has_digit), bool(has_special)])
        
        if char_types == 4:
            score += 30
            feedback.append("✅ Отличное разнообразие символов")
        elif char_types == 3:
            score += 20
            feedback.append("✅ Хорошее разнообразие символов")
        elif char_types == 2:
            score += 10
            feedback.append("⚠️ Добавьте больше типов символов")
        else:
            score += 0
            feedback.append("❌ Используйте разные типы символов")
        
        # Проверка на последовательности и повторения
        if re.search(r'(.)\1{2,}', password):
            score -= 15
            feedback.append("❌ Обнаружены повторяющиеся символы")
        
        if re.search(r'(123|234|345|456|567|678|789|qwe|wer|ert|rty|tyu|yui|uio|iop|asd|sdf|dfg|fgh|ghj|hjk|jkl|zxc|xcv|cvb|vbn|bnm)', password.lower()):
            score -= 20
            feedback.append("❌ Обнаружены последовательности символов")
        
        # Проверка на common passwords (расширенный список)
        common_passwords = [
            '123456', 'password', '12345678', 'qwerty', '123456789', '12345', 
            '1234', '111111', '1234567', 'dragon', '123123', 'baseball', 
            'abc123', 'football', 'monkey', 'letmein', '696969', 'shadow',
            'master', '666666', 'qwertyuiop', '123321', 'mustang', '1234567890',
            'michael', '654321', 'superman', '1qaz2wsx', '7777777', 'fuckyou',
            '121212', '000000', 'qazwsx', '123qwe', 'killer', 'trustno1',
            'jordan', 'jennifer', 'zxcvbnm', 'asdfgh', 'hunter', 'buster',
            'soccer', 'harley', 'batman', 'andrew', 'tigger', 'sunshine',
            'iloveyou', 'fuckme', '2000', 'charlie', 'robert', 'thomas',
            'hockey', 'ranger', 'daniel', 'starwars', 'klaster', '112233',
            'george', 'asshole', 'computer', 'michelle', 'jessica', 'pepper',
            '1111', 'zxcvbn', '555555', '11111111', '131313', 'freedom',
            '777777', 'pass', 'fuck', 'maggie', '159753', 'aaaaaa', 'ginger',
            'princess', 'joshua', 'cheese', 'amanda', 'summer', 'love',
            'ashley', '6969', 'nicole', 'chelsea', 'biteme', 'matthew',
            'access', 'yankees', '987654321', 'dallas', 'austin', 'thunder',
            'taylor', 'matrix', 'minecraft', 'admin', 'password1'
        ]
        
        if password.lower() in common_passwords:
            score = 10
            feedback = ["🚨 ОДИН ИЗ САМЫХ НЕНАДЕЖНЫХ ПАРОЛЕЙ! Немедленно смените!"]
        
        # Энтропия пароля
        entropy = SecurityScanner.calculate_entropy(password)
        if entropy >= 80:
            score += 25
            feedback.append("✅ Отличная энтропия пароля")
        elif entropy >= 60:
            score += 20
            feedback.append("✅ Хорошая энтропия пароля")
        elif entropy >= 40:
            score += 10
            feedback.append("⚠️ Энтропия пароля можно улучшить")
        else:
            score += 0
            feedback.append("❌ Низкая энтропия пароля")
        
        # Ограничение score от 0 до 100
        score = max(0, min(100, score))
        
        # Определение уровня безопасности
        if score >= 90:
            strength = "Отличная"
            color = "success"
        elif score >= 75:
            strength = "Хорошая"
            color = "info"
        elif score >= 60:
            strength = "Средняя"
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
            'crack_time': SecurityScanner.calculate_crack_time(score, length, char_types),
            'entropy': entropy,
            'length': length,
            'char_types': char_types
        }
    
    @staticmethod
    def calculate_entropy(password):
        """Расчет энтропии пароля"""
        if not password:
            return 0
            
        # Определяем размер алфавита
        char_set = 0
        if re.search(r'[a-z]', password):
            char_set += 26
        if re.search(r'[A-Z]', password):
            char_set += 26
        if re.search(r'\d', password):
            char_set += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            char_set += 33  # Специальные символы
        
        if char_set == 0:
            return 0
            
        entropy = len(password) * (char_set.bit_length())
        return min(100, entropy)
    
    @staticmethod
    def calculate_crack_time(score, length, char_types):
        """Реальный расчет времени взлома"""
        base_time = 0.001  # базовое время в секундах
        
        # Факторы влияния
        length_factor = 2 ** (length - 6)  # Экспоненциальная зависимость от длины
        complexity_factor = 10 ** (char_types - 1)  # Зависимость от разнообразия символов
        score_factor = (score / 20) ** 3  # Зависимость от общего score
        
        total_time = base_time * length_factor * complexity_factor * score_factor
        
        # Конвертация в читаемый формат
        if total_time < 1:
            return "Менее секунды"
        elif total_time < 60:
            return f"{int(total_time)} секунд"
        elif total_time < 3600:
            return f"{int(total_time/60)} минут"
        elif total_time < 86400:
            return f"{int(total_time/3600)} часов"
        elif total_time < 31536000:
            return f"{int(total_time/86400)} дней"
        elif total_time < 315360000:
            return f"{int(total_time/31536000)} лет"
        else:
            return "Сотни лет"
    
    @staticmethod
    def scan_email_security(email):
        """Проверка безопасности email (без внешних DNS запросов)"""
        if not email or '@' not in email:
            return {'error': 'Некорректный email'}
        
        issues = []
        recommendations = []
        score = 100  # Начинаем с идеального score
        
        try:
            domain = email.split('@')[-1]
            
            # Упрощенная проверка без внешних DNS запросов
            # Проверка формата email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                issues.append("❌ Некорректный формат email")
                score -= 20
            
            # Проверка домена на известные провайдеры
            secure_providers = ['gmail.com', 'protonmail.com', 'tutanota.com', 'outlook.com', 'yahoo.com']
            medium_providers = ['yandex.ru', 'mail.ru', 'rambler.ru', 'hotmail.com']
            
            if domain in secure_providers:
                recommendations.append("✅ Надежный почтовый провайдер")
                recommendations.append("✅ Вероятно настроены SPF/DKIM/DMARC")
            elif domain in medium_providers:
                recommendations.append("⚠️ Стандартный почтовый провайдер")
                recommendations.append("💡 Проверьте настройки SPF/DKIM/DMARC")
                score -= 5
            else:
                issues.append("💡 Проверьте надежность почтового провайдера")
                recommendations.append("💡 Настройте SPF, DKIM и DMARC записи")
                score -= 10
            
            # Базовые рекомендации для всех
            recommendations.extend([
                "Включите двухфакторную аутентификацию",
                "Используйте надежный уникальный пароль",
                "Регулярно проверяйте активность аккаунта"
            ])
            
            # Проверка на утечки (имитация)
            leaked_domains = ['example.com', 'test.com', 'hacked-domain.com']
            if domain in leaked_domains:
                issues.append("🚨 Домен присутствует в известных утечках (тест)")
                score -= 25
                recommendations.append("Немедленно смените пароль и включите 2FA")
            
        except Exception as e:
            issues.append(f"❌ Ошибка проверки: {str(e)}")
            score -= 20
        
        # Балансировка score
        score = max(0, min(100, score))
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'score': score,
            'domain': domain
        }
    
    @staticmethod
    def network_scan(target):
        """Сканирование сети с обработкой ошибок"""
        if not target:
            target = "127.0.0.1"
        
        # Очистка target от протоколов
        target = target.replace('http://', '').replace('https://', '').split('/')[0]
        
        ports = []
        vulnerabilities = []
        
        # Стандартные порты для проверки
        common_ports = [
            (21, 'FTP', 'high'),
            (22, 'SSH', 'medium'),
            (23, 'Telnet', 'critical'),
            (25, 'SMTP', 'medium'),
            (53, 'DNS', 'medium'),
            (80, 'HTTP', 'low'),
            (110, 'POP3', 'medium'),
            (143, 'IMAP', 'medium'),
            (443, 'HTTPS', 'low'),
            (993, 'IMAPS', 'medium'),
            (995, 'POP3S', 'medium'),
            (1433, 'MSSQL', 'high'),
            (3306, 'MySQL', 'high'),
            (3389, 'RDP', 'critical'),
            (5432, 'PostgreSQL', 'high'),
            (5900, 'VNC', 'critical'),
            (6379, 'Redis', 'high'),
            (27017, 'MongoDB', 'high')
        ]
        
        # Сканирование портов с обработкой ошибок
        open_ports_count = 0
        for port, service, risk in common_ports:
            try:
                is_open = SecurityScanner.check_port(target, port)
                status = 'open' if is_open else 'closed'
                
                if is_open:
                    open_ports_count += 1
                    # Добавляем уязвимости для открытых портов
                    if risk == 'critical':
                        vulnerabilities.append(f"Открыт критический порт {port} ({service})")
                    elif risk == 'high':
                        vulnerabilities.append(f"Открыт высокорисковый порт {port} ({service})")
                
                ports.append({
                    'port': port,
                    'service': service,
                    'status': status,
                    'security': risk if is_open else 'low'
                })
            except Exception as e:
                # Если сканирование порта не удалось, добавляем его как закрытый
                ports.append({
                    'port': port,
                    'service': service,
                    'status': 'unknown',
                    'security': 'low'
                })
        
        # Расчет общего score безопасности
        security_score = max(10, 100 - (open_ports_count * 5))
        
        # Дополнительные проверки (с обработкой ошибок)
        try:
            if SecurityScanner.check_port(target, 3389):  # RDP
                vulnerabilities.append("Открыт порт RDP (3389) - высокий риск")
                security_score -= 20
        except:
            pass
            
        try:
            if SecurityScanner.check_port(target, 23):  # Telnet
                vulnerabilities.append("Открыт порт Telnet (23) - критический риск")
                security_score -= 25
        except:
            pass
            
        try:
            if SecurityScanner.check_port(target, 21):  # FTP
                vulnerabilities.append("Открыт порт FTP (21) - данные передаются в открытом виде")
                security_score -= 15
        except:
            pass
        
        # Рекомендации
        recommendations = []
        if open_ports_count > 10:
            recommendations.append("Слишком много открытых портов - закройте неиспользуемые")
        if any(p['port'] == 80 and p['status'] == 'open' for p in ports) and not any(p['port'] == 443 and p['status'] == 'open' for p in ports):
            recommendations.append("HTTP доступен без HTTPS - настроить SSL")
        if vulnerabilities:
            recommendations.append("Обновите ПО и настройки безопасности")
        
        recommendations.extend([
            'Настройте брандмауэр',
            'Используйте сложные пароли для сервисов',
            'Регулярно обновляйте ПО'
        ])
        
        return {
            'ports': ports,
            'vulnerabilities': vulnerabilities,
            'security_score': max(0, security_score),
            'recommendations': recommendations,
            'target': target,
            'open_ports': open_ports_count
        }
    
    @staticmethod
    def check_port(host, port, timeout=2):
        """Проверка доступности порта с обработкой ошибок"""
        try:
            # Пытаемся преобразовать host в IP адрес
            try:
                ip = socket.gethostbyname(host)
            except socket.gaierror:
                return False
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                return result == 0
        except:
            return False

    @staticmethod
    def quick_system_scan():
        """Быстрое сканирование системы (кроссплатформенное)"""
        security_issues = []
        recommendations = []
        
        try:
            # Проверка операционной системы
            system = platform.system()
            recommendations.append(f"Обнаружена ОС: {system}")
            
            # Общие проверки для всех систем
            try:
                # Проверка использования памяти (индикатор подозрительной активности)
                import psutil
                memory_percent = psutil.virtual_memory().percent
                if memory_percent > 90:
                    security_issues.append(f"Высокая загрузка памяти: {memory_percent}%")
            except ImportError:
                # psutil не установлен - пропускаем эту проверку
                pass
            
            # Проверка версии Python (устаревшие версии могут иметь уязвимости)
            python_version = platform.python_version()
            if tuple(map(int, python_version.split('.'))) < (3, 7):
                security_issues.append(f"Используется устаревшая версия Python: {python_version}")
                recommendations.append("Обновите Python до актуальной версии")
            
            # Проверка на наличие известных уязвимостей в зависимостях
            # (здесь можно добавить проверку через safety или аналогичные инструменты)
            
        except Exception as e:
            security_issues.append(f"Ошибка при сканировании системы: {str(e)}")
        
        # Универсальные рекомендации
        recommendations.extend([
            'Регулярно обновляйте операционную систему',
            'Используйте антивирусное ПО',
            'Включите брандмауэр',
            'Делайте резервные копии важных данных'
        ])
        
        # Расчет общего score
        base_score = 80
        score_deduction = len(security_issues) * 10
        system_security = max(20, base_score - score_deduction)
        
        # Сетевой score (случайный, но зависит от проблем)
        network_security = max(30, system_security - random.randint(0, 20))
        
        # Password security (случайный)
        password_security = random.randint(40, 90)
        
        return {
            'system_security': system_security,
            'network_security': network_security,
            'password_security': password_security,
            'threats_found': len(security_issues),
            'security_issues': security_issues,
            'recommendations': recommendations if recommendations else [
                'Система в хорошем состоянии',
                'Продолжайте регулярно обновлять ПО',
                'Используйте менеджер паролей'
            ]
        }

# Маршруты
@scanner_bp.route('/')
@login_required
def scanner_dashboard():
    return render_template('security_scanner/dashboard.html')

@scanner_bp.route('/password')
@login_required
def password_scanner():
    return render_template('security_scanner/password.html')

@scanner_bp.route('/email')
@login_required
def email_scanner():
    return render_template('security_scanner/email.html')

@scanner_bp.route('/network')
@login_required
def network_scanner():
    return render_template('security_scanner/network.html')

@scanner_bp.route('/vulnerabilities')
@login_required
def vulnerability_scanner():
    return render_template('security_scanner/vulnerabilities.html')

# API endpoints
@scanner_bp.route('/api/scan/password', methods=['POST'])
def scan_password():
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Пароль не указан'}), 400
    
    result = SecurityScanner.scan_password_strength(password)
    return jsonify(result)

@scanner_bp.route('/api/scan/email', methods=['POST'])
def scan_email():
    data = request.get_json()
    email = data.get('email', '')
    
    if not email or '@' not in email:
        return jsonify({'error': 'Некорректный email'}), 400
    
    result = SecurityScanner.scan_email_security(email)
    return jsonify(result)

@scanner_bp.route('/api/scan/network', methods=['POST'])
def scan_network():
    data = request.get_json()
    target = data.get('target', '127.0.0.1')
    
    result = SecurityScanner.network_scan(target)
    return jsonify(result)

@scanner_bp.route('/api/scan/quick')
def quick_scan():
    result = SecurityScanner.quick_system_scan()
    return jsonify(result)