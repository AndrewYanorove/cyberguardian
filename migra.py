# fix_all_columns.py
import sqlite3

def add_all_missing_columns():
    conn = sqlite3.connect('instance/cyberguardian.db')
    cursor = conn.cursor()
    
    # Все столбцы, которые должны быть в таблице users
    # (из ошибок видно какие нужны)
    columns_to_add = [
        ('user_is_active', 'BOOLEAN DEFAULT 1'),
        ('banned_reason', 'TEXT'),
        ('banned_at', 'DATETIME'),
        ('banned_by', 'INTEGER'),
        ('last_login', 'DATETIME'),
    ]
    
    # Получаем существующие столбцы
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    print("🔍 Проверка столбцов таблицы users...")
    print(f"Существующие: {existing_columns}")
    
    # Добавляем недостающие столбцы
    for column_name, column_type in columns_to_add:
        if column_name not in existing_columns:
            try:
                sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
                cursor.execute(sql)
                print(f"✅ Добавлен столбец: {column_name}")
            except Exception as e:
                print(f"❌ Ошибка добавления {column_name}: {e}")
    
    conn.commit()
    
    # Проверяем результат
    cursor.execute("PRAGMA table_info(users)")
    final_columns = [col[1] for col in cursor.fetchall()]
    print(f"\n🎯 Итоговые столбцы ({len(final_columns)}):")
    for col in final_columns:
        print(f"  - {col}")
    
    conn.close()
    print("\n✅ Все столбцы добавлены!")

if __name__ == "__main__":
    add_all_missing_columns()