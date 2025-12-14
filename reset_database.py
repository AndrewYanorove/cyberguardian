# reset_database.py
import os
import shutil

# Удаляем старую базу данных
db_files = [
    'instance/cyberguardian.db',
    'backups/persistent_backup.db'
]

for db_file in db_files:
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"🗑️ Удален: {db_file}")

# Удаляем старые миграции
if os.path.exists('migrations'):
    shutil.rmtree('migrations')
    print("🗑️ Удалена папка migrations")

print("✅ База данных сброшена. Запустите app.py для создания новой.")