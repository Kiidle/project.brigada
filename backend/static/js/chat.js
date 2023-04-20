function scrollToBottom() {
    var chat = document.getElementById("chat-area");
    chat.scrollTop = chat.scrollHeight;
}

window.onload = function () {
    scrollToBottom();
}