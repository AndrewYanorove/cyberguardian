from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import random
import time
import threading
from datetime import datetime

ddos_bp = Blueprint('ddos', __name__)

# Хранилище для симуляции атак
active_attacks = {}
attack_history = []

class DDoSSimulator:
    @staticmethod
    def simulate_attack(target, attack_type, duration, intensity):
        """Симуляция DDoS атаки (учебные цели)"""
        attack_id = f"attack_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Параметры атаки
        attack_config = {
            'id': attack_id,
            'target': target,
            'type': attack_type,
            'duration': duration,
            'intensity': intensity,
            'start_time': datetime.now(),
            'status': 'running',
            'packets_sent': 0,
            'success_rate': 0
        }
        
        active_attacks[attack_id] = attack_config
        attack_history.append(attack_config.copy())
        
        # Запускаем симуляцию в отдельном потоке
        thread = threading.Thread(
            target=DDoSSimulator._run_attack_simulation,
            args=(attack_id, target, attack_type, duration, intensity)
        )
        thread.daemon = True
        thread.start()
        
        return attack_id
    
    @staticmethod
    def _run_attack_simulation(attack_id, target, attack_type, duration, intensity):
        """Запуск симуляции атаки"""
        start_time = time.time()
        end_time = start_time + duration
        
        packets_per_second = intensity * 100  # Упрощенная модель
        
        while time.time() < end_time and active_attacks.get(attack_id, {}).get('status') == 'running':
            # Симуляция отправки пакетов
            packets_sent = int((time.time() - start_time) * packets_per_second)
            success_rate = max(10, min(95, 100 - intensity * 5))  # Чем выше интенсивность, тем ниже успех
            
            # Обновляем статистику
            if attack_id in active_attacks:
                active_attacks[attack_id]['packets_sent'] = packets_sent
                active_attacks[attack_id]['success_rate'] = success_rate
                active_attacks[attack_id]['elapsed_time'] = time.time() - start_time
            
            time.sleep(0.5)  # Обновляем статистику каждые 0.5 секунд
        
        # Завершаем атаку
        if attack_id in active_attacks:
            active_attacks[attack_id]['status'] = 'completed'
            active_attacks[attack_id]['end_time'] = datetime.now()
    
    @staticmethod
    def stop_attack(attack_id):
        """Остановка атаки"""
        if attack_id in active_attacks:
            active_attacks[attack_id]['status'] = 'stopped'
            return True
        return False
    
    @staticmethod
    def get_attack_types():
        """Типы DDoS атак для обучения"""
        return [
            {
                'id': 'syn_flood',
                'name': 'SYN Flood',
                'description': 'Переполнение TCP соединений SYN-пакетами',
                'difficulty': 'medium',
                'impact': 'high',
                'defense': 'Настройка SYN cookies, фильтрация пакетов'
            },
            {
                'id': 'udp_flood', 
                'name': 'UDP Flood',
                'description': 'Массовая отправка UDP пакетов',
                'difficulty': 'easy',
                'impact': 'medium',
                'defense': 'Ограничение UDP трафика, фильтрация'
            },
            {
                'id': 'http_flood',
                'name': 'HTTP Flood',
                'description': 'Множество HTTP запросов к веб-серверу',
                'difficulty': 'hard',
                'impact': 'high',
                'defense': 'WAF, ограничение запросов, CAPTCHA'
            },
            {
                'id': 'icmp_flood',
                'name': 'ICMP Flood',
                'description': 'Переполнение ping-пакетами',
                'difficulty': 'easy',
                'impact': 'low',
                'defense': 'Отключение ICMP, фильтрация'
            }
        ]
    
    @staticmethod
    def get_protection_methods():
        """Методы защиты от DDoS атак"""
        return [
            'Использование CDN (Cloudflare, Akamai)',
            'Настройка брандмауэра и IPS',
            'Ограничение скорости запросов',
            'Гео-фильтрация трафика',
            'Использование WAF (Web Application Firewall)',
            'Резервирование каналов связи',
            'Мониторинг трафика в реальном времени',
            'План реагирования на инциденты'
        ]

@ddos_bp.route('/')
@login_required
def ddos_simulator():
    """Главная страница DDoS симулятора"""
    return render_template('ddos_simulator/dashboard.html')

@ddos_bp.route('/attack')
@login_required
def attack_interface():
    """Интерфейс для симуляции атак"""
    return render_template('ddos_simulator/attack.html')

@ddos_bp.route('/education')
@login_required
def ddos_education():
    """Образовательные материалы по DDoS"""
    return render_template('ddos_simulator/education.html')

@ddos_bp.route('/protection')
@login_required
def protection_guide():
    """Руководство по защите"""
    return render_template('ddos_simulator/protection.html')

# API endpoints
@ddos_bp.route('/api/attack-types')
def get_attack_types():
    """Получить типы DDoS атак"""
    return jsonify({'attack_types': DDoSSimulator.get_attack_types()})

@ddos_bp.route('/api/start-attack', methods=['POST'])
@login_required
def start_attack():
    """Начать симуляцию атаки"""
    data = request.get_json()
    
    target = data.get('target', 'example.com')
    attack_type = data.get('attack_type', 'syn_flood')
    duration = data.get('duration', 30)  # в секундах
    intensity = data.get('intensity', 5)  # 1-10
    
    # Валидация для учебных целей
    allowed_targets = ['example.com', 'test-server.org', 'demo-site.net']
    if target not in allowed_targets:
        return jsonify({'error': 'Разрешены только учебные цели: example.com, test-server.org, demo-site.net'}), 400
    
    attack_id = DDoSSimulator.simulate_attack(target, attack_type, duration, intensity)
    
    return jsonify({
        'success': True,
        'attack_id': attack_id,
        'message': 'Симуляция атаки запущена (учебные цели)'
    })

@ddos_bp.route('/api/stop-attack', methods=['POST'])
@login_required
def stop_attack():
    """Остановить атаку"""
    data = request.get_json()
    attack_id = data.get('attack_id')
    
    if DDoSSimulator.stop_attack(attack_id):
        return jsonify({'success': True, 'message': 'Атака остановлена'})
    else:
        return jsonify({'error': 'Атака не найдена'}), 404

@ddos_bp.route('/api/attack-status')
def get_attack_status():
    """Получить статус активных атак"""
    return jsonify({'active_attacks': active_attacks})

@ddos_bp.route('/api/attack-history')
@login_required
def get_attack_history():
    """Получить историю атак"""
    return jsonify({'attack_history': attack_history[-10:]})  # Последние 10 атак

@ddos_bp.route('/api/protection-methods')
def get_protection_methods():
    """Получить методы защиты"""
    return jsonify({'protection_methods': DDoSSimulator.get_protection_methods()})

@ddos_bp.route('/api/attack-stats')
def get_attack_stats():
    """Статистика по атакам"""
    total_attacks = len(attack_history)
    successful_attacks = len([a for a in attack_history if a.get('success_rate', 0) > 50])
    avg_duration = sum([a.get('duration', 0) for a in attack_history]) / max(1, total_attacks)
    
    return jsonify({
        'total_attacks': total_attacks,
        'successful_attacks': successful_attacks,
        'success_rate': round((successful_attacks / total_attacks * 100) if total_attacks > 0 else 0, 1),
        'average_duration': round(avg_duration, 1),
        'active_now': len(active_attacks)
    })
