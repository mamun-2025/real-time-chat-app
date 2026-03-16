

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

const chatSocket = new WebSocket(
   'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);
   const chatMessages = document.getElementById('chat-messages');

   const noMsg = document.getElementById('no-messages');
   if (noMsg) {
      noMsg.remove();
   }

   const alignment = data.username === username ? 'items-end' : 'items-start';
   const bgcolor = data.username === username ? 'bg-blue-500 text-white' : 'bg-white text-gray-800 border';

   const messagehtml = `
      <div class="mb-2 flex ${alignment}">
         <div class="max-w-[80%] rounded-lg px-4 py-2 shadow-sm ${bgcolor}">
            <p class="text-xs font-bold mb-1 opacity-75">${data.username}</p>
            <p class="text-sm">${data.message}</p>
         </div>
      </div>`;

      chatMessages.insertAdjacentElement('beforeend', messagehtml);
      chatMessages.scrollTop = chatMessages.scrollHeight;
};


document.getElementById('chat-form').onsubmit = function(e) {
   e.preventDefault();
   const messageInput = document.getElementById('message-input');
   const message = messageInput.value;

   chatSocket.send(JSON.stringify({
      'message': message,
      'username': username
   }));

   messageInput.value = '';
};