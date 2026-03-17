

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
const messageInput = document.querySelector('#message-input');
const typingIndicator = document.querySelector('#typing-indicator');
const notificationsound = document.getElementById('notification-sound');
let typingTimeout;

chatSocket.onopen = function(e) {
    console.log("Private Chat Connected!");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    //1.Online/Offline status Handle
    if (data.type === 'user_online'){
        const statusText = document.querySelector('#user_online_status_text');
        const statusDot = document.querySelector('#online-status-indicator');
        
       if (data.username === otherUsername) {
            if (data.status === 'online') {
                statusText.textContent = 'Online';
                statusDot.classList.replace('bg-gray-400', 'bg-green-500');
            } else {
                statusText.textContent = 'Offline'; 
                statusDot.classList.replace('bg-green-500', 'bg-gray-400');
            }
        }
        return;
    }

    //2.Typing status handle 
    if (data.type === 'typing_status') {
        if (data.username === otherUsername) {
                typingIndicator.textContent = data.typing ? `${otherUsername} is typing...` : '';           
            }
            return;
        }

    //3.Seen Status Handle 
    if (data.type === 'seen_status') {
        if (data.reader === otherUsername) {
            const allTicks = document.querySelectorAll('.tick-mark');
            allTicks.forEach(tick => {
                tick.classList.remove('text-gray-400');
                tick.classList.add('text-blue-500');
                tick.innerHTML = '✔✔';
            });
        }
        return;
    }

    //4. Message Received Handle 
    if (data.message !== undefined && data.message !== null) {
        const isMe = data.sender === myUsername; 

        if (!isMe && notificationsound) {
            notificationsound.play().catch(error => console.log("Sound error:", error));

            if (document.hasFocus()) {
                chatSocket.send(JSON.stringify({'type': 'mark_as_read'}));
            }
        }

        const alignment = isMe ? 'justify-end' : 'justify-start';
        const bgColor = isMe ? 'bg-rose-700 text-white' : 'bg-white border text-gray-800';
        const rounded = isMe ? 'rounded-l-lg rounded-tr-lg' : 'rounded-r-lg rounded-tl-lg';

        let tickClass = data.is_read ? 'text-blue-500' : 'text-gray-400';
        let tickIcon = data.is_read ? '✔✔' : '✔';
        const tickHtml = isMe ? `<span class="tick-mark ${tickClass} text-[10px] ml-1">${tickIcon}</span>` : '';

        const html = `
            <div class="flex ${alignment}">
                <div class="max-w-[70%] px-4 py-2 rounded-2xl shadow-sm ${bgColor} ${rounded}">
                    <p class="text-sm">${data.message} ${tickHtml}</p>
                </div>
            </div>`;
        
        chatMessages.innerHTML += html;
        scrollToBottom();
    }  
};

window.addEventListener('focus', function() {
    if (chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({
            'type': 'mark_as_read'
        }));
    }
});

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}





// Typing status send handle
if (messageInput) {
    messageInput.addEventListener('input', function() {
        chatSocket.send(JSON.stringify({
            'type': 'typing_status',
            'typing': true,
            'username': myUsername
        }));

// Stop typing status after 3 seconds of inactivity 
        clearTimeout(typingTimeout);
        typingTimer = setTimeout(function() {
            chatSocket.send(JSON.stringify({
                'type': 'typing_status',
                'typing': false,
                'username': myUsername
            }));
        }, 3000);
    });
}






    // Message send handle
document.querySelector('#chat-form').onsubmit = function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender': myUsername 
            }));
        messageInput.value = '';

        // typing status off after sending message 
        chatSocket.send(JSON.stringify({
            'type': 'typing_status',
            'typing': false,
            'username': myUsername 
        }));
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};