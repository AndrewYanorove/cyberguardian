# migrate_donations_simple.py
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db
from auth.models import Donation

def migrate_donations():
    """Добавляем таблицу donations"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Проверяем таблицу donations...")
        
        try:
            # Проверяем, существует ли таблица
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            existing_tables = inspector.get_table_names()
            
            if 'donations' not in existing_tables:
                print("📝 Создаем таблицу 'donations'...")
                Donation.__table__.create(db.engine)
                print("✅ Таблица 'donations' создана!")
            else:
                print("ℹ️ Таблица 'donations' уже существует")
                
                # Показываем структуру
                columns = inspector.get_columns('donations')
                print("\nСтруктура таблицы:")
                for col in columns:
                    print(f"  - {col['name']} ({col['type']})")
            
            # Проверяем внешние ключи
            foreign_keys = inspector.get_foreign_keys('donations')
            if foreign_keys:
                print("\n🔗 Внешние ключи:")
                for fk in foreign_keys:
                    print(f"  {fk['referred_table']}.{fk['referred_columns'][0]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    migrate_donations()