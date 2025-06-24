console.log('chat.js loaded', window.chatRoomName);

let chatSocket;

document.addEventListener('DOMContentLoaded', function () {
  const orderId = window.chatRoomName;
  if (!orderId) return;

  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/order/" + window.chatRoomName + "/"
  );

  function addMessage(sender, message, file_url, timestamp, comment, price) {
    const chatLog = document.getElementById('chat-log');
    const isMe = sender === window.currentUser;
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


  chatSocket.onclose = function (e) {
    console.error('WebSocket-зʼєднання закрите неочікувано');
  };

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

  // 🔥 Дублювання з Django-форми "bid-form"
  const bidForm = document.getElementById('bid-form');
  if (bidForm && chatSocket) {
    bidForm.addEventListener('submit', function () {
      event.preventDefault();
      
      const commentInput = document.getElementById('commentInput');
      const priceInput = document.getElementById('priceInput');

      const comment = commentInput ? commentInput.value.trim() : '';
      const price = priceInput ? priceInput.value.trim() : '';

      if (chatSocket.readyState === WebSocket.OPEN && (comment || price)) {
        chatSocket.send(JSON.stringify({
          message: '',
          comment: comment,
          price: price,
          order_id: orderId
        }));
        bidForm.submit();
      }
    });
  }
});
