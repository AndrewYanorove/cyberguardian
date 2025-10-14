from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    current_app
)
from datetime import datetime
import random
import os
from werkzeug.utils import secure_filename

from .courses_data import get_course, get_all_courses, get_course_lesson, get_course_module
from .course_materials import get_quiz, get_practice

education_bp = Blueprint("education", __name__, url_prefix="/education")

# Настройки загрузки файлов
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@education_bp.route("/")
def education_home():
    """Главная страница модуля обучения"""
    courses_data = get_all_courses()
    
    courses = [
        {
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "difficulty": course_data["difficulty"],
            "rating": course_data["rating"],
            "students_count": course_data["students_count"],
            "estimated_time": course_data["estimated_time"],
            "progress": random.randint(0, 100),
        }
        for course_id, course_data in courses_data.items()
    ]

    return render_template(
        "education/education_home.html", 
        courses=courses, 
        featured_courses=courses[:3]
    )

@education_bp.route("/course/<course_id>")
def course_page(course_id):
    """Страница курса с подробным содержанием"""
    course_data = get_course(course_id)
    if not course_data:
        return "Страница не найдена", 404

    # Симуляция прогресса пользователя
    progress = {
        "percentage": random.randint(0, 100),
        "completed": random.randint(0, 20),
        "in_progress": random.randint(0, 5),
        "total": 25,
    }

    # Добавляем информацию о завершении уроков
    for module in course_data["modules"]:
        module["completed_lessons"] = random.randint(0, len(module["lessons"]))
        for lesson in module["lessons"]:
            lesson["completed"] = random.choice([True, False])
            if "sublessons" in lesson:
                for sublesson in lesson["sublessons"]:
                    sublesson["completed"] = random.choice([True, False])

    return render_template(
        "education/course.html",
        course=course_data,
        progress=progress,
        course_completed=progress["percentage"] == 100,
    )

@education_bp.route("/course/<course_id>/lesson/<lesson_id>")
def lesson_page(course_id, lesson_id):
    """Страница урока"""
    lesson_data, module_data = get_course_lesson(course_id, lesson_id)
    if not lesson_data:
        return "Страница не найдена", 404

    course_data = get_course(course_id)

    # Навигация между уроками
    all_lessons = []
    for module in course_data["modules"]:
        all_lessons.extend(module["lessons"])

    current_index = next(
        (i for i, lesson in enumerate(all_lessons) if lesson["id"] == lesson_id), -1
    )
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = (
        all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    )

    return render_template(
        "education/lesson.html",
        course=course_data,
        module=module_data,
        lesson=lesson_data,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
    )

@education_bp.route("/course/<course_id>/module/<module_id>")
def module_detail(course_id, module_id):
    """Детальная страница модуля"""
    module_data = get_course_module(course_id, module_id)
    if not module_data:
        return "Страница не найдена", 404

    course_data = get_course(course_id)
    prev_module = None
    next_module = None

    # Находим соседние модули
    for i, module in enumerate(course_data["modules"]):
        if module["id"] == module_id:
            if i > 0:
                prev_module = course_data["modules"][i - 1]
            if i < len(course_data["modules"]) - 1:
                next_module = course_data["modules"][i + 1]
            break

    return render_template(
        "education/module_detail.html",
        course=course_data,
        module=module_data,
        prev_module=prev_module,
        next_module=next_module,
    )

@education_bp.route("/course/<course_id>/quiz/<lesson_id>")
def lesson_quiz(course_id, lesson_id):
    """Страница теста урока"""
    quiz_data = get_quiz(lesson_id)
    if not quiz_data:
        return "Тест не найден", 404

    course_data = get_course(course_id)
    lesson_data, module_data = get_course_lesson(course_id, lesson_id)
    
    return render_template(
        "education/quiz.html",
        course=course_data,
        lesson=lesson_data,
        module=module_data,
        quiz=quiz_data,
    )

@education_bp.route("/course/<course_id>/practice/<lesson_id>")
def lesson_practice(course_id, lesson_id):
    """Страница практического задания"""
    practice_data = get_practice(lesson_id)
    if not practice_data:
        return "Практическое задание не найдено", 404

    course_data = get_course(course_id)
    lesson_data, module_data = get_course_lesson(course_id, lesson_id)
    
    return render_template(
        "education/practice.html",
        course=course_data,
        lesson=lesson_data,
        module=module_data,
        practice=practice_data,
    )

@education_bp.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    """API для отправки результатов теста"""
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    answers = data.get('answers', {})
    
    quiz_data = get_quiz(lesson_id)
    if not quiz_data:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Проверяем ответы
    results = []
    total_score = 0
    max_score = len(quiz_data['questions'])
    
    for question in quiz_data['questions']:
        question_id = str(question['id'])
        user_answer = answers.get(question_id)
        is_correct = False
        
        if question['type'] == 'multiple_choice':
            is_correct = user_answer == question['correct_answer']
        elif question['type'] == 'multiple_select':
            is_correct = set(user_answer or []) == set(question['correct_answers'])
        elif question['type'] == 'matching':
            is_correct = True
        
        results.append({
            'question_id': question_id,
            'is_correct': is_correct,
            'explanation': question.get('explanation', '')
        })
        
        if is_correct:
            total_score += 1
    
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    
    return jsonify({
        'success': True,
        'score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'results': results,
        'passed': percentage >= 70
    })

@education_bp.route("/course/<course_id>/certificate")
def course_certificate(course_id):
    """Страница сертификата курса"""
    course_data = get_course(course_id)
    if not course_data:
        return "Страница не найдена", 404

    certificate_data = {
        "id": f"CERT-{random.randint(1000, 9999)}",
        "course_name": course_data["title"],
        "student_name": "Иван Иванов",
        "completion_date": datetime.now().strftime("%d.%m.%Y"),
        "score": random.randint(85, 98),
    }

    return render_template(
        "education/certificate.html", 
        course=course_data, 
        certificate=certificate_data
    )

@education_bp.route("/certificates")
def certificates():
    """Страница сертификатов пользователя"""
    certificates_data = [
        {
            "id": 1,
            "course_name": "Основы кибербезопасности",
            "issue_date": "2024-01-15",
            "expiry_date": "2026-01-15",
            "certificate_url": "#",
            "verified": True,
        }
    ]
    return render_template("education/certificates.html", certificates=certificates_data)

@education_bp.route("/achievements")
def achievements():
    """Страница достижений пользователя"""
    achievements_data = [
        {
            "id": 1,
            "name": "Первый шаг",
            "description": "Завершите первый урок",
            "icon": "bi-emoji-smile",
            "earned": True,
            "earned_date": "2024-01-10",
        }
    ]
    return render_template("education/achievements.html", achievements=achievements_data)