# check_db.py
import os
import sqlite3
from datetime import datetime
import shutil

def check_database_integrity():
    """Проверяет целостность базы данных"""
    db_path = 'instance/cyberguardian.db'
    
    if not os.path.exists(db_path):
        print("❌ Файл базы данных не найден!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем целостность
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        if result[0] == 'ok':
            print("✅ База данных цела")
            
            # Проверяем ВСЕ таблицы
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            total_records = 0
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                print(f"📊 {table}: {count} записей")
            
            print(f"🎯 Всего записей в БД: {total_records}")
            
            return True
        else:
            print(f"❌ Ошибка целостности БД: {result[0]}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки БД: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def backup_database():
    """Создает резервную копию БД при каждом запуске"""
    source = 'instance/cyberguardian.db'
    if os.path.exists(source):
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/backup_{timestamp}.db'
        
        try:
            shutil.copy2(source, backup_file)
            print(f"✅ Резервная копия создана: {backup_file}")
            
            # Удаляем старые бэкапы (оставляем последние 10)
            backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('backup_')])
            for old_backup in backups[:-10]:
                os.remove(os.path.join(backup_dir, old_backup))
                print(f"🗑️ Удален старый бэкап: {old_backup}")
                
        except Exception as e:
            print(f"❌ Ошибка создания бэкапа: {e}")
    else:
        print("ℹ️ Файл БД не существует, бэкап не требуется")

if __name__ == '__main__':
    check_database_integrity()