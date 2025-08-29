// --- 配置部分 ---
// 为了便于部署和避免前端构建工具的复杂性（如处理 process.env），
// 这里直接定义 API 的基础 URL。
// 如果前端和后端部署在同一个域名下（例如，通过反向代理或直接由后端提供静态文件），
// 则可以使用相对路径 '/'。
// 如果前端和后端是分离部署的，则需要将 'apiBaseUrl' 设置为后端 API 的完整基础 URL。
// 例如: const apiBaseUrl = 'http://your-backend-domain.com';
// 注意：修改此配置后，需要重新部署前端代码。

// 默认使用相对路径 '/'，假设前端静态文件和 API 由同一个后端服务提供
const apiBaseUrl = '';
// 如果是分离部署，请取消下面一行的注释，并设置正确的后端地址
// const apiBaseUrl = 'http://your-backend-api-domain.com';

const apiUrl = `${apiBaseUrl}/athletes/`;
// --- 配置部分结束 ---
const tableBody = document.querySelector('#athlete-table tbody');
const modal = document.getElementById('athlete-modal');
const modalTitle = document.getElementById('modal-title');
const form = document.getElementById('athlete-form');
const addAthleteBtn = document.getElementById('add-athlete-btn');
const closeBtn = document.querySelector('.close-btn');

// Search form elements
const searchForm = document.getElementById('search-form');
const searchName = document.getElementById('search-name');
const searchSportEvent = document.getElementById('search-sport-event');
const searchHometown = document.getElementById('search-hometown');
const searchMinAge = document.getElementById('search-min-age');
const searchMaxAge = document.getElementById('search-max-age');
const searchMinHeight = document.getElementById('search-min-height');
const searchMaxHeight = document.getElementById('search-max-height');
const searchMinWeight = document.getElementById('search-min-weight');
const searchMaxWeight = document.getElementById('search-max-weight');
const resetSearchBtn = document.getElementById('reset-search-btn');

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
async function getAthletes(searchParams = {}) {
    try {
        let response;
        if (Object.keys(searchParams).length > 0) {
            response = await fetch(`${apiUrl}search/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchParams),
            });
        } else {
            response = await fetch(apiUrl);
        }

        const athletes = await response.json();

        tableBody.innerHTML = '';
        athletes.forEach(athlete => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${athlete.name || ''}</td>
                <td>${athlete.age || ''}</td>
                <td>${athlete.hometown || ''}</td>
                <td>${athlete.sport_event || ''}</td>
                <td>${athlete.height || ''}</td>
                <td>${athlete.weight || ''}</td>
                <td>${athlete.description || ''}</td>
                <td>${athlete.remarks || ''}</td>
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
        age: parseInt(document.getElementById('age').value) || null,
        hometown: document.getElementById('hometown').value,
        sport_event: document.getElementById('sport_event').value,
        height: parseFloat(document.getElementById('height').value) || null,
        weight: parseFloat(document.getElementById('weight').value) || null,
        description: document.getElementById('description').value,
        remarks: document.getElementById('remarks').value,
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
        document.getElementById('name').value = athlete.name || '';
        document.getElementById('age').value = athlete.age || '';
        document.getElementById('hometown').value = athlete.hometown || '';
        document.getElementById('sport_event').value = athlete.sport_event || '';
        document.getElementById('height').value = athlete.height || '';
        document.getElementById('weight').value = athlete.weight || '';
        document.getElementById('description').value = athlete.description || '';
        document.getElementById('remarks').value = athlete.remarks || '';

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
searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchParams = {};
    if (searchName.value) searchParams.name = searchName.value;
    if (searchSportEvent.value) searchParams.sport_event = searchSportEvent.value;
    if (searchHometown.value) searchParams.hometown = searchHometown.value;
    if (searchMinAge.value) searchParams.min_age = parseInt(searchMinAge.value);
    if (searchMaxAge.value) searchParams.max_age = parseInt(searchMaxAge.value);
    if (searchMinHeight.value) searchParams.min_height = parseFloat(searchMinHeight.value);
    if (searchMaxHeight.value) searchParams.max_height = parseFloat(searchMaxHeight.value);
    if (searchMinWeight.value) searchParams.min_weight = parseFloat(searchMinWeight.value);
    if (searchMaxWeight.value) searchParams.max_weight = parseFloat(searchMaxWeight.value);

    getAthletes(searchParams);
});

resetSearchBtn.addEventListener('click', () => {
    searchForm.reset();
    getAthletes({}); // Fetch all athletes
});

// Initial load
getAthletes();

// Chat Assistant
const chatFab = document.getElementById('chat-fab');
const chatWindow = document.getElementById('chat-window');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send-btn');
const markdownConverter = new showdown.Converter();

chatFab.addEventListener('click', () => {
    const isChatOpen = chatWindow.style.display === 'flex';
    chatWindow.style.display = isChatOpen ? 'none' : 'flex';

    // Add initial message if chat is opened for the first time
    if (!isChatOpen && chatMessages.children.length === 0) {
        appendMessage('您好！我是您的运动员管理助手，有什么可以帮助您的吗？', 'assistant-message');
    }
});

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user-message');
    chatInput.value = '';

    // Create and append typing indicator
    const typingIndicatorElement = document.createElement('div');
    typingIndicatorElement.classList.add('typing-indicator', 'chat-message');
    typingIndicatorElement.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typingIndicatorElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`http://127.0.0.1:8001/chat/?message=${encodeURIComponent(message)}`);
        const data = await response.json();
        const assistantMessage = data.info; // Assuming the response has an 'info' field
        appendMessage(assistantMessage, 'assistant-message');
    } catch (error) {
        console.error('对话助手请求失败:', error);
        appendMessage('抱歉，我现在无法回答。', 'assistant-message');
    } finally {
        // Remove typing indicator
        if (typingIndicatorElement.parentNode === chatMessages) {
            chatMessages.removeChild(typingIndicatorElement);
        }
    }
}

function appendMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);

    if (className === 'assistant-message') {
        messageElement.innerHTML = markdownConverter.makeHtml(text);
    } else {
        messageElement.textContent = text;
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatSendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
