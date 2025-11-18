from flask import (
    Blueprint, render_template, request, jsonify, session, 
    redirect, url_for, current_app
)
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

from .courses_data import get_course, get_all_courses, get_course_lesson, get_course_module
from .course_materials import get_quiz, get_practice
from .progress_service import ProgressService

education_bp = Blueprint("education", __name__, url_prefix="/education")

@education_bp.route("/")
def education_home():
    """Главная страница модуля обучения"""
    courses_data = get_all_courses()
    
    courses = []
    for course_id, course_data in courses_data.items():
        if current_user.is_authenticated:
            progress = ProgressService.get_course_progress(current_user.id, course_id)
        else:
            progress = 0
            
        courses.append({
            "id": course_id,
            "title": course_data["title"],
            "description": course_data["description"],
            "difficulty": course_data["difficulty"],
            "rating": course_data["rating"],
            "students_count": course_data["students_count"],
            "estimated_time": course_data["estimated_time"],
            "progress": progress,
        })

    return render_template(
        "education/education_home.html", 
        courses=courses, 
        featured_courses=courses[:3]
    )

@education_bp.route("/course/<course_id>")
@login_required
def course_page(course_id):
    """Страница курса с реальным прогрессом"""
    course_data = get_course(course_id)
    if not course_data:
        return "Страница не найдена", 404

    # Получаем реальный прогресс пользователя
    progress_percentage = ProgressService.get_course_progress(current_user.id, course_id)
    user_progress = ProgressService.get_user_progress(current_user.id, course_id)
    
    # Считаем завершенные уроки
    total_lessons = sum(len(module['lessons']) for module in course_data['modules'])
    completed_lessons = sum(1 for p in user_progress.values() if p['completed'])
    
    progress = {
        "percentage": progress_percentage,
        "completed": completed_lessons,
        "in_progress": 0,
        "total": total_lessons,
    }

    # Добавляем информацию о завершении уроков из БД
    for module in course_data["modules"]:
        module_completed = 0
        for lesson in module["lessons"]:
            lesson_progress = user_progress.get(lesson['id'])
            lesson["completed"] = lesson_progress['completed'] if lesson_progress else False
            if lesson["completed"]:
                module_completed += 1
            
            # Обрабатываем подуроки
            if "sublessons" in lesson:
                for sublesson in lesson["sublessons"]:
                    sublesson["completed"] = lesson["completed"]
        
        module["completed_lessons"] = module_completed

    return render_template(
        "education/course.html",
        course=course_data,
        progress=progress,
        course_completed=progress["percentage"] == 100,
    )

@education_bp.route("/course/<course_id>/lesson/<lesson_id>")
@login_required
def lesson_page(course_id, lesson_id):
    """Страница урока с отслеживанием прогресса"""
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

    # Получаем прогресс текущего урока
    lesson_progress = ProgressService.get_lesson_progress(current_user.id, lesson_id)

    return render_template(
        "education/lesson.html",
        course=course_data,
        module=module_data,
        lesson=lesson_data,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
        lesson_progress=lesson_progress
    )

@education_bp.route("/api/lesson/complete", methods=["POST"])
@login_required
def mark_lesson_complete():
    """API для отметки урока как завершенного"""
    data = request.get_json()
    
    course_id = data.get('course_id')
    module_id = data.get('module_id')
    lesson_id = data.get('lesson_id')
    score = data.get('score', 100)
    time_spent = data.get('time_spent', 0)
    
    if not all([course_id, module_id, lesson_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success = ProgressService.mark_lesson_completed(
        current_user.id, course_id, module_id, lesson_id, score, time_spent
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Прогресс сохранен',
            'progress': ProgressService.get_course_progress(current_user.id, course_id)
        })
    else:
        return jsonify({'error': 'Failed to save progress'}), 500

@education_bp.route("/api/lesson/time", methods=["POST"])
@login_required
def update_lesson_time():
    """API для обновления времени, проведенного в уроке"""
    data = request.get_json()
    
    lesson_id = data.get('lesson_id')
    time_spent = data.get('time_spent', 0)
    
    if not lesson_id:
        return jsonify({'error': 'Lesson ID is required'}), 400
    
    success = ProgressService.update_lesson_time(current_user.id, lesson_id, time_spent)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to update time'}), 500

@education_bp.route("/api/quiz/complete", methods=["POST"])
@login_required
def mark_quiz_complete():
    """API для отметки теста как завершенного и обновления прогресса"""
    data = request.get_json()
    
    course_id = data.get('course_id')
    module_id = data.get('module_id')
    lesson_id = data.get('lesson_id')
    score = data.get('score', 0)
    passed = data.get('passed', False)
    
    if not all([course_id, module_id, lesson_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Если тест пройден успешно, отмечаем урок как завершенный
    if passed:
        success = ProgressService.mark_lesson_completed(
            current_user.id, course_id, module_id, lesson_id, score, time_spent=0
        )
    else:
        # Если не пройден, просто обновляем прогресс без завершения
        success = ProgressService.update_lesson_score(
            current_user.id, lesson_id, score
        )
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Результаты теста сохранены',
            'progress': ProgressService.get_course_progress(current_user.id, course_id)
        })
    else:
        return jsonify({'error': 'Failed to save quiz results'}), 500

@education_bp.route("/course/<course_id>/certificate")
@login_required
def course_certificate(course_id):
    """Страница сертификата курса"""
    course_data = get_course(course_id)
    if not course_data:
        return "Страница не найдена", 404

    # Получаем реальный сертификат из БД
    certificates = ProgressService.get_user_certificates(current_user.id)
    user_certificate = next((c for c in certificates if c.course_id == course_id), None)
    
    if not user_certificate:
        return "Сертификат не найден. Завершите курс для получения сертификата.", 404

    certificate_data = {
        "id": user_certificate.certificate_id,
        "course_name": course_data["title"],
        "student_name": current_user.username,
        "completion_date": user_certificate.completion_date.strftime("%d.%m.%Y"),
        "score": user_certificate.score,
    }

    return render_template(
        "education/certificate.html", 
        course=course_data, 
        certificate=certificate_data
    )

@education_bp.route("/certificates")
@login_required
def certificates():
    """Страница сертификатов пользователя"""
    user_certificates = ProgressService.get_user_certificates(current_user.id)
    
    certificates_data = []
    for cert in user_certificates:
        course_data = get_course(cert.course_id)
        if course_data:
            certificates_data.append({
                "id": cert.id,
                "course_name": course_data["title"],
                "issue_date": cert.completion_date.strftime("%Y-%m-%d"),
                "expiry_date": (cert.completion_date.replace(year=cert.completion_date.year + 2)).strftime("%Y-%m-%d"),
                "certificate_url": url_for('education.course_certificate', course_id=cert.course_id),
                "verified": True,
            })
    
    return render_template("education/certificates.html", certificates=certificates_data)

@education_bp.route("/achievements")
@login_required
def achievements():
    """Страница достижений пользователя"""
    user_achievements = ProgressService.get_user_achievements(current_user.id)
    
    achievements_data = []
    for achievement in user_achievements:
        achievements_data.append({
            "id": achievement.id,
            "name": achievement.achievement_name,
            "description": achievement.achievement_description,
            "icon": achievement.icon or "bi-emoji-smile",
            "earned": True,
            "earned_date": achievement.earned_date.strftime("%Y-%m-%d"),
        })
    
    return render_template("education/achievements.html", achievements=achievements_data)

# Остальные маршруты остаются без изменений
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
@login_required
def lesson_quiz(course_id, lesson_id):
    """Страница теста урока"""
    quiz_data = get_quiz(lesson_id)
    if not quiz_data:
        return "Тест не найден", 404

    course_data = get_course(course_id)
    lesson_data, module_data = get_course_lesson(course_id, lesson_id)
    
    # Получаем прогресс урока
    lesson_progress = ProgressService.get_lesson_progress(current_user.id, lesson_id)
    
    return render_template(
        "education/quiz.html",
        course=course_data,
        lesson=lesson_data,
        module=module_data,
        quiz=quiz_data,
        lesson_progress=lesson_progress
    )

@education_bp.route("/course/<course_id>/practice/<lesson_id>")
@login_required
def lesson_practice(course_id, lesson_id):
    """Страница практического задания"""
    practice_data = get_practice(lesson_id)
    if not practice_data:
        return "Практическое задание не найдено", 404

    course_data = get_course(course_id)
    lesson_data, module_data = get_course_lesson(course_id, lesson_id)
    
    # Получаем прогресс урока
    lesson_progress = ProgressService.get_lesson_progress(current_user.id, lesson_id)
    
    return render_template(
        "education/practice.html",
        course=course_data,
        lesson=lesson_data,
        module=module_data,
        practice=practice_data,
        lesson_progress=lesson_progress
    )

@education_bp.route("/api/quiz/submit", methods=["POST"])
@login_required
def submit_quiz():
    """API для отправки результатов теста"""
    data = request.get_json()
    course_id = data.get('course_id')
    module_id = data.get('module_id')
    lesson_id = data.get('lesson_id')
    answers = data.get('answers', {})
    score = data.get('score', 0)
    max_score = data.get('max_score', 0)
    percentage = data.get('percentage', 0)
    passed = data.get('passed', False)

    print(f"Quiz submit received: course_id={course_id}, lesson_id={lesson_id}, score={score}, passed={passed}")

    quiz_data = get_quiz(lesson_id)
    if not quiz_data:
        return jsonify({'error': 'Quiz not found'}), 404

    # Сохраняем результаты теста в прогресс
    if course_id and module_id:
        success = ProgressService.mark_quiz_completed(
            current_user.id, course_id, module_id, lesson_id,
            score, max_score, passed
        )
        print(f"Progress saved: success={success}")
    else:
        success = False
        print("Missing course_id or module_id")

    return jsonify({
        'success': True,
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'passed': passed,
        'progress': ProgressService.get_course_progress(current_user.id, course_id) if course_id else 0
    })

@education_bp.route("/api/practice/complete", methods=["POST"])
@login_required
def mark_practice_complete():
    """API для отметки практического задания как завершенного"""
    data = request.get_json()
    
    course_id = data.get('course_id')
    module_id = data.get('module_id')
    lesson_id = data.get('lesson_id')
    score = data.get('score', 100)
    
    if not all([course_id, module_id, lesson_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success = ProgressService.mark_lesson_completed(
        current_user.id, course_id, module_id, lesson_id, score, time_spent=0
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Практическое задание завершено',
            'progress': ProgressService.get_course_progress(current_user.id, course_id)
        })
    else:
        return jsonify({'error': 'Failed to save practice results'}), 500