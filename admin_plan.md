# План исправления админ-панели

## ✅ Что уже исправлено:
- Модель User: `user_is_active` (column) + `is_active` (property) - правильно реализовано
- Безопасность: CSRF защита, rate limiting, session security

## ❌ Что нужно исправить:

### 1. Архитектура - создать модуль admin
- [ ] Создать admin/__init__.py  
- [ ] Создать admin/routes.py
- [ ] Перенести админ функциональность из app.py в admin/routes.py
- [ ] Обновить app.py для импорта admin blueprint

### 2. API endpoints - перенести из app.py
- [ ] /api/admin/delete-user
- [ ] /api/admin/ban-user  
- [ ] /api/admin/unban-user
- [ ] /api/admin/get-users-stats
- [ ] Обновить все ссылки в templates

### 3. Безопасность - улучшить role-based access
- [ ] Добавить proper проверку ролей администратора
- [ ] Улучшить аудит действий администратора
- [ ] Добавить логирование действий

### 4. Тестирование
- [ ] Протестировать все API endpoints после переноса
- [ ] Проверить UI админ-панели
- [ ] Протестировать CRUD операции

## Файлы для редактирования:
1. **admin/__init__.py** - создать blueprint
2. **admin/routes.py** - перенести все админ функции
3. **app.py** - удалить админ код, добавить импорт admin blueprint
4. **templates/admin_panel.html** - обновить ссылки на API

## Порядок выполнения:
1. Создать admin модуль
2. Перенести функции  
3. Обновить app.py
4. Протестировать
