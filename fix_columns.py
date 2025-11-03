# [file name]: fix_columns.py
import sqlite3
import os

def fix_database():
    db_path = 'instance/cyberguardian.db'
    
    if not os.path.exists(db_path):
        print("❌ Файл БД не найден!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Добавляем is_approved в story_comments если его нет
        cursor.execute("PRAGMA table_info(story_comments)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_approved' not in columns:
            cursor.execute("ALTER TABLE story_comments ADD COLUMN is_approved BOOLEAN DEFAULT TRUE")
            print("✅ Добавлен столбец is_approved в story_comments")
        
        conn.commit()
        print("🎉 База данных исправлена!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_database()