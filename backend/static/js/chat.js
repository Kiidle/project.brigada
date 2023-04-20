function scrollToBottom() {
    var chat = document.getElementById("chat-area");
    chat.scrollTop = chat.scrollHeight;
}

window.onload = function () {
    scrollToBottom();
}

const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${wsProtocol}//${window.location.host}/ws/chats/${user.pk}/`;

const socket = new WebSocket(wsUrl);

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const messageType = message.author === user.pk ? 'sent' : 'received';

    const messageElement = document.createElement('div');
    messageElement.classList.add('message', messageType);
    messageElement.innerText = message.content;

    messageContainer.appendChild(messageElement);
};