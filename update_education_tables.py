# update_education_tables.py
from app import create_app
from database import db

app = create_app()

with app.app_context():
    print("🔄 Обновляем таблицы обучения...")
    
    try:
        # Создаем таблицы
        from education.models import Course, Module, Lesson, UserProgress, CourseCertificate, UserAchievement
        db.create_all()
        print("✅ Таблицы созданы/обновлены")
        
        # Инициализируем данные курсов
        from education.progress_service import ProgressService
        if ProgressService.initialize_course_data():
            print("✅ Данные курсов инициализированы")
        else:
            print("⚠️ Не удалось инициализировать данные курсов")
        
        print("🎯 Система прогресса готова к работе!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")