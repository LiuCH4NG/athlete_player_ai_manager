const apiUrl = 'http://127.0.0.1:8001/athletes/';
const tableBody = document.querySelector('#athlete-table tbody');
const searchInput = document.getElementById('search-input');
const modal = document.getElementById('athlete-modal');
const modalTitle = document.getElementById('modal-title');
const form = document.getElementById('athlete-form');
const addAthleteBtn = document.getElementById('add-athlete-btn');
const closeBtn = document.querySelector('.close-btn');

// Show modal
function showModal() {
    modal.style.display = 'block';
}

// Hide modal
function hideModal() {
    modal.style.display = 'none';
    form.reset();
    document.getElementById('athlete-id').value = '';
}

// Open modal for adding
addAthleteBtn.addEventListener('click', () => {
    modalTitle.textContent = '添加运动员';
    showModal();
});

// Close modal
closeBtn.addEventListener('click', hideModal);
window.addEventListener('click', (e) => {
    if (e.target == modal) {
        hideModal();
    }
});

// Fetch and display athletes
async function getAthletes(query = '') {
    try {
        const url = query ? `http://127.0.0.1:8001/athletes/search/?query=${query}` : apiUrl;
        const response = await fetch(url);
        const athletes = await response.json();

        tableBody.innerHTML = '';
        athletes.forEach(athlete => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${athlete.name}</td>
                <td>${athlete.age}</td>
                <td>${athlete.hometown}</td>
                <td>${athlete.project}</td>
                <td>${athlete.height}</td>
                <td>${athlete.weight}</td>
                <td>${athlete.description}</td>
                <td>${athlete.note}</td>
                <td class="actions">
                    <button class="edit-btn" onclick="editAthlete(${athlete.id})">编辑</button>
                    <button class="delete-btn" onclick="deleteAthlete(${athlete.id})">删除</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('获取运动员列表失败:', error);
    }
}

// Add or update an athlete
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('athlete-id').value;
    const athleteData = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        hometown: document.getElementById('hometown').value,
        project: document.getElementById('project').value,
        height: parseFloat(document.getElementById('height').value),
        weight: parseFloat(document.getElementById('weight').value),
        description: document.getElementById('description').value,
        note: document.getElementById('note').value,
    };

    try {
        const response = await fetch(id ? `${apiUrl}${id}` : apiUrl, {
            method: id ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(athleteData),
        });

        if (response.ok) {
            hideModal();
            getAthletes();
        } else {
            console.error('保存运动员失败:', await response.text());
        }
    } catch (error) {
        console.error('保存运动员失败:', error);
    }
});

// Edit an athlete
async function editAthlete(id) {
    try {
        const response = await fetch(`${apiUrl}${id}`);
        const athlete = await response.json();

        modalTitle.textContent = '编辑运动员';
        document.getElementById('athlete-id').value = athlete.id;
        document.getElementById('name').value = athlete.name;
        document.getElementById('age').value = athlete.age;
        document.getElementById('hometown').value = athlete.hometown;
        document.getElementById('project').value = athlete.project;
        document.getElementById('height').value = athlete.height;
        document.getElementById('weight').value = athlete.weight;
        document.getElementById('description').value = athlete.description;
        document.getElementById('note').value = athlete.note;

        showModal();
    } catch (error) {
        console.error('获取运动员信息失败:', error);
    }
}

// Delete an athlete
async function deleteAthlete(id) {
    if (confirm('您确定要删除这位运动员吗？')) {
        try {
            const response = await fetch(`${apiUrl}${id}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                getAthletes();
            } else {
                console.error('删除运动员失败:', await response.text());
            }
        } catch (error) {
            console.error('删除运动员失败:', error);
        }
    }
}

// Search athletes
searchInput.addEventListener('input', (e) => {
    getAthletes(e.target.value);
});

// Initial load
getAthletes();

// Chat Assistant
const chatFab = document.getElementById('chat-fab');
const chatWindow = document.getElementById('chat-window');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send-btn');
const loadingIndicator = document.querySelector('.loading-indicator');

chatFab.addEventListener('click', () => {
    const isChatOpen = chatWindow.style.display === 'flex';
    chatWindow.style.display = isChatOpen ? 'none' : 'flex';
});

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user-message');
    chatInput.value = '';
    loadingIndicator.style.display = 'block';

    try {
        const response = await fetch(`http://127.0.0.1:8001/chat/?message=${encodeURIComponent(message)}`);
        const data = await response.json();
        const assistantMessage = data.info; // Assuming the response has an 'info' field
        appendMessage(assistantMessage, 'assistant-message');
    } catch (error) {
        console.error('对话助手请求失败:', error);
        appendMessage('抱歉，我现在无法回答。', 'assistant-message');
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

function appendMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);
    messageElement.textContent = text;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatSendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
