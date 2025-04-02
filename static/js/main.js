document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const sendBtn = document.querySelector('.send-btn');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const gameContainer = document.getElementById('game-container');
    const startScreen = document.getElementById('start-screen');

    let detectiveName = '';
    let prisonerName = '';
    let currentChatHistory = '';

    startBtn.addEventListener('click', async () => {
        detectiveName = document.getElementById('detective-name').value.trim();

        if (!detectiveName) {
            alert("Введите имя!");
            return;
        }

        try {
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ detective_name: detectiveName })
            });

            const data = await response.json();

            if (response.ok) {
                prisonerName = data.prisoner_name;
                startScreen.style.display = 'none';
                gameContainer.style.display = 'block';

                data.initial_messages.forEach(msg => {
                    addToChat(msg);
                    currentChatHistory += msg + '\n';
                });
            } else {
                alert(data.error || "Ошибка при запуске игры");
            }
        } catch (error) {
            console.error('Error:', error);
            alert("Ошибка соединения с сервером");
        }
    });

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const message = userInput.value.trim();

        if (!message) {
            alert("Пожалуйста, введите сообщение!");
            return;
        }

        addToChat(`${detectiveName}: ${message}`);
        userInput.value = '';

        try {
            const response = await fetch('/api/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    chat_history: currentChatHistory,
                    detective_name: detectiveName
                })
            });

            const data = await response.json();

            if (response.ok) {
                addToChat(data.response);
                currentChatHistory = data.updated_history;
            } else {
                alert(data.error || "Ошибка при отправке сообщения");
            }
        } catch (error) {
            console.error('Error:', error);
            alert("Ошибка соединения с сервером");
        }
    }

    function addToChat(text, className = '') {
        const message = document.createElement('p');
        message.textContent = text;
        if (className) message.className = className;
        chatHistory.appendChild(message);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});