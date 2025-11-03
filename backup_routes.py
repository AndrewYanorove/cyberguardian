# backup_routes.py
from flask import Blueprint, jsonify, request
import os
import shutil
from datetime import datetime
from database import db

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/api/create-backup', methods=['POST'])
def create_backup_api():
    """API для создания бэкапа (можно вызывать извне)"""
    try:
        if create_automatic_backup():
            return jsonify({
                'status': 'success', 
                'message': 'Backup created successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'status': 'error', 'message': 'Backup failed'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@backup_bp.route('/api/backup-status', methods=['GET'])
def backup_status():
    """Показывает статус бэкапов"""
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        return jsonify({'backups': [], 'total': 0})
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.endswith('.db'):
            file_path = os.path.join(backup_dir, file)
            stats = os.stat(file_path)
            backups.append({
                'name': file,
                'size': stats.st_size,
                'modified': datetime.fromtimestamp(stats.st_mtime).isoformat()
            })
    
    backups.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({
        'backups': backups[:5],  # Последние 5 бэкапов
        'total': len(backups),
        'persistent_exists': os.path.exists('backups/persistent_backup.db')
    })

def create_automatic_backup():
    """Создает автоматический бэкап"""
    try:
        source = 'instance/cyberguardian.db'
        if not os.path.exists(source):
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backups/auto_backup_{timestamp}.db'
        
        shutil.copy2(source, backup_file)
        
        # Сохраняем также как постоянный бэкап
        persistent_backup = 'backups/persistent_backup.db'
        shutil.copy2(source, persistent_backup)
        
        print(f"💾 Автоматический бэкап создан: {backup_file}")
        return True
        
    except Exception as e:
        print(f"⚠️ Ошибка создания бэкапа: {e}")
        return False