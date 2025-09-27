# create_tables.py
from app import create_app

app = create_app()

with app.app_context():
    from auth.models import db
    db.create_all()
    print("✅ Таблицы базы данных созданы успешно!")