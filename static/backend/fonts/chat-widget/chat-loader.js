document.addEventListener('DOMContentLoaded', function() {
  // Define the current domain (you can modify this for a live server)
  var ajaxDomain = 'http://127.0.0.1:8000/';

  // Initialize chatbot appearance settings
  var botId = "Q7T73X7X7DUVHIM";  // Chatbot ID, modify as per your chatbot setup

  // Create HTML structure for the chatbot widget
  var chatbotHTML = `
    <div id="chatbot-container" style="position: fixed; bottom: 20px; right: 20px; width: 350px; height: 450px; background-color: #fff; border-radius: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); display: none; flex-direction: column; transition: all 0.3s ease;">
      <div id="chat-header" style="background-color: #aa4caf; color: #fff; padding: 15px; text-align: center; border-top-left-radius: 20px; border-top-right-radius: 20px;">
        <h3 style="margin: 0;">ChatBot Support</h3>
      </div>
      <div id="chat-messages" style="flex: 1; padding: 20px; overflow-y: auto; font-size: 14px; color: #333; border-bottom: 1px solid #f0f0f0;">
        <div id="bot-message" style="margin-bottom: 10px;">
          <p><strong>Chat Bot:</strong> Hello! How can I help you today?</p>
        </div>
      </div>
      <div id="chat-input" style="padding: 15px; background-color: #f7f7f7; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; display: flex; align-items: center;">
        <input type="text" id="user-message" style="flex: 1; padding: 10px 15px; border-radius: 20px; border: 1px solid #ccc; font-size: 14px; outline: none;" placeholder="Type your message..." />
        <button id="send-message" style="padding: 10px 20px; margin-left: 10px; background-color: #aa4caf; color: white; border: none; border-radius: 20px; cursor: pointer; font-size: 14px; transition: background-color 0.3s;">
          Send
        </button>
      </div>
    </div>
    <button id="chatbot-toggle" style="position: fixed; bottom: 80px; right: 20px; background-color: #aa4caf; color: white; border-radius: 50%; width: 60px; height: 60px; border: none; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
      <span style="font-size: 30px;">💬</span>
    </button>
  `;

  // Append chatbot HTML to the body
  document.body.insertAdjacentHTML('beforeend', chatbotHTML);

  // Toggle chatbot visibility
  document.getElementById('chatbot-toggle').addEventListener('click', function() {
    var chatbot = document.getElementById('chatbot-container');
    chatbot.style.display = (chatbot.style.display === 'none' || chatbot.style.display === '') ? 'flex' : 'none';
  });

  // Handle sending messages
  document.getElementById('send-message').addEventListener('click', function() {
    var userMessage = document.getElementById('user-message').value;
    if (userMessage.trim() !== '') {
      var chatMessages = document.getElementById('chat-messages');
      chatMessages.innerHTML += `
        <div class="user-message" style="margin-bottom: 10px; text-align: right;">
          <p><strong>You:</strong> ${userMessage}</p>
        </div>
      `;
      document.getElementById('user-message').value = ''; // Clear input field

      // Simulate bot response (you can connect this to a backend API for real responses)
      setTimeout(function() {
        chatMessages.innerHTML += `
          <div class="bot-message" style="margin-bottom: 10px; text-align: left;">
            <p><strong>Bot:</strong> I am here to help with your queries!</p>
          </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight; 
      }, 1000);
    }
  });
});
