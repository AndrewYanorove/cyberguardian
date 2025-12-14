"""
🛡️ СИСТЕМА ОГРАНИЧЕНИЯ СКОРОСТИ И УЛУЧШЕННАЯ АУТЕНТИФИКАЦИЯ
CyberGuardian - Защита от DDoS и Brute Force атак
"""

import time
import hashlib
import secrets
import pyotp
import qrcode
from io import BytesIO
import base64
from typing import Dict, Optional, Tuple
from flask import request, session, g, abort, jsonify, render_template_string
from functools import wraps
from datetime import datetime, timedelta
import sqlite3
import os
import re
from collections import defaultdict, deque

class RateLimiter:
    """🚦 Система ограничения скорости запросов"""
    
    def __init__(self):
        self.request_counts = defaultdict(deque)  # {ip: [timestamps]}
        self.blocked_ips = {}  # {ip: {blocked_until, reason}}
        self.rate_limits = {
            'general': {'requests': 100, 'window': 3600},      # 100 запросов в час
            'login': {'requests': 5, 'window': 900},           # 5 попыток входа в 15 минут
            'register': {'requests': 3, 'window': 3600},       # 3 регистрации в час
            'api': {'requests': 1000, 'window': 3600},         # 1000 API запросов в час
            'upload': {'requests': 10, 'window': 3600},        # 10 загрузок в час
        }
    
    def is_rate_limited(self, ip: str, limit_type: str = 'general') -> bool:
        """Проверка ограничений скорости"""
        current_time = time.time()
        limit_config = self.rate_limits.get(limit_type, self.rate_limits['general'])
        max_requests = limit_config['requests']
        window_seconds = limit_config['window']
        
        # Проверяем, не заблокирован ли IP
        if ip in self.blocked_ips:
            blocked_info = self.blocked_ips[ip]
            if current_time < blocked_info['blocked_until']:
                return True
            else:
                # Убираем истекшую блокировку
                del self.blocked_ips[ip]
        
        # Получаем список временных меток для этого IP
        timestamps = self.request_counts[ip]
        
        # Удаляем старые временные метки
        while timestamps and current_time - timestamps[0] > window_seconds:
            timestamps.popleft()
        
        # Проверяем лимит
        if len(timestamps) >= max_requests:
            # Блокируем IP
            block_duration = 3600  # 1 час блокировки
            self.blocked_ips[ip] = {
                'blocked_until': current_time + block_duration,
                'reason': f'Превышен лимит {limit_type}: {len(timestamps)}/{max_requests}'
            }
            return True
        
        # Добавляем текущую временную метку
        timestamps.append(current_time)
        return False
    
    def get_rate_limit_info(self, ip: str, limit_type: str = 'general') -> Dict:
        """Получение информации о лимитах для IP"""
        current_time = time.time()
        limit_config = self.rate_limits.get(limit_type, self.rate_limits['general'])
        max_requests = limit_config['requests']
        window_seconds = limit_config['window']
        
        timestamps = self.request_counts[ip]
        
        # Считаем активные запросы (не старше окна)
        active_requests = len([t for t in timestamps if current_time - t <= window_seconds])
        
        # Вычисляем время до сброса
        reset_time = max(timestamps) if timestamps else current_time
        time_to_reset = max(0, (reset_time + window_seconds) - current_time)
        
        return {
            'current_requests': active_requests,
            'max_requests': max_requests,
            'window_seconds': window_seconds,
            'time_to_reset': time_to_reset,
            'remaining_requests': max(0, max_requests - active_requests),
            'is_blocked': self.is_rate_limited(ip, limit_type)
        }

class TwoFactorAuth:
    """🔐 Двухфакторная аутентификация (2FA)"""
    
    def __init__(self):
        self.secret_keys = {}  # {user_id: secret_key}
        self.backup_codes = {}  # {user_id: [backup_codes]}
    
    def generate_secret_key(self) -> str:
        """Генерация секретного ключа для 2FA"""
        return pyotp.random_base32()
    
    def get_qr_code(self, user_email: str, secret_key: str) -> str:
        """Получение QR кода для настройки 2FA"""
        totp = pyotp.TOTP(secret_key)
        provisioning_uri = totp.provisioning_uri(
            name=user_email,
            issuer_name="CyberGuardian"
        )
        
        # Создаем QR код
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Преобразуем в base64 для отображения в браузере
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def generate_backup_codes(self) -> list:
        """Генерация резервных кодов"""
        codes = []
        for _ in range(8):
            # Генерируем 8-значный код
            code = ''.join(secrets.choice('0123456789') for _ in range(8))
            codes.append(code)
        return codes
    
    def verify_totp(self, secret_key: str, token: str) -> bool:
        """Проверка TOTP токена"""
        totp = pyotp.TOTP(secret_key)
        return totp.verify(token, valid_window=1)  # Допускаем 1 окно рассинхронизации
    
    def enable_2fa(self, user_id: int, user_email: str) -> Tuple[str, str, list]:
        """Включение 2FA для пользователя"""
        secret_key = self.generate_secret_key()
        qr_code = self.get_qr_code(user_email, secret_key)
        backup_codes = self.generate_backup_codes()
        
        # Сохраняем данные
        self.secret_keys[user_id] = secret_key
        self.backup_codes[user_id] = backup_codes
        
        return secret_key, qr_code, backup_codes
    
    def disable_2fa(self, user_id: int):
        """Отключение 2FA"""
        self.secret_keys.pop(user_id, None)
        self.backup_codes.pop(user_id, None)
    
    def is_2fa_enabled(self, user_id: int) -> bool:
        """Проверка включен ли 2FA"""
        return user_id in self.secret_keys

class BruteForceProtection:
    """🛡️ Защита от Brute Force атак"""
    
    def __init__(self):
        self.failed_attempts = defaultdict(list)  # {ip: [attempt_times]}
        self.blocked_ips = {}  # {ip: {blocked_until, reason}}
        self.max_attempts = 5  # Максимум попыток
        self.block_duration = 1800  # 30 минут блокировки
        self.attempt_window = 900  # 15 минут окно
    
    def record_failed_attempt(self, ip: str):
        """Запись неудачной попытки входа"""
        current_time = time.time()
        
        # Получаем список попыток для IP
        attempts = self.failed_attempts[ip]
        
        # Удаляем старые попытки
        while attempts and current_time - attempts[0] > self.attempt_window:
            attempts.pop(0)
        
        # Добавляем текущую попытки
        attempts.append(current_time)
        
        # Проверяем, нужно ли блокировать
        if len(attempts) >= self.max_attempts:
            self.block_ip(ip, "Множественные неудачные попытки входа")
    
    def block_ip(self, ip: str, reason: str):
        """Блокировка IP за Brute Force"""
        current_time = time.time()
        self.blocked_ips[ip] = {
            'blocked_until': current_time + self.block_duration,
            'reason': reason
        }
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Проверка блокировки IP"""
        if ip not in self.blocked_ips:
            return False
        
        blocked_info = self.blocked_ips[ip]
        if time.time() < blocked_info['blocked_until']:
            return True
        else:
            # Убираем истекшую блокировку
            del self.blocked_ips[ip]
            # Очищаем попытки
            self.failed_attempts[ip] = []
            return False
    
    def record_successful_attempt(self, ip: str):
        """Запись успешной попытки (сбрасывает счетчик)"""
        self.failed_attempts[ip] = []
    
    def get_attempts_info(self, ip: str) -> Dict:
        """Получение информации о попытках для IP"""
        current_time = time.time()
        attempts = self.failed_attempts[ip]
        
        # Считаем активные попытки
        active_attempts = len([t for t in attempts if current_time - t <= self.attempt_window])
        
        return {
            'failed_attempts': active_attempts,
            'max_attempts': self.max_attempts,
            'remaining_attempts': max(0, self.max_attempts - active_attempts),
            'is_blocked': self.is_ip_blocked(ip),
            'block_duration': self.block_duration,
            'attempt_window': self.attempt_window
        }

class SessionSecurity:
    """🔒 Безопасность сессий"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 час
        self.secure_session_key = secrets.token_hex(32)
        self.session_fingerprints = {}  # {session_id: fingerprint}
    
    def generate_session_fingerprint(self, request) -> str:
        """Генерация отпечатка сессии для обнаружения угонов"""
        # Создаем отпечаток на основе данных клиента
        user_agent = request.headers.get('User-Agent', '')
        accept_language = request.headers.get('Accept-Language', '')
        accept_encoding = request.headers.get('Accept-Encoding', '')
        
        fingerprint_data = f"{user_agent}{accept_language}{accept_encoding}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    def validate_session(self, session_id: str, request) -> bool:
        """Валидация сессии по отпечатку"""
        if session_id not in self.session_fingerprints:
            return False
        
        current_fingerprint = self.generate_session_fingerprint(request)
        stored_fingerprint = self.session_fingerprints[session_id]
        
        return current_fingerprint == stored_fingerprint
    
    def store_session_fingerprint(self, session_id: str, request):
        """Сохранение отпечатка сессии"""
        fingerprint = self.generate_session_fingerprint(request)
        self.session_fingerprints[session_id] = fingerprint
    
    def invalidate_session(self, session_id: str):
        """Аннулирование сессии"""
        self.session_fingerprints.pop(session_id, None)

# Создаем глобальные экземпляры
rate_limiter = RateLimiter()
two_factor_auth = TwoFactorAuth()
brute_force_protection = BruteForceProtection()
session_security = SessionSecurity()

def rate_limit(limit_type: str = 'general'):
    """Декоратор для ограничения скорости"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            
            if rate_limiter.is_rate_limited(ip, limit_type):
                limit_info = rate_limiter.get_rate_limit_info(ip, limit_type)
                abort(429, description=f'Превышен лимит запросов. Попробуйте через {int(limit_info["time_to_reset"])} секунд')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def brute_force_protect(f):
    """Декоратор для защиты от Brute Force"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if brute_force_protection.is_ip_blocked(ip):
            attempts_info = brute_force_protection.get_attempts_info(ip)
            abort(429, description=f'IP заблокирован до сброса попыток. Попробуйте через {int(attempts_info["block_duration"]/60)} минут')
        
        return f(*args, **kwargs)
    return decorated_function

def session_security_check(f):
    """Декоратор для проверки безопасности сессии"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = session.get('session_id')
        if session_id:
            if not session_security.validate_session(session_id, request):
                # Возможно, сессия угнана
                session.clear()
                abort(403, description='Подозрительная активность сессии')
        
        return f(*args, **kwargs)
    return decorated_function

def require_2fa(user_id: int):
    """Требование 2FA для критических операций"""
    if two_factor_auth.is_2fa_enabled(user_id):
        # Проверяем, подтвержден ли 2FA для этой сессии
        if not session.get('2fa_verified', False):
            abort(403, description='Требуется подтверждение двухфакторной аутентификации')

def setup_enhanced_auth_routes():
    """Настройка улучшенных маршрутов аутентификации"""
    from flask import Blueprint
    
    auth_security_bp = Blueprint('auth_security', __name__)
    
    @auth_security_bp.route('/2fa/setup', methods=['GET', 'POST'])
    @rate_limit('general')
    def setup_2fa():
        """Настройка двухфакторной аутентификации"""
        if 'user_id' not in session:
            abort(401)
        
        user_id = session['user_id']
        user_email = session.get('user_email', '')
        
        if request.method == 'POST':
            # Включаем 2FA
            secret_key, qr_code, backup_codes = two_factor_auth.enable_2fa(user_id, user_email)
            
            return jsonify({
                'success': True,
                'secret_key': secret_key,
                'qr_code': qr_code,
                'backup_codes': backup_codes
            })
        
        return jsonify({'enabled': two_factor_auth.is_2fa_enabled(user_id)})
    
    @auth_security_bp.route('/2fa/verify', methods=['POST'])
    @rate_limit('login')
    @brute_force_protect
    def verify_2fa():
        """Подтверждение 2FA кода"""
        if 'user_id' not in session:
            abort(401)
        
        user_id = session['user_id']
        token = request.json.get('token', '')
        
        if not two_factor_auth.is_2fa_enabled(user_id):
            return jsonify({'error': '2FA не включен'}), 400
        
        secret_key = two_factor_auth.secret_keys[user_id]
        
        if two_factor_auth.verify_totp(secret_key, token):
            session['2fa_verified'] = True
            brute_force_protection.record_successful_attempt(
                request.headers.get('X-Forwarded-For', request.remote_addr)
            )
            return jsonify({'success': True})
        
        return jsonify({'error': 'Неверный код'}), 400
    
    @auth_security_bp.route('/security/stats')
    @rate_limit('general')
    def get_security_stats():
        """Получение статистики безопасности"""
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        return jsonify({
            'rate_limit': rate_limiter.get_rate_limit_info(ip),
            'brute_force': brute_force_protection.get_attempts_info(ip)
        })
    
    return auth_security_bp

def initialize_auth_security():
    """Инициализация системы безопасной аутентификации"""
    return setup_enhanced_auth_routes()
