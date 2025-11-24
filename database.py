# database.py
from flask_sqlalchemy import SQLAlchemy

# Оптимизированная конфигурация БД для производительности
db = SQLAlchemy(engine_options={
    'pool_pre_ping': True,  # Проверяем соединения перед использованием
    'pool_recycle': 300,   # Пересоздаем соединения каждые 5 минут
    'pool_size': 10,       # Размер пула соединений
    'max_overflow': 20     # Максимальное количество дополнительных соединений
})
