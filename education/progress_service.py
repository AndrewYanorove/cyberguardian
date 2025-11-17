from database import db
from .models import UserProgress, Course, Module, Lesson, CourseCertificate, UserAchievement
from datetime import datetime

class ProgressService:
    
    @staticmethod
    def initialize_course_data():
        """Инициализация данных курсов в БД"""
        try:
            from .courses_data import COURSES_DATA
            
            for course_id, course_data in COURSES_DATA.items():
                # Проверяем, существует ли курс
                existing_course = Course.query.get(course_id)
                if not existing_course:
                    course = Course(
                        id=course_id,
                        title=course_data['title'],
                        description=course_data['description'],
                        difficulty=course_data['difficulty'],
                        estimated_time=course_data['estimated_time'],
                        rating=course_data.get('rating', 4.5),
                        students_count=course_data.get('students_count', 0)
                    )
                    db.session.add(course)
                
                # Добавляем модули
                for module_index, module_data in enumerate(course_data.get('modules', [])):
                    existing_module = Module.query.get(module_data['id'])
                    if not existing_module:
                        module = Module(
                            id=module_data['id'],
                            course_id=course_id,
                            title=module_data['title'],
                            description=module_data['description'],
                            icon=module_data.get('icon', ''),
                            difficulty=module_data.get('difficulty', 'beginner'),
                            estimated_time=module_data.get('estimated_time', ''),
                            order_index=module_index
                        )
                        db.session.add(module)
                    
                    # Добавляем уроки
                    for lesson_index, lesson_data in enumerate(module_data.get('lessons', [])):
                        existing_lesson = Lesson.query.get(lesson_data['id'])
                        if not existing_lesson:
                            # Собираем контент из подуроков
                            content_parts = []
                            for sublesson in lesson_data.get('sublessons', []):
                                content_parts.append(f"<h3>{sublesson['title']}</h3>")
                                content_parts.append(sublesson.get('content', ''))
                            
                            lesson = Lesson(
                                id=lesson_data['id'],
                                module_id=module_data['id'],
                                title=lesson_data['title'],
                                description=lesson_data['description'],
                                duration=lesson_data.get('duration', 0),
                                content='\n'.join(content_parts),
                                video_url=lesson_data.get('video_url', ''),
                                order_index=lesson_index,
                                has_quiz=lesson_data.get('quiz', False),
                                has_practice=lesson_data.get('practice', False)
                            )
                            db.session.add(lesson)
                
            db.session.commit()
            print("✅ Данные курсов инициализированы в БД")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка инициализации данных курсов: {e}")
            return False

    @staticmethod
    def get_user_progress(user_id, course_id=None):
        """Получить прогресс пользователя"""
        try:
            query = UserProgress.query.filter_by(user_id=user_id)
            if course_id:
                query = query.filter_by(course_id=course_id)
                
            progress_records = query.all()
            return {record.lesson_id: {
                'completed': record.completed,
                'score': record.score,
                'time_spent': record.time_spent,
                'completed_at': record.completed_at
            } for record in progress_records}
        except Exception as e:
            print(f"Ошибка получения прогресса: {e}")
            return {}

    @staticmethod
    def get_course_progress(user_id, course_id):
        """Получить процент завершения курса"""
        try:
            # Получаем все уроки курса из нашей структуры данных
            from .courses_data import get_course
            course_data = get_course(course_id)
            if not course_data:
                return 0
            
            total_lessons = 0
            for module in course_data.get('modules', []):
                total_lessons += len(module.get('lessons', []))
            
            if total_lessons == 0:
                return 0
            
            # Считаем завершенные уроки
            completed_lessons = UserProgress.query.filter_by(
                user_id=user_id, 
                course_id=course_id,
                completed=True
            ).count()
            
            return (completed_lessons / total_lessons) * 100
            
        except Exception as e:
            print(f"Ошибка расчета прогресса курса: {e}")
            return 0

    @staticmethod
    def mark_lesson_completed(user_id, course_id, module_id, lesson_id, score=100, time_spent=0):
        """Отметить урок как завершенный"""
        try:
            # Проверяем, существует ли уже запись
            progress = UserProgress.query.filter_by(
                user_id=user_id,
                lesson_id=lesson_id
            ).first()
            
            if progress:
                # Обновляем существующую запись
                progress.completed = True
                progress.score = max(progress.score, score)
                progress.time_spent += time_spent
                progress.completed_at = datetime.utcnow()
                progress.updated_at = datetime.utcnow()
            else:
                # Создаем новую запись
                progress = UserProgress(
                    user_id=user_id,
                    course_id=course_id,
                    module_id=module_id,
                    lesson_id=lesson_id,
                    completed=True,
                    score=score,
                    time_spent=time_spent,
                    completed_at=datetime.utcnow()
                )
                db.session.add(progress)
            
            db.session.commit()
            
            # Проверяем, завершен ли весь курс
            ProgressService._check_course_completion(user_id, course_id)
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при сохранении прогресса: {e}")
            return False

    @staticmethod
    def mark_quiz_completed(user_id, course_id, module_id, lesson_id, score, max_score, passed):
        """Отметить завершение теста"""
        try:
            # Рассчитываем процент выполнения
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            
            # Если тест пройден успешно, отмечаем урок как завершенный
            if passed and percentage >= 70:
                return ProgressService.mark_lesson_completed(
                    user_id, course_id, module_id, lesson_id, percentage
                )
            else:
                # Если не пройден, просто обновляем счет
                return ProgressService.update_lesson_score(user_id, lesson_id, percentage)
                
        except Exception as e:
            print(f"Ошибка при сохранении результатов теста: {e}")
            return False

    @staticmethod
    def update_lesson_score(user_id, lesson_id, score):
        """Обновить счет урока без отметки о завершении"""
        try:
            progress = UserProgress.query.filter_by(
                user_id=user_id,
                lesson_id=lesson_id
            ).first()
            
            if progress:
                progress.score = max(progress.score, score)
                progress.updated_at = datetime.utcnow()
            else:
                # Используем данные из courses_data чтобы найти module_id и course_id
                from .courses_data import get_all_courses
                courses = get_all_courses()
                
                for course_id, course_data in courses.items():
                    for module in course_data.get('modules', []):
                        for lesson in module.get('lessons', []):
                            if lesson['id'] == lesson_id:
                                progress = UserProgress(
                                    user_id=user_id,
                                    course_id=course_id,
                                    module_id=module['id'],
                                    lesson_id=lesson_id,
                                    completed=False,
                                    score=score,
                                    time_spent=0
                                )
                                db.session.add(progress)
                                break
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при обновлении счета: {e}")
            return False

    @staticmethod
    def update_lesson_time(user_id, lesson_id, time_spent):
        """Обновить время, проведенное в уроке"""
        try:
            progress = UserProgress.query.filter_by(
                user_id=user_id,
                lesson_id=lesson_id
            ).first()
            
            if progress:
                progress.time_spent += time_spent
                progress.updated_at = datetime.utcnow()
            else:
                # Используем данные из courses_data
                from .courses_data import get_all_courses
                courses = get_all_courses()
                
                for course_id, course_data in courses.items():
                    for module in course_data.get('modules', []):
                        for lesson in module.get('lessons', []):
                            if lesson['id'] == lesson_id:
                                progress = UserProgress(
                                    user_id=user_id,
                                    course_id=course_id,
                                    module_id=module['id'],
                                    lesson_id=lesson_id,
                                    completed=False,
                                    score=0,
                                    time_spent=time_spent
                                )
                                db.session.add(progress)
                                break
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при обновлении времени: {e}")
            return False

    @staticmethod
    def _check_course_completion(user_id, course_id):
        """Проверить, завершен ли курс, и выдать сертификат"""
        try:
            # Используем данные из courses_data
            from .courses_data import get_course
            course_data = get_course(course_id)
            if not course_data:
                return False
            
            total_lessons = 0
            for module in course_data.get('modules', []):
                total_lessons += len(module.get('lessons', []))
            
            completed_lessons = UserProgress.query.filter_by(
                user_id=user_id, 
                course_id=course_id, 
                completed=True
            ).count()
            
            if total_lessons > 0 and completed_lessons == total_lessons:
                # Курс завершен - создаем сертификат
                certificate = CourseCertificate.query.filter_by(
                    user_id=user_id,
                    course_id=course_id
                ).first()
                
                if not certificate:
                    certificate = CourseCertificate(
                        user_id=user_id,
                        course_id=course_id,
                        certificate_id=f"CERT-{user_id}-{course_id}-{datetime.utcnow().strftime('%Y%m%d')}",
                        score=ProgressService._calculate_course_score(user_id, course_id)
                    )
                    db.session.add(certificate)
                    
                    # Выдаем достижение
                    achievement = UserAchievement(
                        user_id=user_id,
                        achievement_name=f"Завершение курса: {course_data['title']}",
                        achievement_description=f"Поздравляем с успешным завершением курса {course_data['title']}!",
                        icon="bi-trophy"
                    )
                    db.session.add(achievement)
                    
                    db.session.commit()
                    print(f"🎉 Пользователь {user_id} завершил курс {course_id}!")
                    
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при проверке завершения курса: {e}")
            return False

    @staticmethod
    def _calculate_course_score(user_id, course_id):
        """Рассчитать средний балл по курсу"""
        progress_records = UserProgress.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            completed=True
        ).all()
        
        if not progress_records:
            return 0.0
        
        total_score = sum(record.score for record in progress_records)
        return total_score / len(progress_records)

    @staticmethod
    def get_user_certificates(user_id):
        """Получить сертификаты пользователя"""
        return CourseCertificate.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_achievements(user_id):
        """Получить достижения пользователя"""
        return UserAchievement.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_lesson_progress(user_id, lesson_id):
        """Получить прогресс по конкретному уроку"""
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()
        
        if progress:
            return {
                'completed': progress.completed,
                'score': progress.score,
                'time_spent': progress.time_spent,
                'completed_at': progress.completed_at
            }
        else:
            return {
                'completed': False,
                'score': 0,
                'time_spent': 0,
                'completed_at': None
            }