# reset_education_complete.py
from app import create_app
from database import db
from sqlalchemy import text
import os

app = create_app()

with app.app_context():
    print("🔄 ПОЛНЫЙ СБРОС СИСТЕМЫ ОБУЧЕНИЯ...")
    
    try:
        # 1. Удаляем ВСЕ таблицы обучения
        tables = ['user_achievements', 'course_certificates', 'user_progress', 
                 'lessons', 'modules', 'courses']
        
        for table in tables:
            try:
                db.session.execute(text(f'DROP TABLE IF EXISTS {table}'))
                print(f"✅ Удалена таблица: {table}")
            except Exception as e:
                print(f"⚠️ Не удалось удалить {table}: {e}")
        
        db.session.commit()
        print("✅ Все старые таблицы удалены")
        
        # 2. Создаем чистые таблицы БЕЗ relationships
        db.create_all()
        print("✅ Новые таблицы созданы")
        
        # 3. Инициализируем данные курсов
        from education.progress_service import ProgressService
        if ProgressService.initialize_course_data():
            print("✅ Данные курсов успешно инициализированы!")
        else:
            print("❌ Ошибка инициализации данных курсов")
        
        # 4. Проверяем что все создалось
        from education.models import Course, Module, Lesson
        course_count = Course.query.count()
        module_count = Module.query.count() 
        lesson_count = Lesson.query.count()
        
        print(f"📊 Статистика:")
        print(f"   Курсы: {course_count}")
        print(f"   Модули: {module_count}")
        print(f"   Уроки: {lesson_count}")
        
        print("🎯 СИСТЕМА ОБУЧЕНИЯ ГОТОВА К РАБОТЕ!")
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        db.session.rollback()