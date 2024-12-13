let socket;
let username = "";

// Function to join the chat room
function joinChat() {
    username = document.getElementById("username").value;
    if (username.trim() === "") {
        alert("Please enter a username.");
        return;
    }

    socket = new WebSocket("ws://localhost:6800");

    socket.onopen = () => {
        socket.send(JSON.stringify({ command: "join_room", username: username }));
        document.getElementById("username-input-container").style.display = "none";
        document.getElementById("message-input-container").style.display = "flex";
    };

    socket.onmessage = (event) => {
        const chatBox = document.getElementById("chat-box");
        const message = document.createElement("p");
        message.textContent = event.data;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    socket.onclose = () => {
        alert("Disconnected from the chat room.");
    };
}

// Function to send a message to the chat room
function sendMessage() {
    const messageInput = document.getElementById("message");
    const messageText = messageInput.value.trim();
    if (messageText === "") return;

    const messageData = {
        command: "send_msg",
        message: messageText
    };

    socket.send(JSON.stringify(messageData));
    messageInput.value = "";
}

// Close the WebSocket connection when leaving the page
window.onbeforeunload = () => {
    if (socket) {
        socket.send(JSON.stringify({ command: "leave_room" }));
        socket.close();
    }
};
