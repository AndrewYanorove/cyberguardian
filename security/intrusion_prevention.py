"""
🔒 СИСТЕМА ОБНАРУЖЕНИЯ И ПРЕДОТВРАЩЕНИЯ ВТОРЖЕНИЙ (IPS)
CyberGuardian - Максимальная защита от кибератак
"""

import re
import time
import hashlib
import json
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from flask import request, g, abort, jsonify
from collections import defaultdict, deque
import threading

class SecurityThreatDetector:
    """🛡️ Основной класс для обнаружения угроз"""
    
    def __init__(self):
        self.threat_patterns = {
            'sql_injection': [
                r"(\bunion\b.*\bselect\b)",
                r"(\bor\b\s+\d+\s*=\s*\d+)",
                r"(\bdrop\b.*\btable\b)",
                r"(\bdelete\b.*\bfrom\b)",
                r"(\binsert\b.*\binto\b)",
                r"(\bupdate\b.*\bset\b)",
                r"(\bexec\b|\bexecute\b)",
                r"(';\s*--)|(;\s*--)",
                r"(\bor\b\s*'.*'='.*')",
                r"(\bxp_cmdshell\b)",
                r"(\binformation_schema\b)",
                r"(\bsys\.tables\b)",
                r"(\bload_file\b\()",
                r"(\binto\s+outfile\b)"
            ],
            'xss_attempts': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"vbscript:",
                r"onload\s*=",
                r"onerror\s*=",
                r"onclick\s*=",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>",
                r"<form[^>]*action\s*=\s*['\"].*['\"]",
                r"document\.cookie",
                r"document\.location",
                r"eval\(",
                r"alert\(",
                r"confirm\(",
                r"prompt\("
            ],
            'path_traversal': [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e%5c",
                r"\.\.%2f",
                r"\.\.%5c",
                r"/etc/passwd",
                r"c:\\windows\\system32",
                r"boot\.ini",
                r"\\..\\",
                r"\.\.%252f"
            ],
            'command_injection': [
                r"\|\s*nc\s",
                r"\|\s*netcat\s",
                r"\|\s*bash\s",
                r"\|\s*sh\s",
                r"\|\s*powershell\s",
                r";\s*rm\s",
                r";\s*del\s",
                r"&\s*cmd",
                r"&\s*command",
                r"\|\|\s*whoami",
                r"\|\|\s*id",
                r"`[^`]*`",
                r"\$\([^)]*\)",
                r"\bcurl\s",
                r"\bwget\s",
                r"\bnslookup\s",
                r"\bdig\s"
            ],
            'malicious_files': [
                r"\.php$",
                r"\.asp$",
                r"\.aspx$",
                r"\.jsp$",
                r"\.exe$",
                r"\.bat$",
                r"\.cmd$",
                r"\.scr$",
                r"\.vbs$",
                r"\.js$",
                r"\.jar$",
                r"\.com$",
                r"\.pif$",
                r"\.scr$"
            ],
            'suspicious_user_agents': [
                r"sqlmap",
                r"nikto",
                r"nmap",
                r"masscan",
                r"zap",
                r"burp",
                r"scanner",
                r"bot",
                r"crawler",
                r"spider",
                r"wget",
                r"curl",
                r"python-requests",
                r"scrapy"
            ]
        }
        
        # Блокированные IP адреса
        self.blocked_ips = set()
        self.ip_activity = defaultdict(lambda: {'requests': deque(maxlen=100), 'threats': 0, 'last_activity': time.time()})
        self.rate_limits = defaultdict(lambda: {'count': 0, 'reset_time': time.time()})
        
        # Инициализация базы данных угроз
        self.init_threat_database()
    
    def init_threat_database(self):
        """Инициализация базы данных для хранения угроз"""
        try:
            threat_db_path = 'instance/threats.db'
            os.makedirs('instance', exist_ok=True)
            
            conn = sqlite3.connect(threat_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    threat_type TEXT,
                    threat_details TEXT,
                    request_path TEXT,
                    request_method TEXT,
                    severity TEXT,
                    blocked BOOLEAN DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocked_ips (
                    ip_address TEXT PRIMARY KEY,
                    blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    reason TEXT,
                    expires_at DATETIME,
                    is_permanent BOOLEAN DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            print("🛡️ База данных угроз инициализирована")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации БД угроз: {e}")
    
    def log_threat(self, ip: str, threat_type: str, details: str, request_data: dict, severity: str = 'HIGH', blocked: bool = True):
        """Логирование обнаруженных угроз"""
        try:
            threat_db_path = 'instance/threats.db'
            conn = sqlite3.connect(threat_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_logs 
                (ip_address, user_agent, threat_type, threat_details, request_path, request_method, severity, blocked)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ip,
                request_data.get('user_agent', ''),
                threat_type,
                details,
                request_data.get('path', ''),
                request_data.get('method', ''),
                severity,
                blocked
            ))
            
            conn.commit()
            conn.close()
            
            # Обновляем статистику активности IP
            self.ip_activity[ip]['threats'] += 1
            self.ip_activity[ip]['last_activity'] = time.time()
            
            print(f"🚨 УГРОЗА ОБНАРУЖЕНА: {threat_type} от IP {ip}")
            
        except Exception as e:
            print(f"❌ Ошибка логирования угрозы: {e}")
    
    def block_ip(self, ip: str, reason: str, duration_hours: int = 24, permanent: bool = False):
        """Блокировка IP адреса"""
        try:
            # Добавляем в память
            self.blocked_ips.add(ip)
            
            # Сохраняем в базу данных
            threat_db_path = 'instance/threats.db'
            conn = sqlite3.connect(threat_db_path)
            cursor = conn.cursor()
            
            expires_at = None if permanent else datetime.now() + timedelta(hours=duration_hours)
            
            cursor.execute('''
                INSERT OR REPLACE INTO blocked_ips 
                (ip_address, reason, expires_at, is_permanent)
                VALUES (?, ?, ?, ?)
            ''', (ip, reason, expires_at, permanent))
            
            conn.commit()
            conn.close()
            
            print(f"🚫 IP {ip} заблокирован на {duration_hours} часов. Причина: {reason}")
            
        except Exception as e:
            print(f"❌ Ошибка блокировки IP: {e}")
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Проверка, заблокирован ли IP"""
        # Проверяем в памяти
        if ip in self.blocked_ips:
            return True
        
        # Проверяем в базе данных
        try:
            threat_db_path = 'instance/threats.db'
            conn = sqlite3.connect(threat_db_path)
            cursor = conn.cursor()
            
            # Проверяем активные блокировки
            cursor.execute('''
                SELECT is_permanent, expires_at FROM blocked_ips 
                WHERE ip_address = ? AND (is_permanent = 1 OR expires_at > datetime('now'))
            ''', (ip,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                if result[0]:  # permanent
                    self.blocked_ips.add(ip)
                    return True
                else:
                    self.blocked_ips.add(ip)
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Ошибка проверки блокировки IP: {e}")
            return False
    
    def check_rate_limit(self, ip: str, limit: int = 100, window_seconds: int = 3600) -> bool:
        """Проверка лимита запросов"""
        current_time = time.time()
        rate_data = self.rate_limits[ip]
        
        # Сброс счетчика если окно прошло
        if current_time - rate_data['reset_time'] > window_seconds:
            rate_data['count'] = 0
            rate_data['reset_time'] = current_time
        
        rate_data['count'] += 1
        
        if rate_data['count'] > limit:
            self.block_ip(ip, f"Превышен лимит запросов: {rate_data['count']}/{limit}", duration_hours=1)
            return False
        
        return True
    
    def detect_threats(self, request_data: dict) -> Tuple[bool, List[str]]:
        """Обнаружение угроз в запросе"""
        threats = []
        ip = request_data.get('ip', '')
        
        # Проверяем блокировку IP
        if self.is_ip_blocked(ip):
            return True, ['IP заблокирован']
        
        # Проверяем rate limiting
        if not self.check_rate_limit(ip):
            return True, ['Превышен лимит запросов']
        
        # Проверяем паттерны угроз
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, str(request_data.get('data', '')), re.IGNORECASE | re.MULTILINE):
                        threats.append(threat_type)
                        
                        # Логируем угрозу
                        self.log_threat(ip, threat_type, f"Обнаружен паттерн: {pattern}", request_data)
                        
                        # Блокируем при критических угрозах
                        if threat_type in ['sql_injection', 'command_injection', 'path_traversal']:
                            self.block_ip(ip, f"Критическая угроза: {threat_type}", duration_hours=24)
                            return True, threats
                        
                except Exception as e:
                    print(f"❌ Ошибка проверки паттерна {pattern}: {e}")
        
        # Дополнительные проверки
        if self.is_suspicious_request(request_data):
            threats.append('suspicious_activity')
            self.log_threat(ip, 'suspicious_activity', 'Подозрительная активность', request_data)
        
        return len(threats) > 0, threats
    
    def is_suspicious_request(self, request_data: dict) -> bool:
        """Дополнительные проверки подозрительной активности"""
        suspicious_indicators = 0
        
        # Проверяем User-Agent
        user_agent = request_data.get('user_agent', '').lower()
        for pattern in self.threat_patterns['suspicious_user_agents']:
            if re.search(pattern, user_agent, re.IGNORECASE):
                suspicious_indicators += 1
        
        # Проверяем частоту запросов
        ip = request_data.get('ip', '')
        if ip in self.ip_activity:
            recent_requests = [t for t in self.ip_activity[ip]['requests'] 
                             if time.time() - t < 60]  # последние 60 секунд
            if len(recent_requests) > 50:  # более 50 запросов в минуту
                suspicious_indicators += 1
        
        # Проверяем размер запроса
        data_size = len(str(request_data.get('data', '')))
        if data_size > 100000:  # более 100KB
            suspicious_indicators += 1
        
        return suspicious_indicators >= 2
    
    def get_threat_statistics(self) -> dict:
        """Получение статистики угроз"""
        try:
            threat_db_path = 'instance/threats.db'
            conn = sqlite3.connect(threat_db_path)
            cursor = conn.cursor()
            
            # Общая статистика
            cursor.execute('SELECT COUNT(*) FROM security_logs WHERE timestamp > datetime("now", "-24 hours")')
            threats_last_24h = cursor.fetchone()[0]
            
            # Статистика по типам угроз
            cursor.execute('''
                SELECT threat_type, COUNT(*) 
                FROM security_logs 
                WHERE timestamp > datetime("now", "-24 hours")
                GROUP BY threat_type
            ''')
            threat_types = dict(cursor.fetchall())
            
            # Топ атакующих IP
            cursor.execute('''
                SELECT ip_address, COUNT(*) 
                FROM security_logs 
                WHERE timestamp > datetime("now", "-24 hours")
                GROUP BY ip_address 
                ORDER BY COUNT(*) DESC 
                LIMIT 10
            ''')
            top_attackers = dict(cursor.fetchall())
            
            # Заблокированные IP
            cursor.execute('SELECT COUNT(*) FROM blocked_ips WHERE is_permanent = 0 AND expires_at > datetime("now")')
            active_blocks = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'threats_last_24h': threats_last_24h,
                'threat_types': threat_types,
                'top_attackers': top_attackers,
                'active_blocks': active_blocks,
                'total_blocked_ips': len(self.blocked_ips)
            }
            
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            return {}

# Глобальный экземпляр детектора угроз
threat_detector = SecurityThreatDetector()

def security_middleware():
    """Middleware для проверки безопасности запросов"""
    try:
        # Собираем данные запроса
        request_data = {
            'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
            'user_agent': request.headers.get('User-Agent', ''),
            'path': request.path,
            'method': request.method,
            'data': str(request.get_data())
        }
        
        # Обнаруживаем угрозы
        is_threat, threats = threat_detector.detect_threats(request_data)
        
        if is_threat:
            # Логируем атаку
            threat_detector.log_threat(
                request_data['ip'],
                'multiple_threats',
                f'Обнаружены угрозы: {", ".join(threats)}',
                request_data,
                severity='CRITICAL'
            )
            
            # Возвращаем ошибку 403
            abort(403, description='Доступ заблокирован из-за подозрительной активности')
        
        # Добавляем информацию о безопасности в g
        g.security_checked = True
        g.request_ip = request_data['ip']
        
    except Exception as e:
        print(f"❌ Ошибка в security middleware: {e}")

def get_security_stats():
    """Получение статистики безопасности"""
    return threat_detector.get_threat_statistics()

def force_block_ip(ip: str, reason: str = "Ручная блокировка", hours: int = 24):
    """Принудительная блокировка IP"""
    threat_detector.block_ip(ip, reason, duration_hours=hours)
    return {"status": "blocked", "ip": ip, "reason": reason}

def unblock_ip(ip: str):
    """Разблокировка IP"""
    try:
        threat_db_path = 'instance/threats.db'
        conn = sqlite3.connect(threat_db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM blocked_ips WHERE ip_address = ?', (ip,))
        
        conn.commit()
        conn.close()
        
        # Удаляем из памяти
        threat_detector.blocked_ips.discard(ip)
        
        return {"status": "unblocked", "ip": ip}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
