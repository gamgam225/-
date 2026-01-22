/**
 * Модуль для работы с таблицей расписания
 */

import { 
    getScheduleForGroup, 
    getAllGroups, 
    getTimeSlotById,
    filterLessons 
} from './data.js';

// DOM элементы
let currentGroup = 'ИСП-401';
const scheduleTable = document.getElementById('schedule-table');
const groupFilter = document.getElementById('group-filter');
const teacherFilter = document.getElementById('teacher-filter');
const roomFilter = document.getElementById('room-filter');
const currentLessonIndicator = document.getElementById('current-lesson');

/**
 * Инициализирует страницу расписания
 */
function initSchedulePage() {
    if (!scheduleTable) return; // Если не на странице расписания, выходим
    
    loadFilters();
    renderSchedule();
    setupEventListeners();
    highlightCurrentLesson();
}

/**
 * Загружает данные в фильтры
 */
function loadFilters() {
    // Загружаем группы
    const groups = getAllGroups();
    groupFilter.innerHTML = '<option value="">Все группы</option>';
    groups.forEach(group => {
        const option = document.createElement('option');
        option.value = group;
        option.textContent = group;
        if (group === currentGroup) option.selected = true;
        groupFilter.appendChild(option);
    });
    
    // Получаем уникальных преподавателей и аудитории для фильтров
    const uniqueTeachers = [...new Set
