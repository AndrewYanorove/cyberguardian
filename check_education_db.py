from app import create_app
from database import db

app = create_app()

with app.app_context():
    # Проверяем существование таблиц
    from education.models import Course, Module, Lesson, UserProgress
    
    print("🔍 Проверка таблиц обучения:")
    print(f"📚 Courses: {Course.query.count()}")
    print(f"📖 Modules: {Module.query.count()}")
    print(f"📝 Lessons: {Lesson.query.count()}")
    print(f"📊 UserProgress: {UserProgress.query.count()}")
    
    # Показываем несколько курсов
    courses = Course.query.all()
    for course in courses[:3]:  # первые 3 курса
        print(f"  - {course.id}: {course.title}")