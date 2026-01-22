/**
 * Модуль для работы с данными расписания
 * Хранит данные в формате JSON и управляет LocalStorage
 */

// Инициализация данных расписания
let scheduleData = {
    groups: ['ИСП-401', 'ИСП-402', 'ИСП-403', 'ПРОГ-401', 'ПРОГ-402'],
    days: ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
    timeSlots: [
        { id: 1, time: '8:30 - 10:00' },
        { id: 2, time: '10:10 - 11:40' },
        { id: 3, time: '12:00 - 13:30' },
        { id: 4, time: '13:40 - 15:10' },
        { id: 5, time: '15:20 - 16:50' },
        { id: 6, time: '17:00 - 18:30' }
    ],
    lessons: [
        // Примеры пар для группы ИСП-401
        {
            id: 1,
            group: 'ИСП-401',
            day: 'Понедельник',
            timeSlot: 1,
            subject: 'Программирование',
            teacher: 'Иванова А.П.',
            room: '401',
            type: 'лекция'
        },
        {
            id: 2,
            group: 'ИСП-401',
            day: 'Понедельник',
            timeSlot: 2,
            subject: 'Базы данных',
            teacher: 'Петров С.И.',
            room: '302',
            type: 'практика'
        },
        {
            id: 3,
            group: 'ИСП-401',
            day: 'Вторник',
            timeSlot: 1,
            subject: 'Веб-разработка',
            teacher: 'Сидорова М.К.',
            room: '405',
            type: 'лабораторная'
        },
        // Примеры для других групп
        {
            id: 4,
            group: 'ИСП-402',
            day: 'Понедельник',
            timeSlot: 3,
            subject: 'Математика',
            teacher: 'Кузнецов В.А.',
            room: '201',
            type: 'лекция'
        },
        {
            id: 5,
            group: 'ПРОГ-401',
            day: 'Среда',
            timeSlot: 2,
            subject: 'Алгоритмы',
            teacher: 'Смирнов Д.В.',
            room: '305',
            type: 'практика'
        }
    ]
};

// Ключ для LocalStorage
const STORAGE_KEY = 'smart-schedule-data';

/**
 * Инициализирует данные из LocalStorage или использует дефолтные
 */
function initializeData() {
    const savedData = localStorage.getItem(STORAGE_KEY);
    if (savedData) {
        try {
            scheduleData = JSON.parse(savedData);
            console.log('Данные загружены из LocalStorage');
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            saveData(); // Сохраняем дефолтные данные
        }
    } else {
        saveData(); // Сохраняем дефолтные данные при первом запуске
    }
}

/**
 * Сохраняет данные в LocalStorage
 */
function saveData() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(scheduleData));
        console.log('Данные сохранены в LocalStorage');
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
    }
}

/**
 * Возвращает расписание для конкретной группы
 * @param {string} groupName - Название группы
 * @returns {Array} Массив пар для группы
 */
function getScheduleForGroup(groupName) {
    return scheduleData.lessons.filter(lesson => lesson.group === groupName);
}

/**
 * Добавляет новую пару в расписание
 * @param {Object} lessonData - Данные новой пары
 * @returns {Object} Добавленная пара с ID
 */
function addLesson(lessonData) {
    const newLesson = {
        id: Date.now(), // Генерируем уникальный ID на основе времени
        ...lessonData
    };
    
    scheduleData.lessons.push(newLesson);
    saveData(); // Сохраняем изменения
    
    // Если группа новая, добавляем её в список групп
    if (!scheduleData.groups.includes(lessonData.group)) {
        scheduleData.groups.push(lessonData.group);
        saveData();
    }
    
    return newLesson;
}

/**
 * Удаляет пару из расписания
 * @param {number} lessonId - ID пары для удаления
 * @returns {boolean} Успешно ли удалено
 */
function deleteLesson(lessonId) {
    const initialLength = scheduleData.lessons.length;
    scheduleData.lessons = scheduleData.lessons.filter(lesson => lesson.id !== lessonId);
    
    if (scheduleData.lessons.length < initialLength) {
        saveData();
        return true;
    }
    return false;
}

/**
 * Получает все доступные группы
 * @returns {Array} Массив названий групп
 */
function getAllGroups() {
    return [...scheduleData.groups]; // Возвращаем копию массива
}

/**
 * Получает все дни недели
 * @returns {Array} Массив дней недели
 */
function getAllDays() {
    return [...scheduleData.days];
}

/**
 * Получает все временные слоты
 * @returns {Array} Массив временных слотов
 */
function getAllTimeSlots() {
    return [...scheduleData.timeSlots];
}

/**
 * Получает информацию о временном слоте по ID
 * @param {number} timeSlotId - ID временного слота
 * @returns {Object} Информация о временном слоте
 */
function getTimeSlotById(timeSlotId) {
    return scheduleData.timeSlots.find(slot => slot.id === timeSlotId) || { time: 'Не указано' };
}

/**
 * Фильтрует пары по различным критериям
 * @param {Object} filters - Объект с фильтрами
 * @returns {Array} Отфильтрованный массив пар
 */
function filterLessons(filters = {}) {
    return scheduleData.lessons.filter(lesson => {
        // Проверяем каждый фильтр
        for (const [key, value] of Object.entries(filters)) {
            if (value && lesson[key] !== value) {
                return false;
            }
        }
        return true;
    });
}

// Инициализируем данные при загрузке модуля
initializeData();

// Экспортируем функции для использования в других файлах
export {
    getScheduleForGroup,
    addLesson,
    deleteLesson,
    getAllGroups,
    getAllDays,
    getAllTimeSlots,
    getTimeSlotById,
    filterLessons,
    scheduleData
};
