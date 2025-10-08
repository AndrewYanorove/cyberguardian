from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
import random
from datetime import datetime, timedelta

threat_bp = Blueprint('threats', __name__)

# База данных угроз
CYBER_THREATS = [
    {
        'id': 1,
        'name': 'Фишинговая атака',
        'type': 'phishing',
        'severity': 'high',
        'description': 'Массовая рассылка поддельных писем от имени банков',
        'target': 'Пользователи банковских услуг',
        'status': 'active',
        'detected': datetime.now() - timedelta(hours=2),
        'affected_users': 1500,
        'protection': 'Не переходите по ссылкам в подозрительных письмах'
    },
    {
        'id': 2,
        'name': 'DDoS атака',
        'type': 'ddos',
        'severity': 'medium',
        'description': 'Распределенная атака на серверы образовательных учреждений',
        'target': 'Образовательные платформы',
        'status': 'monitoring',
        'detected': datetime.now() - timedelta(hours=5),
        'affected_users': 3200,
        'protection': 'Используйте DDoS защиту и мониторинг трафика'
    },
    {
        'id': 3,
        'name': 'Ransomware',
        'type': 'malware',
        'severity': 'critical',
        'description': 'Шифровальщик атакует корпоративные сети',
        'target': 'Корпоративные пользователи',
        'status': 'contained',
        'detected': datetime.now() - timedelta(days=1),
        'affected_users': 89,
        'protection': 'Регулярно делайте резервные копии данных'
    },
    {
        'id': 4,
        'name': 'Утечка данных',
        'type': 'data_breach',
        'severity': 'high',
        'description': 'Обнаружена утечка персональных данных пользователей',
        'target': 'Социальные сети',
        'status': 'investigating',
        'detected': datetime.now() - timedelta(hours=12),
        'affected_users': 50000,
        'protection': 'Используйте двухфакторную аутентификацию'
    }
]

THREAT_STATS = {
    'total_threats': 156,
    'threats_today': 8,
    'blocked_attacks': 142,
    'success_rate': 91.2,
    'avg_response_time': '2.3 мин'
}

@threat_bp.route('/')
@login_required
def threat_dashboard():
    """Дашборд мониторинга угроз"""
    return render_template('threat_monitor/dashboard.html')

@threat_bp.route('/live')
@login_required
def live_threats():
    """Мониторинг угроз в реальном времени"""
    return render_template('threat_monitor/live.html')

@threat_bp.route('/analysis')
@login_required
def threat_analysis():
    """Анализ угроз и статистика"""
    return render_template('threat_monitor/analysis.html')

@threat_bp.route('/protection')
@login_required
def protection_guide():
    """Руководство по защите"""
    return render_template('threat_monitor/protection.html')

# API endpoints
@threat_bp.route('/api/active-threats')
def get_active_threats():
    """Получить активные угрозы"""
    active_threats = [t for t in CYBER_THREATS if t['status'] in ['active', 'monitoring']]
    return jsonify({'threats': active_threats})

@threat_bp.route('/api/threat-stats')
def get_threat_stats():
    """Получить статистику угроз"""
    return jsonify(THREAT_STATS)

@threat_bp.route('/api/live-feed')
def get_live_feed():
    """Генерация живого фида угроз"""
    threat_types = ['phishing', 'malware', 'ddos', 'data_breach', 'brute_force']
    severities = ['low', 'medium', 'high', 'critical']
    
    live_events = []
    for i in range(10):
        event = {
            'id': i + 1,
            'timestamp': datetime.now() - timedelta(minutes=random.randint(1, 60)),
            'type': random.choice(threat_types),
            'severity': random.choice(severities),
            'description': f'Обнаружена {random.choice(["попытка", "активность", "атака"])} {random.choice(["в сети", "на сервере", "в приложении"])}',
            'source_ip': f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
            'target': random.choice(['Сервер', 'Пользователь', 'Сеть', 'База данных']),
            'action': random.choice(['Блокировано', 'Мониторинг', 'Исследование'])
        }
        live_events.append(event)
    
    # Сортируем по времени
    live_events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({'events': live_events})

@threat_bp.route('/api/threat-map')
def get_threat_map():
    """Генерация данных для карты угроз"""
    countries = ['Россия', 'США', 'Германия', 'Китай', 'Бразилия', 'Индия', 'Япония', 'Великобритания']
    
    threat_map = []
    for country in countries:
        threat_map.append({
            'country': country,
            'threats': random.randint(5, 50),
            'attacks_blocked': random.randint(50, 200),
            'severity': random.choice(['low', 'medium', 'high'])
        })
    
    return jsonify({'threat_map': threat_map})

@threat_bp.route('/api/report-threat', methods=['POST'])
@login_required
def report_threat():
    """Сообщить об угрозе"""
    data = request.get_json()
    
    new_threat = {
        'id': len(CYBER_THREATS) + 1,
        'name': data.get('name', 'Новая угроза'),
        'type': data.get('type', 'unknown'),
        'severity': data.get('severity', 'medium'),
        'description': data.get('description', ''),
        'reported_by': current_user.username,
        'status': 'reported',
        'detected': datetime.now()
    }
    
    CYBER_THREATS.append(new_threat)
    
    return jsonify({
        'success': True,
        'message': 'Угроза успешно зарегистрирована',
        'threat_id': new_threat['id']
    })
