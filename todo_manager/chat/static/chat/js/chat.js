console.log('chat.js loaded', window.chatRoomName);

document.addEventListener('DOMContentLoaded', function() {
  const orderId = window.chatRoomName; // Передаємо order_id через глобальну змінну
  if (!orderId) return;

  const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/order/' + orderId + '/'
  );

  // Функція для додавання повідомлення до DOM
  function addMessage(sender, message, file_url, timestamp) {
    const chatLog = document.getElementById('chat-log');
    const isMe = sender === window.currentUser; // Поточний користувач
    const msgDiv = document.createElement('div');

    // Стилізація контейнера повідомлення
    msgDiv.className = 'd-flex flex-row ' +
      (isMe ? 'justify-content-end mb-4 pt-1' : 'justify-content-start mb-4');

    msgDiv.innerHTML = `
      ${!isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
      <div>
        <p class="small p-2 ${isMe ? 'me-3 text-white bg-primary' : 'ms-3 bg-body-tertiary'} mb-1 rounded-3">
          ${message}
        </p>
        <p class="small ${isMe ? 'me-3' : 'ms-3'} mb-3 rounded-3 text-muted">
          ${timestamp || ''}
        </p>
      </div>
      ${isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
    `;
    chatLog.appendChild(msgDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  // Обробка повідомлень, що приходять по WebSocket
  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // Перевірка типу повідомлення
    if (data.type === 'chat_history') {
      // Історія повідомлень – ітеруємо і додаємо кожне повідомлення окремо
      data.history.forEach(function(msg) {
        addMessage(msg.sender, msg.message, msg.file_url, msg.timestamp);
      });
    } else if (data.type === 'chat_message') {
      // Нове повідомлення
      addMessage(data.sender, data.message, data.file_url, data.time || '');
    }
  };

  chatSocket.onclose = function(e) {
    console.error('WebSocket-зʼєднання закрите неочікувано');
  };

  // Функція для надсилання повідомлення
  function sendMessage() {
    const inputField = document.getElementById('chat-message-input');
    const message = inputField.value.trim();
    if (message !== '') {
      chatSocket.send(JSON.stringify({ 'message': message, 'order_id': orderId })); // Додаємо order_id
      inputField.value = ''; // Очищення поля вводу після відправки
    }
  }

  // Надсилання повідомлення по кліку на кнопку
  document.getElementById('chat-message-submit').onclick = function(e) {
    sendMessage();
  };

  // Надсилання повідомлення при натисканні клавіші Enter
  document.getElementById('chat-message-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Запобігаємо стандартному переходу рядка
      sendMessage();
    }
  });
});
