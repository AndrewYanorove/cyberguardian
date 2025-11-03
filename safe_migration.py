# safe_migration.py
import os
import sqlite3
import shutil
from datetime import datetime

def safe_database_migration():
    """Безопасная миграция базы данных при деплое"""
    print("🛡️ Запускаем БЕЗОПАСНУЮ миграцию базы данных...")
    
    old_db_path = 'instance/cyberguardian.db'
    backup_path = 'backups/deploy_backup.db'
    
    # Создаем папки если их нет
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # 1. Если старая БД существует - создаем резервную копию
    if os.path.exists(old_db_path):
        shutil.copy2(old_db_path, backup_path)
        print(f"💾 Создана резервная копия: {backup_path}")
        
        # Проверяем целостность старой БД
        if check_database_integrity(old_db_path):
            print("✅ Старая база данных цела, можно использовать")
            return True
        else:
            print("⚠️ Старая БД повреждена, будет создана новая")
            return False
    else:
        print("🆕 База данных не существует, будет создана новая")
        return False

def check_database_integrity(db_path):
    """Проверяет целостность базы данных"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем целостность
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        # Проверяем основные таблицы
        required_tables = ['user', 'user_progress', 'encryption_history']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Проверяем что все нужные таблицы существуют
        for table in required_tables:
            if table not in existing_tables:
                print(f"❌ Отсутствует таблица: {table}")
                return False
        
        conn.close()
        return result[0] == 'ok'
        
    except Exception as e:
        print(f"❌ Ошибка проверки целостности: {e}")
        return False

def restore_from_backup():
    """Восстанавливает данные из бэкапа"""
    backup_path = 'backups/deploy_backup.db'
    old_db_path = 'instance/cyberguardian.db'
    
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, old_db_path)
        print(f"🔥 Восстановлено из бэкапа: {backup_path}")
        return True
    return False

if __name__ == '__main__':
    safe_database_migration()