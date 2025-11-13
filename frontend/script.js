const apiUrl = 'http://127.0.0.1:8001/medical_supplies/';
const tableBody = document.querySelector('#supply-table tbody');
const modal = document.getElementById('supply-modal');
const modalTitle = document.getElementById('modal-title');
const form = document.getElementById('supply-form');
const addSupplyBtn = document.getElementById('add-supply-btn');
const closeBtn = document.querySelector('.close-btn');

// Search form elements
const searchForm = document.getElementById('search-form');
const searchName = document.getElementById('search-name');
const searchCode = document.getElementById('search-code');
const searchCategory = document.getElementById('search-category');
const searchSpecification = document.getElementById('search-specification');
const searchManufacturer = document.getElementById('search-manufacturer');
const searchLocation = document.getElementById('search-location');
const searchMinPrice = document.getElementById('search-min-price');
const searchMaxPrice = document.getElementById('search-max-price');
const searchMinStock = document.getElementById('search-min-stock');
const searchMaxStock = document.getElementById('search-max-stock');
const resetSearchBtn = document.getElementById('reset-search-btn');

// Show modal
function showModal() {
    modal.style.display = 'block';
}

// Hide modal
function hideModal() {
    modal.style.display = 'none';
    form.reset();
    document.getElementById('supply-id').value = '';
}

// Open modal for adding
addSupplyBtn.addEventListener('click', () => {
    modalTitle.textContent = '添加医学耗材';
    showModal();
});

// Close modal
closeBtn.addEventListener('click', hideModal);
window.addEventListener('click', (e) => {
    if (e.target == modal) {
        hideModal();
    }
});

// Fetch and display medical supplies
async function getMedicalSupplies(searchParams = {}) {
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

        const supplies = await response.json();

        tableBody.innerHTML = '';
        supplies.forEach(supply => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${supply.name || ''}</td>
                <td>${supply.code || ''}</td>
                <td>${supply.category || ''}</td>
                <td>${supply.specification || ''}</td>
                <td>${supply.manufacturer || ''}</td>
                <td>${supply.unit || ''}</td>
                <td>${supply.unit_price || ''}</td>
                <td>${supply.stock_quantity || ''}</td>
                <td>${supply.min_stock || ''}</td>
                <td>${supply.expiry_date || ''}</td>
                <td>${supply.batch_number || ''}</td>
                <td>${supply.storage_location || ''}</td>
                <td>${supply.description || ''}</td>
                <td>${supply.remarks || ''}</td>
                <td class="actions">
                    <button class="edit-btn" onclick="editMedicalSupply(${supply.id})">编辑</button>
                    <button class="delete-btn" onclick="deleteMedicalSupply(${supply.id})">删除</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('获取耗材列表失败:', error);
    }
}

// Add or update a medical supply
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('supply-id').value;
    const supplyData = {
        name: document.getElementById('name').value,
        code: document.getElementById('code').value,
        category: document.getElementById('category').value,
        specification: document.getElementById('specification').value,
        manufacturer: document.getElementById('manufacturer').value,
        unit: document.getElementById('unit').value,
        unit_price: parseFloat(document.getElementById('unit_price').value) || null,
        stock_quantity: parseInt(document.getElementById('stock_quantity').value) || null,
        min_stock: parseInt(document.getElementById('min_stock').value) || null,
        expiry_date: document.getElementById('expiry_date').value,
        batch_number: document.getElementById('batch_number').value,
        storage_location: document.getElementById('storage_location').value,
        description: document.getElementById('description').value,
        remarks: document.getElementById('remarks').value,
    };

    try {
        const response = await fetch(id ? `${apiUrl}${id}` : apiUrl, {
            method: id ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(supplyData),
        });

        if (response.ok) {
            hideModal();
            getMedicalSupplies();
        } else {
            console.error('保存耗材失败:', await response.text());
        }
    } catch (error) {
        console.error('保存耗材失败:', error);
    }
});

// Edit a medical supply
async function editMedicalSupply(id) {
    try {
        const response = await fetch(`${apiUrl}${id}`);
        const supply = await response.json();

        modalTitle.textContent = '编辑医学耗材';
        document.getElementById('supply-id').value = supply.id;
        document.getElementById('name').value = supply.name || '';
        document.getElementById('code').value = supply.code || '';
        document.getElementById('category').value = supply.category || '';
        document.getElementById('specification').value = supply.specification || '';
        document.getElementById('manufacturer').value = supply.manufacturer || '';
        document.getElementById('unit').value = supply.unit || '';
        document.getElementById('unit_price').value = supply.unit_price || '';
        document.getElementById('stock_quantity').value = supply.stock_quantity || '';
        document.getElementById('min_stock').value = supply.min_stock || '';
        document.getElementById('expiry_date').value = supply.expiry_date || '';
        document.getElementById('batch_number').value = supply.batch_number || '';
        document.getElementById('storage_location').value = supply.storage_location || '';
        document.getElementById('description').value = supply.description || '';
        document.getElementById('remarks').value = supply.remarks || '';

        showModal();
    } catch (error) {
        console.error('获取耗材信息失败:', error);
    }
}

// Delete a medical supply
async function deleteMedicalSupply(id) {
    if (confirm('您确定要删除这个耗材吗？')) {
        try {
            const response = await fetch(`${apiUrl}${id}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                getMedicalSupplies();
            } else {
                console.error('删除耗材失败:', await response.text());
            }
        } catch (error) {
            console.error('删除耗材失败:', error);
        }
    }
}

// Search medical supplies
searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchParams = {};
    if (searchName.value) searchParams.name = searchName.value;
    if (searchCode.value) searchParams.code = searchCode.value;
    if (searchCategory.value) searchParams.category = searchCategory.value;
    if (searchSpecification.value) searchParams.specification = searchSpecification.value;
    if (searchManufacturer.value) searchParams.manufacturer = searchManufacturer.value;
    if (searchLocation.value) searchParams.storage_location = searchLocation.value;
    if (searchMinPrice.value) searchParams.min_price = parseFloat(searchMinPrice.value);
    if (searchMaxPrice.value) searchParams.max_price = parseFloat(searchMaxPrice.value);
    if (searchMinStock.value) searchParams.min_stock = parseInt(searchMinStock.value);
    if (searchMaxStock.value) searchParams.max_stock = parseInt(searchMaxStock.value);

    getMedicalSupplies(searchParams);
});

resetSearchBtn.addEventListener('click', () => {
    searchForm.reset();
    getMedicalSupplies({}); // Fetch all supplies
});

// Initial load
getMedicalSupplies();

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
        appendMessage('您好！我是您的医学耗材管理助手，有什么可以帮助您的吗？', 'assistant-message');
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
        // 聊天助手返回后自动刷新运动员列表
        setTimeout(() => {
            getAthletes();
        }, 1000);
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
