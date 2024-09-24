const apiUrl = "http://localhost:8000/todos";

// Görevleri yükle
function loadTodos() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(todos => {
            const todoList = document.getElementById('todo-list');
            todoList.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.innerHTML = `${todo.title} - Öncelik: ${todo.priority} - Son Tarih: ${todo.deadline} 
                <button onclick="completeTodo(${todo.id})">${todo.completed ? 'Tamamlandı' : 'Tamamla'}</button>
                <button onclick="deleteTodo(${todo.id})">Sil</button>
                <button onclick="archiveTodo(${todo.id})">Arşivle</button>`;
                todoList.appendChild(li);
            });
        });
}

// Arşivlenmiş görevleri yükle
function loadArchivedTodos() {
    fetch(`${apiUrl}/archived`)
        .then(response => response.json())
        .then(todos => {
            const archivedList = document.getElementById('archived-list');
            archivedList.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.innerHTML = `${todo.title} - Öncelik: ${todo.priority} - Son Tarih: ${todo.deadline}`;
                archivedList.appendChild(li);
            });
        });
}

// Yeni görev ekle
document.getElementById('add-todo').addEventListener('click', function() {
    const title = document.getElementById('todo-input').value;
    const deadline = document.getElementById('deadline-input').value;
    const priority = document.getElementById('priority-select').value;
    
    const newTodo = {
        id: Date.now(),
        title: title,
        completed: false,
        priority: priority,
        deadline: deadline
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newTodo),
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById('todo-input').value = ''; // Input'u temizle
        loadTodos(); // Görevleri yenile
    });
});

// Görev sil
function deleteTodo(id) {
    fetch(`${apiUrl}/${id}`, {
        method: 'DELETE',
    })
    .then(() => loadTodos());
}

// Görev tamamla
function completeTodo(id) {
    fetch(`${apiUrl}/${id}/complete`, {
        method: 'PUT',
    })
    .then(() => loadTodos());
}

// Görev arşivle
function archiveTodo(id) {
    fetch(`${apiUrl}/${id}/archive`, {
        method: 'POST',
    })
    .then(() => loadTodos())
    .then(() => loadArchivedTodos());
}

// Sayfa yüklendiğinde görevleri getir
window.onload = function() {
    loadTodos();
    loadArchivedTodos();
};
