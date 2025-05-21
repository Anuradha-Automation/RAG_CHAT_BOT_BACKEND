
function getCSRFToken() {
  let cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.startsWith("csrftoken=")) {
          return cookie.split("=")[1];
      }
  }
  return "";
}

let  ajaxResult = null;
const Ajax_response = async (url, method, values, beforetask, success, callback) => {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    jQuery.ajaxSetup({headers: {'X-CSRF-TOKEN': getCSRFToken()}});
    return jQuery.ajax({
        type: method,
        url: url,
        data: values,
        beforeSend: function (msg) {
        },
        success: function (msg) {
            callback
        },
        error: function (_request, status, _error) {
        }
    });
};
(async function() {
    document.head.insertAdjacentHTML('beforeend', '<link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.16/tailwind.min.css" rel="stylesheet" />');
    document.head.insertAdjacentHTML('beforeend', '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" />');
    document.head.insertAdjacentHTML('beforeend', '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=0" />');
    let ajaxDomain = document.querySelector('script[base_url]')?.getAttribute('base_url');
    // Current Script data
    var botCurrentScript = document.currentScript;
    var botId = botCurrentScript.getAttribute('chatbot-id');
     // save visitor's data and get visitor id
     var visitor_id = null
     var full_url = `${ajaxDomain}/api/v2/chatbot/appearances/?chat_id=${botId}&type=json`;
     const [response] = await Promise.all([Ajax_response(full_url, "GET", {}, '')]);
     if (response.status === 'success') {
        data = response.data
        var chatbot = data.chatbot
        var chatbot_title = data.chatbot_title
        var display_name = data.display_name
        var footer_name = data.footer_name
        var initial_message = data.initial_message
        var chatbot_theme = data.chatbot_theme
        var chatbot_mode = data.chatbot_mode
        var suggested_messages = data.suggested_messages
        var chatbot_image = data.chatbot_image
        var top_bar_background = data.top_bar_background
        var top_bar_textcolor = data.top_bar_textcolor
        var bot_message_background = data.bot_message_background
        var bot_message_color = data.bot_message_color
        var user_message_background = data.user_message_background
        var user_message_color = data.user_message_color
        var chatbot_background_color = data.chatbot_background_color
        var chatbot_background_pattern = data.chatbot_background_pattern
        var chatbot_launcher_icon = data.chatbot_launcher_icon
        var font_family = data.font_family
        var font_size = data.font_size
        var widget_width = data.widget_width
        var widget_height = data.widget_height
        var widget_position = data.widget_position
        var show_popup_notification = data.show_popup_notification
        var delay_showing_popup_notification = data.delay_showing_popup_notification
  
        localStorage.setItem("chatbot_image", chatbot_image);
  
        if (widget_width === null || widget_width === undefined || widget_width === '') {
          widget_width = '25%'
        } else {
          widget_width = widget_width;
        }
  
        styleData = `
                .top-bar-background{
                 background-color:${top_bar_background} !important;
                }
                .chatbot-background {
                  background-color : ${chatbot_background_color} !important;
                }
  
                .chatbot-pattern {
               background-image: url(${ajaxDomain }${chatbot_background_pattern}) !important;
                }
  
              .chatbot-font-family {
                font-family: ${font_family} !important;
                  }
  
          .chatbot-font-size {
                 font-family: ${font_size} !important;
               }
        .chatbot_theme {
                 font-family: ${font_size} !important;
               }
  
            #chat-messages{
            color: ${bot_message_color } !important;
            padding: 20px;
            font-size:15px;
            font-weight: 400;
            font-weight: 400;
          }
  
          .chatbot-msg-background {
      background-color: ${ajaxDomain }${bot_message_background } !important;
      height: auto;
      width: auto;
          border-radius: 0 10px 10px 10px;
  }
  
    #chat-submit {
              background-color: ${chatbot_theme} !important;;
              color: #fff;
              padding: 8px 15px;
              border: none;
              border-radius: 5px;
              cursor: pointer;
          }
  .user-msg-color{
    color: #000000 !important;
     padding: 20px;
     font-size:15px;
     font-weight: 400;
  }
  
          .avatar {
              width: 3rem !important;
              height: 3rem !important;
              cursor: pointer;
          }
          .sticky-powerdby {
              background: lightgray;
          }
           #footerContainer {
                  width: 420px;
                  min-height: 100px;
                  border: 1px solid #ccc;
                  padding: 10px;
                  box-sizing: border-box;
                  overflow: hidden;
              }
  #chatbot-initial-messages{
    color:${bot_message_color } !important;
    padding: 20px;
    font-size:15px;
    font-weight: 400;
    font-weight: 400;
  }
  
  
  .user-msg-background {
      background-color: #ffffff;
      height: auto;
      width: auto;
          border-radius: 10px 0px 10px 10px;
  } `
        const styleElement = document.createElement("style");
  
        // Set the content of the <style> element to the styleData
        styleElement.innerHTML = styleData;
  
        // Append the <style> element to the <head> section of the document
        document.head.appendChild(styleElement);
        // Chatbot position
        if (widget_position === 'left'){
          $('.chatbot-trigger').addClass("chatbar-left").removeClass("chatbar-right");
          $('#overlayElement').addClass("chatbot-left").removeClass("chatbot-right");
        }else{
          $('.chatbot-trigger').removeClass("chatbar-left").addClass("chatbar-right");
          $('#overlayElement').removeClass("chatbot-left").addClass("chatbot-right");
        }
  
        // Chatbot position
        if (show_popup_notification === false){
          $('#overlayElement').hide();
        } else {
          $('#overlayElement').hide();
          setTimeout(function () {
              $('#overlayElement').show();
              // $("#toggleButton").css("display", "none");
          }, 2500);
        }
  
        var sec = delay_showing_popup_notification * 1000;
        setTimeout(function () {
          $('.container-chatbot').removeClass("d-none");
        }, sec);
  
        // Chatbot width control
        if (widget_height === 20){
          $('#overlayElement').addClass("chatbot-mini");
        }
        else if (widget_height === 30){
          $('#overlayElement').addClass("chatbot-xl");
        }
        else if (widget_height === 35){
          $('#overlayElement').addClass("chatbot-xxl");
        }

     }else{
        console.error('Error fetching model data:', response.status);
     }
     
    // Inject the CSS
    const style = document.createElement('style');
    style.innerHTML = `
    .hidden {
      display: none;
    }
    #chat-widget-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      flex-direction: column;
    }
    #chat-popup {
      height: 70vh;
      max-height: 70vh;
      transition: all 0.3s;
      overflow: hidden;
  
    }
  
  
  .pop-message {
      margin: 9px 0 0 -4px;
  }
  
    @media (max-width: 768px) {
      #chat-popup {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 75%;
        max-height: 75%;
        border-radius: 0;
  
      }
    }

    .loader {
    display: flex;
    font-size: 24px;
    font-weight: bold;
}
.loader .dot {
    animation: blink 1.5s infinite;
    margin: 0 2px;
}
.loader .dot:nth-child(2) {
    animation-delay: 0.2s;
}
.loader .dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes blink {
    0% { opacity: 0; }
    50% { opacity: 1; }
    100% { opacity: 0; }
}

  `;
    document.head.appendChild(style);
    // Create chat widget container
    const chatWidgetContainer = document.createElement('div');
    chatWidgetContainer.id = 'chat-widget-container';
    document.body.appendChild(chatWidgetContainer);
  
    // Inject the HTML
    chatWidgetContainer.innerHTML = `
      <div id="chat-bubble" class="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer text-3xl ">
          <img class="rounded-circle cursor-pointer launcher-icon" src='${ajaxDomain}${chatbot_launcher_icon}' alt="avatar" height="60" width="60">
      </div>
      <span class="pop-message position-absolute top-0 start-100 translate-middle badge border rounded-pill bg-primary"></span>
      <div id="chat-popup" class="hidden absolute bottom-20 right-0 w-96 bg-white rounded-md shadow-md flex flex-col transition-all text-sm chatbot-font-size chatbot-font-family">
        <div id="chat-header" class="top-bar-background flex justify-between items-center p-4 rounded-t-md">
          <h6 id="title" class="m-0 text-lg text-white">${display_name}</h6>
          <button id="close-popup" class="bg-transparent border-none text-white cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
  
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto chatbot-background chatbot-pattern  ">
            <div class="chat-history-body ">
                      <div class="d-flex overflow-hidden" >
                                  <div class="user-avatar flex-shrink-0 me-3">
                                    <div class="avatar avatar-sm">
                                      <img src="${ajaxDomain}${chatbot_image}" alt="Avatar"
                                           class="rounded-circle chatbot-image" />
                                    </div>
                                  </div>
                                  <div class="chat-message-wrapper flex-grow-1">
                                    <div class="chat-message-text chatbot-text theme-right chatbot-msg-background user-default-msg-color">
                                      <p class="mb-0" id="chatbot-initial-messages">
                                      ${initial_message}
                                      </p>
                                    </div>
                                  </div>
                                </div>
              </div>
        </div>
        <div id="chat-input-container" class="p-4 border-t border-gray-200">
          <div class="flex space-x-4 items-center">
            <input type="text" id="chat-input" class="flex-1 border border-gray-300 rounded-md px-4 py-2 outline-none w-3/4" placeholder="Type your message...">
            <button id="chat-submit" class="bg-gray-800 text-white rounded-md px-4 py-2 cursor-pointer ">Send</button>
          </div>
          <div class="flex text-center text-xs pt-4">
            <span class="flex-1" id="chat-footer-name">
            ${footer_name}
            </span>
          </div>
        </div>
      </div>
    `;
    // Add event listeners
    const chatInput = document.getElementById('chat-input');
    const chatSubmit = document.getElementById('chat-submit');
    const chatMessages = document.getElementById('chat-messages');
    const chatBubble = document.getElementById('chat-bubble');
    const chatPopup = document.getElementById('chat-popup');
    const closePopup = document.getElementById('close-popup');
    chatSubmit.addEventListener('click', function() {
      const message = chatInput.value.trim();
      if (!message) return;
      chatMessages.scrollTop = chatMessages.scrollHeight;
      chatInput.value = '';
      onUserRequest(message);
    });
  
    chatInput.addEventListener('keyup', function(event) {
      if (event.key === 'Enter') {
        chatSubmit.click();
      }
    });
  
    chatBubble.addEventListener('click', function() {
      togglePopup();
    });
  
    closePopup.addEventListener('click', function() {
      togglePopup();
    });
  
   function togglePopup() {
      const chatPopup = document.getElementById('chat-popup');
      chatPopup.classList.toggle('hidden');
      if (!chatPopup.classList.contains('hidden')) {
        document.getElementById('chat-input');
      }
    }
    function displayMessage(message, sender) {
        let answer = ` ${message}`;
        const chatMessages = document.getElementById('chat-messages');
        const replyElement = document.createElement('div');
        replyElement.className = 'flex mb-3';
        replyElement.innerHTML = `
         <div class="user-avatar flex-shrink-0 me-3">
                                  <div class="avatar avatar-sm">
                                    <img src="${ajaxDomain}${chatbot_image}" alt="Avatar"
                                         class="rounded-circle chatbot-image" />
                                  </div>
                                </div>
                                <div class="chat-message-wrapper flex-grow-1 max-w-[70%]">
                                  <div class="chat-message-text chatbot-text theme-right chatbot-msg-background user-default-msg-color ">
                                    <p class="mb-0" id="chatbot-initial-messages">
                                    ${answer}
                                    </p>
                                  </div>
                                  &nbsp;

                                </div>
        `;
        chatMessages.appendChild(replyElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatInput.focus();

    }
    async function onUserRequest(question) {
      // Handle user request here
      console.log('User request message:', question);
  
      // Display user message
      const messageElement = document.createElement('div');
      messageElement.className = 'flex justify-end mb-3';
      messageElement.innerHTML = `
        <div class="chat-message-text theme-right user-msg-background user-default-msg-color user-msg-color max-w-[70%]">
          ${question}
        </div>`;
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
      chatInput.value = '';
      let botAnimation = document.createElement("li");
    botAnimation.className = "chat-message";
    botAnimation.id = "bot-animation";
    botAnimation.innerHTML = `
        <div class="d-flex overflow-hidden">
            <div class="user-avatar flex-shrink-0 me-3">
                <div class="avatar avatar-sm">
                    <img src="${ajaxDomain}${chatbot_image}" alt="Avatar" class="rounded-circle" />
                </div>
            </div>
            <div class="chat-message-wrapper flex-grow-1">
                <div class="chat-message-text chatbot-msg-background">
                    <div class="loader">
                        <span class="dot">.</span>
                        <span class="dot">.</span>
                        <span class="dot">.</span>
                    </div>
                </div>
            </div>
        </div>`;
      chatMessages.appendChild(botAnimation);
      const apiUrl = `${ajaxDomain}/api/v2/chatbot/query/?chat_id=${botId}`;
      fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // Include CSRF token here
            },
            body: JSON.stringify({ query: question })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("API Response:", data);
            document.getElementById("bot-animation").remove();
            // Extract and display chatbot's response
            if (data.results) {
                displayMessage(data.results.response, "bot");
            } else {
                displayMessage("No response from chatbot.", "bot");
            }
        })
        .catch(error => {
            document.getElementById("bot-animation").remove();
            displayMessage("Error fetching response.", "bot");
        });
      
      

      // Reply to the user
//        $.ajax({
//         type: "POST",
//         url: ajaxDomain + "visitor_chat",
//         data: {
//             history: "history",
//             question: question,
//             chatdata_id: botId,
//             visitor_id: visitor_id,
//         },
//         success: function (data) {
//   //        $("#bot-animation").fadeOut(500);
//   //        const now = new Date(); // create a new Date object with the current date and time
//   //        const currentTime = now.toLocaleTimeString();
  
//           let answer = ` ${data}`;
//           const chatMessages = document.getElementById('chat-messages');
//           const replyElement = document.createElement('div');
//           replyElement.className = 'flex mb-3';
//           replyElement.innerHTML = `
//            <div class="user-avatar flex-shrink-0 me-3">
//                                     <div class="avatar avatar-sm">
//                                       <img src="${chatbot_image}" alt="Avatar"
//                                            class="rounded-circle chatbot-image" />
//                                     </div>
//                                   </div>
//                                   <div class="chat-message-wrapper flex-grow-1 max-w-[70%]">
//                                     <div class="chat-message-text chatbot-text theme-right chatbot-msg-background user-default-msg-color ">
//                                       <p class="mb-0" id="chatbot-initial-messages">
//                                       ${answer}
//                                       </p>
//                                     </div>
//                                     &nbsp;
  
//                                   </div>
//           `;
//           chatMessages.appendChild(replyElement);
//           chatMessages.scrollTop = chatMessages.scrollHeight;
//           chatInput.focus();
//         },
//       });
  
    }
  
    function reply(message) {
      const chatMessages = document.getElementById('chat-messages');
      const replyElement = document.createElement('div');
      replyElement.className = 'flex mb-3';
      replyElement.innerHTML = `
  //      <div class="bg-gray-200 text-black rounded-lg py-2 px-4 max-w-[70%]">
          ${message}
  //      </div>
      `;
      chatMessages.appendChild(replyElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  
  })();
  
  