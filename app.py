#!/usr/bin/env python3
"""
Веб-сервер для SmartSchedule - электронного расписания колледжа
Запуск: python app.py
Открыть в браузере: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from datetime import datetime
from flask_cors import CORS

# Инициализация Flask приложения
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Конфигурация
app.config['SECRET_KEY'] = 'smart-schedule-secret-key-2024'
app.config['DATA_FILE'] = 'data/schedule_data.json'

# Создаем папку для данных, если её нет
os.makedirs('data', exist_ok=True)

# Загрузка данных из JSON файла
def load_schedule_data():
    """Загружает данные расписания из JSON файла"""
    try:
        if os.path.exists(app.config['DATA_FILE']):
            with open(app.config['DATA_FILE'], 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
    
    # Возвращаем данные по умолчанию, если файла нет
    return {
        "groups": ["ИСП-401", "ИСП-402", "ИСП-403", "ПРОГ-401", "ПРОГ-402"],
        "days": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
        "time_slots": [
            {"id": 1, "time": "8:30 - 10:00"},
            {"id": 2, "time": "10:10 - 11:40"},
            {"id": 3, "time": "12:00 - 13:30"},
            {"id": 4, "time": "13:40 - 15:10"},
            {"id": 5, "time": "15:20 - 16:50"},
            {"id": 6, "time": "17:00 - 18:30"}
        ],
        "lessons": [
            {
                "id": 1,
                "group": "ИСП-401",
                "day": "Понедельник",
                "time_slot": 1,
                "subject": "Программирование",
                "teacher": "Иванова А.П.",
                "room": "401",
                "type": "лекция"
            },
            {
                "id": 2,
                "group": "ИСП-401",
                "day": "Понедельник",
                "time_slot": 2,
                "subject": "Базы данных",
                "teacher": "Петров С.И.",
                "room": "302",
                "type": "практика"
            },
            {
                "id": 3,
                "group": "ИСП-401",
                "day": "Вторник",
                "time_slot": 1,
                "subject": "Веб-разработка",
                "teacher": "Сидорова М.К.",
                "room": "405",
                "type": "лабораторная"
            }
        ]
    }

# Сохранение данных в JSON файл
def save_schedule_data(data):
    """Сохраняет данные расписания в JSON файл"""
    try:
        with open(app.config['DATA_FILE'], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")
        return False

# ========== МАРШРУТЫ (ROUTES) ==========

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', 
                         title="SmartSchedule - Умное расписание",
                         current_year=datetime.now().year)

@app.route('/about')
def about():
    """Страница "О проекте" """
    team_members = [
        {"name": "Алексей Иванов", "role": "Team Lead / Backend", "description": "Координация проекта, архитектура, Python/Flask"},
        {"name": "Мария Петрова", "role": "Frontend Developer", "description": "Вёрстка, адаптивный дизайн, CSS/HTML"},
        {"name": "Дмитрий Сидоров", "role": "JavaScript Developer", "description": "Интерактивность, формы, AJAX запросы"},
        {"name": "Екатерина Кузнецова", "role": "UI/UX Designer", "description": "Дизайн, иконки, пользовательский опыт"}
    ]
    
    technologies = [
        {"name": "Python", "icon": "fab fa-python"},
        {"name": "Flask", "icon": "fas fa-flask"},
        {"name": "HTML5", "icon": "fab fa-html5"},
        {"name": "CSS3", "icon": "fab fa-css3-alt"},
        {"name": "JavaScript", "icon": "fab fa-js"},
        {"name": "SQLite", "icon": "fas fa-database"}
    ]
    
    return render_template('about.html',
                         title="О проекте - SmartSchedule",
                         team_members=team_members,
                         technologies=technologies,
                         current_year=datetime.now().year)

@app.route('/schedule')
def schedule():
    """Страница с расписанием"""
    data = load_schedule_data()
    return render_template('schedule.html',
                         title="Расписание - SmartSchedule",
                         groups=data['groups'],
                         days=data['days'],
                         current_year=datetime.now().year)

@app.route('/add-event')
def add_event():
    """Страница добавления новой пары"""
    data = load_schedule_data()
    return render_template('add-event.html',
                         title="Добавить пару - SmartSchedule",
                         groups=data['groups'],
                         days=data['days'],
                         time_slots=data['time_slots'],
                         current_year=datetime.now().year)

# ========== API ЭНДПОИНТЫ ==========

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """API: Получить расписание (можно фильтровать)"""
    data = load_schedule_data()
    group = request.args.get('group')
    day = request.args.get('day')
    teacher = request.args.get('teacher')
    
    lessons = data['lessons']
    
    # Применяем фильтры
    if group:
        lessons = [lesson for lesson in lessons if lesson['group'] == group]
    if day:
        lessons = [lesson for lesson in lessons if lesson['day'] == day]
    if teacher:
        lessons = [lesson for lesson in lessons if teacher.lower() in lesson['teacher'].lower()]
    
    return jsonify({
        "success": True,
        "data": {
            "lessons": lessons,
            "total": len(lessons),
            "groups": data['groups'],
            "days": data['days'],
            "time_slots": data['time_slots']
        }
    })

@app.route('/api/schedule', methods=['POST'])
def add_lesson():
    """API: Добавить новую пару"""
    try:
        data = load_schedule_data()
        lesson_data = request.json
        
        # Генерируем новый ID
        new_id = max([lesson['id'] for lesson in data['lessons']], default=0) + 1
        
        # Создаём новую пару
        new_lesson = {
            "id": new_id,
            "group": lesson_data.get('group', ''),
            "day": lesson_data.get('day', ''),
            "time_slot": int(lesson_data.get('time_slot', 1)),
            "subject": lesson_data.get('subject', ''),
            "teacher": lesson_data.get('teacher', ''),
            "room": lesson_data.get('room', ''),
            "type": lesson_data.get('type', 'лекция')
        }
        
        # Добавляем в данные
        data['lessons'].append(new_lesson)
        
        # Добавляем группу, если её нет
        if new_lesson['group'] not in data['groups']:
            data['groups'].append(new_lesson['group'])
        
        # Сохраняем
        if save_schedule_data(data):
            return jsonify({
                "success": True,
                "message": "Пара успешно добавлена",
                "lesson": new_lesson
            })
        else:
            return jsonify({
                "success": False,
                "message": "Ошибка сохранения данных"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка сервера: {str(e)}"
        }), 500

@app.route('/api/schedule/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
    """API: Удалить пару по ID"""
    try:
        data = load_schedule_data()
        
        # Ищем и удаляем пару
        initial_count = len(data['lessons'])
        data['lessons'] = [lesson for lesson in data['lessons'] if lesson['id'] != lesson_id]
        
        if len(data['lessons']) < initial_count:
            save_schedule_data(data)
            return jsonify({
                "success": True,
                "message": "Пара успешно удалена"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Пара не найдена"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка сервера: {str(e)}"
        }), 500

@app.route('/api/current-lesson')
def get_current_lesson():
    """API: Получить текущую пару (на основе времени сервера)"""
    data = load_schedule_data()
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = now.weekday()  # 0-Понедельник, 6-Воскресенье
    
    # Соответствие дней недели
    weekdays_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    current_day = weekdays_ru[current_weekday] if current_weekday < 6 else None
    
    if not current_day:
        return jsonify({"current_lesson": None})
    
    # Ищем текущую пару
    for lesson in data['lessons']:
        if lesson['day'] == current_day:
            # Простая логика: если сейчас между 8:30 и 18:30
            if 8 <= current_hour <= 18:
                return jsonify({
                    "current_lesson": lesson,
                    "current_time": f"{current_hour}:{current_minute:02d}"
                })
    
    return jsonify({"current_lesson": None})

# ========== СТАТИЧЕСКИЕ ФАЙЛЫ ==========

@app.route('/static/<path:path>')
def serve_static(path):
    """Отдача статических файлов"""
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    """Favicon"""
    return send_from_directory('static', 'favicon.ico')

# ========== ЗАПУСК СЕРВЕРА ==========

if __name__ == '__main__':
    print("=" * 50)
    print("ЗАПУСК СЕРВЕРА SMART SCHEDULE")
    print("=" * 50)
    print("Сервер запущен на http://localhost:5000")
    print("Доступные страницы:")
    print("  • http://localhost:5000/          - Главная страница")
    print("  • http://localhost:5000/about     - О проекте")
    print("  • http://localhost:5000/schedule  - Расписание")
    print("  • http://localhost:5000/add-event - Добавить пару")
    print("\nДля остановки сервера нажмите Ctrl+C")
    print("=" * 50)
    
    # Запуск сервера с горячей перезагрузкой (debug=True для разработки)
    app.run(host='0.0.0.0', port=5000, debug=True)
