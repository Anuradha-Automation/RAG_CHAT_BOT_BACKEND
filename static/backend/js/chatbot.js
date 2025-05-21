document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message");
    const sendButton = document.getElementById("send");
    const chatHistory = document.getElementById("chat-history-ul");

    sendButton.addEventListener("click", function (event) {
        event.preventDefault();
        const userMessage = messageInput.value.trim();
        if (userMessage !== "") {
            addMessageToChat(userMessage, "user");
            sendMessageToAPI(userMessage);
            messageInput.value = "";
        }
    });

    function sendMessageToAPI(message) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Get CSRF token
        var chat_bot_url = $('#chat_bot_url').val()
        fetch(chat_bot_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  
            },
            body: JSON.stringify({ query: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            if (data && data.results && data.results.length > 0) {
                addMessageToChat(data.results[0].text, "bot");
            } else {
                addMessageToChat("No response from the bot.", "bot");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            addMessageToChat("Error fetching response. Please try again.", "bot");
        });
    }
    function addMessageToChat(message, sender) {
        const chatMessage = document.createElement("li");
        chatMessage.classList.add("chat-message");

        if (sender === "user") {
            chatMessage.classList.add("chat-message-right");
            chatMessage.innerHTML = `
                <div class="chat-message-wrapper flex-grow-1">
                    <div class="chat-message-text user-msg-background">
                        <p class="mb-0">${message}</p>
                    </div>
                    <div class="text-end text-muted">
                        <small>${new Date().toLocaleString()}</small>
                    </div>
                </div>
            `;
        } else {
            chatMessage.innerHTML = `
                <div class="d-flex overflow-hidden">
                    <div class="chat-message-wrapper flex-grow-1">
                        <div class="chat-message-text chatbot-msg-background">
                            <p class="mb-0">${message}</p>
                        </div>
                        <div class="text-muted">
                            <small>${new Date().toLocaleString()}</small>
                        </div>
                    </div>
                </div>
            `;
        }

        chatHistory.appendChild(chatMessage);
        chatHistory.scrollTop = chatHistory.scrollHeight;  // Scroll to bottom
    }
});
