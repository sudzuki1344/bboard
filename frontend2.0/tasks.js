// Адрес нашего API
const apiDomain = 'http://localhost:8000/api/';

// Функция для загрузки списка задач
async function loadTasks() {
    try {
        const response = await fetch(`${apiDomain}tasks/`);
        if (response.ok) {
            const tasks = await response.json();
            const taskListDiv = document.getElementById('task-list');
            let tasksHTML = '<ul>';
            tasks.forEach(task => {
                tasksHTML += `<li>${task.title} – ${task.completed ? 'Выполнено' : 'Не выполнено'}</li>`;
            });
            tasksHTML += '</ul>';
            taskListDiv.innerHTML = tasksHTML;
        } else {
            console.error('Ошибка загрузки задач:', response.statusText);
        }
    } catch (e) {
        console.error('Ошибка запроса:', e);
    }
}

// Функция для загрузки списка пользователей
async function loadUsers() {
    try {
        const response = await fetch(`${apiDomain}users/`);
        if (response.ok) {
            const users = await response.json();
            const userListDiv = document.getElementById('user-list');
            let usersHTML = '<ul>';
            users.forEach(user => {
                usersHTML += `<li>${user.username} (${user.email})</li>`;
            });
            usersHTML += '</ul>';
            userListDiv.innerHTML = usersHTML;
        } else {
            console.error('Ошибка загрузки пользователей:', response.statusText);
        }
    } catch (e) {
        console.error('Ошибка запроса:', e);
    }
}

// Обработчик формы для создания новой задачи
document.getElementById('task-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    // Получаем значения полей формы
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const completed = document.getElementById('completed').checked;
    
    const newTask = {
        title: title,
        description: description,
        completed: completed
    };
    
    try {
        const response = await fetch(`${apiDomain}tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newTask)
        });
        if (response.ok) {
            // После успешного создания обновляем список задач и очищаем форму
            loadTasks();
            document.getElementById('task-form').reset();
        } else {
            console.error('Ошибка создания задачи:', response.statusText);
        }
    } catch (e) {
        console.error('Ошибка запроса:', e);
    }
});

// При загрузке страницы инициируем запросы к API
window.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadUsers();
}); 