// filepath: chat/static/chat/js/chat.js
console.log('chat.js loaded', window.chatRoomName);
document.addEventListener('DOMContentLoaded', function() {
  const roomName = window.chatRoomName; // Передавай roomName через глобальну змінну
  if (!roomName) return;
  const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
  );

  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const chatLog = document.getElementById('chat-log');
    const isMe = data.sender === window.currentUser; // Передавай currentUser через глобальну змінну
    const msgDiv = document.createElement('div');
    msgDiv.className = 'd-flex flex-row ' + (isMe ? 'justify-content-end mb-4 pt-1' : 'justify-content-start mb-4');
    msgDiv.innerHTML = `
      ${!isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
      <div>
        <p class="small p-2 ${isMe ? 'me-3 text-white bg-primary' : 'ms-3 bg-body-tertiary'} mb-1 rounded-3">${data.message}</p>
        <p class="small ${isMe ? 'me-3' : 'ms-3'} mb-3 rounded-3 text-muted">${data.time || ''}</p>
      </div>
      ${isMe ? `<img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp" alt="avatar" style="width: 45px; height: 100%;">` : ''}
    `;
    chatLog.appendChild(msgDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onclose = function(e) {
    console.error('WebSocket-зʼєднання закрите неочікувано');
  };

  document.getElementById('chat-message-submit').onclick = function(e) {
    const inputField = document.getElementById('chat-message-input');
    const message = inputField.value;
    if (message.trim() !== '') {
      chatSocket.send(JSON.stringify({ 'message': message }));
      inputField.value = '';
    }
  };
});