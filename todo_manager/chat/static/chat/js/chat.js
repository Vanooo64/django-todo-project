console.log('chat.js loaded', window.chatRoomName);

let chatSocket; // Глобальний — доступний всюди

document.addEventListener('DOMContentLoaded', function () {
  const orderId = window.chatRoomName;
  const currentUser = window.currentUser;
  if (!orderId) return;

  // 📡 Встановлення WebSocket-зʼєднання
  chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/order/" + orderId + "/"
  );

  // 🔵 Індикатор WebSocket зʼєднання
  chatSocket.onopen = function () {
    console.log('✅ WebSocket підʼєднано');
    showStatus("🟢 Зʼєднано з сервером");
  };

  chatSocket.onclose = function (e) {
    console.error('❌ WebSocket-зʼєднання закрите');
    showStatus("🔴 Відключено від сервера");
  };

  // 💬 Вивід повідомлень
  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type === 'chat_history') {
      data.history.forEach(function (msg) {
        const onlyMessage = msg.message && !(msg.comment || msg.price);
        if (onlyMessage) {
          addMessage(msg.sender, msg.message, msg.file_url, msg.timestamp, null, null);
        } else {
          addMessage(msg.sender, '', msg.file_url, msg.timestamp, msg.comment, msg.price);
        }
      });
    } else if (data.type === 'chat_message') {
      const onlyMessage = data.message && !(data.comment || data.price);
      if (onlyMessage) {
        addMessage(data.sender, data.message, null, data.timestamp || '', null, null);
      } else {
        addMessage(data.sender, '', null, data.timestamp || '', data.comment, data.price);
      }
    }
  };

  function addMessage(sender, message, file_url, timestamp, comment, price) {
    const chatLog = document.getElementById('chat-log');
    const isMe = sender === currentUser;
    const msgDiv = document.createElement('div');
    let contentHtml = '';

    if (message) {
      contentHtml += `
        <p class="small p-2 ${isMe ? 'me-3 text-white bg-primary' : 'ms-3 bg-body-tertiary'} mb-1 rounded-3">
          ${message}
        </p>`;
    }

    if (comment) {
      contentHtml += `
        <p class="small p-2 ${isMe ? 'me-3 bg-light text-dark' : 'ms-3 bg-light'} mb-1 rounded-3 border">
          💬 <strong>Коментар:</strong> ${comment}
        </p>`;
    }

    if (price && price !== 'None') {
      contentHtml += `
        <p class="small p-2 ${isMe ? 'me-3 bg-warning text-dark' : 'ms-3 bg-warning'} mb-1 rounded-3 border">
          💰 <strong>Ціна:</strong> ${price} грн
        </p>`;
    }

    contentHtml += `
      <p class="small ${isMe ? 'me-3' : 'ms-3'} mb-3 rounded-3 text-muted">
        ${timestamp || ''}
      </p>`;

    msgDiv.className = 'd-flex flex-row ' +
      (isMe ? 'justify-content-end mb-4 pt-1' : 'justify-content-start mb-4');

    msgDiv.innerHTML = `
      ${!isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
      <div>${contentHtml}</div>
      ${isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
    `;

    chatLog.appendChild(msgDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function sendMessage() {
    const inputField = document.getElementById('chat-message-input');
    const message = inputField.value.trim();
    if (message !== '') {
      chatSocket.send(JSON.stringify({
        message: message,
        order_id: orderId
      }));
      inputField.value = '';
    }
  }

  document.getElementById('chat-message-submit').onclick = function () {
    sendMessage();
  };

  document.getElementById('chat-message-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  });

  // 📦 Надсилання пропозиції (ціна + коментар)
  const bidForm = document.getElementById('bid-form');
  if (bidForm) {
    bidForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const commentInput = document.getElementById('commentInput');
      const priceInput = document.getElementById('priceInput');

      const comment = commentInput ? commentInput.value.trim() : '';
      const price = priceInput ? priceInput.value.trim() : '';

      // Надсилаємо в WebSocket
      if (chatSocket.readyState === WebSocket.OPEN && (comment || price)) {
        chatSocket.send(JSON.stringify({
          message: '',
          comment: comment,
          price: price,
          order_id: orderId
        }));
      }

      // Плавний UX — показ повідомлення
      showStatus("⏳ Надсилаємо пропозицію...", "info");

      // Очищення полів перед сабмітом
      // (але не одразу, щоб не зникло при помилці сабміту)
      setTimeout(() => {
        commentInput.value = '';
        priceInput.value = '';
        showStatus("✅ Пропозиція надіслана", "success");
      }, 500);

      // Сабмітимо форму справжнім POST-запитом
      HTMLFormElement.prototype.submit.call(bidForm);
    });
  }

  // 🧩 Функція статусу зʼєднання / дій
  function showStatus(text, type = "success") {
    let statusDiv = document.getElementById('chat-status');
    if (!statusDiv) {
      statusDiv = document.createElement('div');
      statusDiv.id = 'chat-status';
      statusDiv.style.position = 'fixed';
      statusDiv.style.bottom = '20px';
      statusDiv.style.right = '20px';
      statusDiv.style.zIndex = 10000;
      statusDiv.style.padding = '10px 15px';
      statusDiv.style.borderRadius = '8px';
      statusDiv.style.color = '#fff';
      statusDiv.style.boxShadow = '0 0 8px rgba(0,0,0,0.2)';
      document.body.appendChild(statusDiv);
    }

    const color = {
      success: '#198754',
      danger: '#dc3545',
      warning: '#ffc107',
      info: '#0d6efd'
    }[type] || '#198754';

    statusDiv.textContent = text;
    statusDiv.style.backgroundColor = color;
    statusDiv.style.display = 'block';

    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 3000);
  }
});
