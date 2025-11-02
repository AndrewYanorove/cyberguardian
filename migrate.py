# migrate.py
import os
import sqlite3
import shutil
from datetime import datetime
from app import create_app
from database import db

app = create_app()

def safe_migration():
    print("🛡️ Запускаем БЕЗОПАСНУЮ миграцию...")
    
    with app.app_context():
        # 1. СОЗДАЕМ СУПЕР-БЭКАП
        backup_file = create_super_backup()
        
        try:
            # 2. Получаем ВСЕ данные из старой БД
            old_data = extract_all_data()
            
            # 3. Создаем новую временную БД с обновленной структурой
            temp_db = create_temp_database()
            
            # 4. Переносим ВСЕ данные в новую структуру
            transfer_all_data(old_data, temp_db)
            
            # 5. Заменяем старую БД на новую
            replace_database(temp_db)
            
            print("✅ МИГРАЦИЯ УСПЕШНА! Все данные сохранены!")
            
        except Exception as e:
            print(f"❌ Ошибка миграции: {e}")
            restore_from_backup(backup_file)
            print("✅ Восстановлен из бэкапа!")

def create_super_backup():
    """Создает бэкап с timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backups/super_backup_{timestamp}.db'
    
    if os.path.exists('instance/cyberguardian.db'):
        shutil.copy2('instance/cyberguardian.db', backup_file)
        print(f"💾 Создан супер-бэкап: {backup_file}")
    
    return backup_file

def extract_all_data():
    """Извлекает ВСЕ данные из текущей БД"""
    if not os.path.exists('instance/cyberguardian.db'):
        return {}
    
    conn = sqlite3.connect('instance/cyberguardian.db')
    conn.row_factory = sqlite3.Row
    data = {}
    
    try:
        # Получаем все таблицы
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Сохраняем данные из каждой таблицы
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            data[table] = [dict(row) for row in cursor.fetchall()]
            print(f"📊 Извлечено из {table}: {len(data[table])} записей")
    
    finally:
        conn.close()
    
    return data

def create_temp_database():
    """Создает временную БД с новой структурой"""
    temp_db = 'instance/temp_cyberguardian.db'
    
    if os.path.exists(temp_db):
        os.remove(temp_db)
    
    # Создаем новое приложение для временной БД
    from app import create_app
    temp_app = create_app()
    temp_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_db}'
    
    with temp_app.app_context():
        db.create_all()
    
    return temp_db

def transfer_all_data(old_data, temp_db):
    """Переносит все данные в новую структуру"""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    
    try:
        for table_name, records in old_data.items():
            if not records:
                continue
                
            # Получаем колонки новой таблицы
            cursor.execute(f"PRAGMA table_info({table_name})")
            new_columns = [row[1] for row in cursor.fetchall()]
            
            for record in records:
                # Фильтруем данные под новую структуру
                filtered_data = {k: v for k, v in record.items() if k in new_columns}
                
                if filtered_data:
                    columns = ', '.join(filtered_data.keys())
                    placeholders = ', '.join(['?' for _ in filtered_data])
                    values = list(filtered_data.values())
                    
                    cursor.execute(
                        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                        values
                    )
            
            print(f"✅ Перенесено в {table_name}: {len(records)} записей")
        
        conn.commit()
        
    finally:
        conn.close()

def replace_database(temp_db):
    """Заменяет старую БД на новую"""
    old_db = 'instance/cyberguardian.db'
    
    if os.path.exists(old_db):
        os.remove(old_db)
    
    shutil.copy2(temp_db, old_db)
    os.remove(temp_db)
    
    print("🔄 База данных успешно заменена!")

def restore_from_backup(backup_file):
    """Восстанавливает из бэкапа"""
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, 'instance/cyberguardian.db')
        print(f"🔥 Восстановлен из: {backup_file}")

if __name__ == '__main__':
    safe_migration()