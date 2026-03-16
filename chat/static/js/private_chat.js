

// private_chat.js
const otherUsername = JSON.parse(document.getElementById('other-username').textContent);
const myUsername = JSON.parse(document.getElementById('my-username').textContent);

const chatSocket = new WebSocket(
     (window.location.protocol === "https:" ? 'wss://' : 'ws://') + 
     window.location.host +
     '/ws/private/' + 
     otherUsername + '/'
);

const chatMessages = document.querySelector('#chat-messages');

chatSocket.onopen = function(e) {
    console.log("Private Chat Connected!");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // মেসেজ বাবল তৈরি
    const isMe = data.sender === myUsername; 
    const alignment = isMe ? 'justify-end' : 'justify-start';
    const bgColor = isMe ? 'bg-blue-600 text-white' : 'bg-white border text-gray-800';
    const rounded = isMe ? 'rounded-l-lg rounded-tr-lg' : 'rounded-r-lg rounded-tl-lg';

    const html = `
        <div class="flex ${alignment}">
            <div class="max-w-[70%] px-4 py-2 rounded-2xl shadow-sm ${bgColor} ${rounded}">
                <p class="text-sm">${data.message}</p>
            </div>
        </div>`;
    
    chatMessages.innerHTML += html;
    chatMessages.scrollTop = chatMessages.scrollHeight;
};


document.querySelector('#chat-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInput = document.querySelector('#message-input');
    const message = messageInput.value.trim();

    chatSocket.send(JSON.stringify({
        'message': message,
        'sender': myUsername // এখানে আপনার ইউজারনেম যাচ্ছে
    }));

    messageInput.value = '';
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};