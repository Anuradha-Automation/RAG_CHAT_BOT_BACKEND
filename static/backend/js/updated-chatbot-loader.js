// chatbot-loader.js
var botIdScript = document.currentScript;
var visitor_id = null
function load_visitor_data() {
  return new Promise(async function(resolve, reject) {
    try {
      var bot_Id = botIdScript.getAttribute('chatbot-id');
      var ipData = await $.getJSON("https://api.ipify.org?format=json");
      var ipAddress = ipData.ip;

      var locationData = await $.getJSON("https://ipapi.co/" + ipAddress + "/json");
      var location = locationData.city + ", " + locationData.region + ", " + locationData.country;

      var response = await $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/track",
        data: {
          url: window.location.href,
          location: location,
          ipAddress: ipAddress,
          botId: bot_Id,
        },
      });

      console.log("success:- ", response);
      visitor_id = response;

      resolve(visitor_id);
    } catch (error) {
      console.error("error", error);
      reject(error);
    }
  });
}

// Usage example:
load_visitor_data()
  .then(function(visitor_id) {
    // Do something with the visitor_id
    console.log("Visitor ID:", visitor_id);
  })
  .catch(function(error) {
    // Handle errors
    console.error("Error:", error);
  });



function loadChatbot() {
  const currentFormattedTime = getCurrentFormattedTime();
  var botId = document.currentScript;
  bot_data = botId.getAttribute('chatbot-id')
  // Append the HTML and Style to the body of the page
  var chatbotHTML = `
            <div class="container-chatbot widget d-none chatbar-left chatbot-trigger" style="display: none;"  id="toggleButton">
            <span class="position-absolute top-0 start-100 translate-middle badge border rounded-pill bg-primary">1</span>
          </div>

  <div class="chatbot-left widget" id="overlayElement" style="display: none;">
      <div class="app-chat card overflow-hidden" >
          <div class="row g-0">
              <!-- Chat History -->
          <div class="col app-chat-history chatbot-width chatbot-height chatbot-position chatbot-font-family chatbot-font-size mb-2">
              <div class="chat-history-wrapper chat-widget top-bar-text" style="background: #f8f8f9; overflow: hidden;">
              <div class="chat-history-header border-bottom theme-header chatbot-theme top-bar-background">
                  <div class="d-flex justify-content-between align-items-center">
                      <div class="d-flex overflow-hidden align-items-center">



                          <div class="chat-contact-info flex-grow-1 ms-3">
                              <h6 class="m-0 top-bar-text" id="title" >Testing</h6>
                              <span class="user-status text-body invisible d-none">NextJS developer</span>
                          </div>
                      </div>
                  <div class="d-flex align-items-center">
                      <div class="dropdown">
                          <button class="btn btn-icon btn-text-secondary rounded-pill" id="chat-header-actions">
                                 <span class="close text-dark">x</span>
                          </button>
                      </div>
                  </div>
                  </div>
              </div>
              <div class="chat-history-body widget-chat-height chatbot-pattern chatbot-background-color">
                  <ul id='chat-history-ul' class="list-unstyled chat-history">
                  <li class="chat-message">
                      <div class="d-flex overflow-hidden">
                      <div class="user-avatar flex-shrink-0 me-3">
                          <div class="avatar avatar-sm">
                          <img src="http://127.0.0.1:8000/Static/assets1/img/avatars/1.png" alt="Avatar"
                              class="rounded-circle chatbot-image" />
                          </div>
                      </div>
                      <div class="chat-message-wrapper flex-grow-1">
                          <div class="chat-message-text widget-max-width chatbot-msg-background">
                          <p class="mb-0 chatbot-text-color" id="initial-message">Hi! What can I help with you ? 😎</p>
                          </div>

                          <div class="text-muted">
                          <small>${currentFormattedTime}</small>
                          </div>
                      </div>
                      </div>
                  </li>

                  </ul>
              </div>
              <!-- Chat message form -->
              <div class="chat-history-footer">
                  <form class="form-send-message d-flex justify-content-between align-items-center py-2" autocomplete="off">
                      <input type="hidden" id="chatdata_id" value="${bot_data}">
                      <input class="form-control message-input me-3 white-bg" id="message" name="question" style="border: 1px solid #d8d8dd;"
                      placeholder="Type your message here"/>
                  <div class="message-actions d-flex align-items-center">
                      <button type="button" class="btn btn-primary d-flex send-msg-btn" id="send">
                      <span class="align-middle">Send</span>
                      </button>
                  </div>
                  </form>
              </div>
              <ul class="nav nav-tabs nav-tabs-widget pb-3 mx-2 d-flex flex-nowrap sticky-suggestion" role="tablist">
                  <li class="nav-item d-none" role="presentation">
                  <div class="ms-3 badge bg-label-success rounded-pill py-3">How can i Help you ?</div>
                  </li>
                  <li class="nav-item d-none" role="presentation">
                  <div class="ms-3 badge bg-label-success rounded-pill py-3">What is your name?
                      </div>
                  </li>
                  <li class="nav-item d-none" role="presentation">
                  <div class="ms-3 badge bg-label-success rounded-pill py-3">What is your name?
                      </div>
                  </li>
                  <li class="nav-item d-none" role="presentation">
                  <div class="ms-3 badge bg-label-success rounded-pill py-3">Can you tell me a joke?</div>
                  </li>
              <span class="tab-slider"></span>
              </ul>

              </div>
          </div>
              <div class="d-flex justify-content-between sticky-powerdby">
                  <small class="m-3" id="footer_name">Powered by My AI Solutions</small>
              </div>

          <div class="app-overlay"></div>
          </div>
      </div>
  </div>`;
  document.body.innerHTML += chatbotHTML;
  document.body.setAttribute('data-assets-path','/Static/assets1/');

  // Required
  styleUrls = [
    "http://127.0.0.1:8000/Static/assets1/css/base.css",
    "http://127.0.0.1:8000/Static/assets1/css/chatbot.css",
    "http://127.0.0.1:8000/Static/assets1/css/demo.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/css/pages/assistant.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/perfect-scrollbar/perfect-scrollbar.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/fonts/materialdesignicons.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/fonts/fontawesome.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/node-waves/node-waves.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/typeahead-js/typeahead.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/bootstrap-maxlength/bootstrap-maxlength.css",
    "http://127.0.0.1:8000/Static/assets1/vendor/css/pages/app-chat.css",
    "http://127.0.0.1:8000/Static/assets1/css/chatbot-config.css",
  ]

  scriptUrls = [
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/jquery/jquery.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/popper/popper.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/js/bootstrap.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/perfect-scrollbar/perfect-scrollbar.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/node-waves/node-waves.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/hammer/hammer.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/i18n/i18n.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/typeahead-js/typeahead.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/js/menu.js",
    "http://127.0.0.1:8000/Static/assets1/vendor/libs/bootstrap-maxlength/bootstrap-maxlength.js",
    "http://127.0.0.1:8000/Static/assets1/js/main.js",
    "http://127.0.0.1:8000/Static/assets1/js/app-chat.js",
  ]
  // Scripts append dynamically
  for (const url of scriptUrls) {
    const scriptElement = document.createElement('script');
    scriptElement.src = url;
    document.body.appendChild(scriptElement);
  }

  const scriptElement = document.createElement('script');
  scriptElement.src = "http://127.0.0.1:8000/Static/assets1/js/app-chat.js";
  document.body.appendChild(scriptElement);

  // CSS append dynamically
  for (const url of styleUrls) {
    const linkElement = document.createElement('link');
    linkElement.rel = 'stylesheet';
    linkElement.type = 'text/css';
    linkElement.href = url;
    document.head.appendChild(linkElement);
  }
}


 // Data and time format
 function getCurrentFormattedTime() {
  const options = {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "numeric",
    minute: "numeric",
    hour12: true
  };
  const formattedTime = new Date().toLocaleString("en-US", options);
  return formattedTime;
}

//  Auto page scroller
function scrollToBottom() {
  var chatContainer = $("#chat-history-ul");
  chatContainer.scrollTop(chatContainer[0].scrollHeight);
}

const linkElement3 = document.createElement('link');
linkElement3.rel = 'stylesheet';
linkElement3.type = 'text/css';
linkElement3.href = 'http://127.0.0.1:8000/Static/assets1/vendor/css/rtl/core.css';
linkElement3.className = 'template-customizer-core-css';

const linkElement2 = document.createElement('link');
linkElement2.rel = 'stylesheet';
linkElement2.type = 'text/css';
linkElement2.href = 'http://127.0.0.1:8000/Static/assets1/vendor/css/rtl/theme-default.css';
linkElement2.className = 'template-customizer-theme-css';


document.head.appendChild(linkElement3);
document.head.appendChild(linkElement2);

loadChatbot();

$(document).ready(function () {


  var csrftoken = null;
  // Get Chatbot appearance details initial request
  $.ajax({
    url: 'http://127.0.0.1:8000/api/chatbot-appearances/' + bot_data,
    dataType: 'json',
    success: function (data) {
      console.log(data, "---------appearance data");
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

      localStorage.setItem("img_url", chatbot_image);

      if (widget_width === null || widget_width === undefined || widget_width === '') {
        widget_width = '25%'
      } else {
        widget_width = widget_width;
      }

      styleData = `
              /* Chatbot Theme color */
                .widget .chatbot-theme{
                background-color:${chatbot_theme} !important;
              }

              /* Chatbot pattern */
                .widget .chatbot-pattern {
                  background-image: url(${ chatbot_background_pattern }) !important;
              }

              /* Chatbot messages background */
                .widget .chatbot-msg-background {
                background-color: ${bot_message_background} !important;
              }

              /* Chatbot messages text color */
                .widget .chatbot-text-color {
                color: ${bot_message_color} !important;
              }

              /* User messages bg color */
                .widget .user-msg-background {
                background-color: ${user_message_background} !important;
              }

              /* User messages text color */
                .widget .user-msg-color {
                color: ${user_message_color} !important;
              }

              /* Top bar bg color */
                  .widget .top-bar-background {
                  background-color: ${top_bar_background} !important;
                }

              /* Top bar text color */
                .widget .top-bar-text{
                  color: ${top_bar_textcolor} !important;
                }

              /* Chatbot font style */
              .widget .chatbot-font-family {
                font-family: ${font_family} !important;
              }

              /* Chatbot font style size */
                .widget .chatbot-font-size {
                  font-size: ${font_size}px !important;
                }
              /*  Chatbot background color */
                .widget .chatbot-background-color {
                  background-color: ${chatbot_background_color} !important;

                .chatbot-right{
                  width:${widget_width}% !important;
                }
                .chatbot-left{
                  width:${widget_width}% !important;
                }
                  `
      const styleElement = document.createElement("style");

      // Set the content of the <style> element to the styleData
      styleElement.innerHTML = styleData;

      // Append the <style> element to the <head> section of the document
      document.head.appendChild(styleElement);
      //  Chatbot name
      $('#title').html(display_name);
      $('#footer_name').html(footer_name);

      //  Chatbot heading
      $('#chat-heading').html(chatbot_title);

      // initial message
      $('#initial-message').html(initial_message);

      // Chatbot profile image change
      if (chatbot_image != null){
        $('.chatbot-image').attr('src',chatbot_image);
      }else{
        var chabot_image_live = 'http://127.0.0.1:8000/Static/assets1/img/avatars/1.png'
        $('.chatbot-image').attr('src',chabot_image_live);
      }
      // Chatbot chatbot_launcher_icon change
      if (chatbot_launcher_icon != null){
        $('.chatbar-left').css('background-image', 'url(' + chatbot_launcher_icon + ')');
      }

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


    },
    error: function (error) {
      console.error('Error fetching model data:', error);
    }
  });

  function historyClick(e, history) {
    $("#chat-title").text(history);
    var $listItems = $("li").filter(".chat-contact-list-item");
    $listItems.each(function () {
      // Do something with the current li element (this)
      $(this).removeClass("active");
    });

    //$('#chat-title').text(history)
    // get_chat(history);

    $(e).closest("li").addClass("active");
  }

  function get_chat(history) {
    //$('#chat-title').text(history)
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/get_chat",
      data: { category: "librarian", history: history },
      success: function (data) {
        chat_data = ``;
        for (i = 1; i <= data.length; i++) {
          chat_data += `
          <li class="chat-message chat-message-right">
              <div class="d-flex overflow-hidden">
              <div class="chat-message-wrapper flex-grow-1">
                  <div class="chat-message-text widget-max-width chatbot-theme user-msg-background user-default-msg-color user-msg-color ">
                  <p class="mb-0 user-msg-color">${data[i - 1][0]}</p>
                  </div>
                  <div class="text-end text-muted">
                  <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" viewBox="0 0 24 24">
                            <path d="M0.41,13.41L6,19L7.41,17.58L1.83,12M22.24,5.58L11.66,16.17L7.5,12L6.07,13.41L11.66,19L23.66,7M18,7L16.59,5.58L10.24,11.93L11.66,13.34L18,7Z" style="fill: #70e043;" />
                        </svg>
                  <small>${data[i - 1][1]}</small>
                  </div>
              </div>
              <div class="user-avatar flex-shrink-0 ms-3">
                  <div class="avatar avatar-sm">
                  <img src="http://127.0.0.1:8000/Static/assets1/img/avatars/1.png" alt="Avatar" class="rounded-circle" />
                  </div>
              </div>
              </div>
          </li>
          <li class="chat-message">
              <div class="d-flex overflow-hidden">
              <div class="user-avatar flex-shrink-0 me-3">
                  <div class="avatar avatar-sm">
                  <img src="http://127.0.0.1:8000/Static/assets1/img/avatars/1.png" alt="Avatar" class="rounded-circle" />
                  </div>
              </div>
              <div class="chat-message-wrapper flex-grow-1">
                  <div class="chat-message-text widget-max-width chatbot-msg-background">
                  <p class="mb-0 chatbot-text-color" >${data[i - 1][2]}</p>
                  </div>
                  <div class="text-muted">
                  <small>${data[i - 1][3]}</small>
                  </div>
              </div>
              </div>
          </li>
              `;
        }
        // 661 line style="color:#000000"

        $("#chat-history-ul").html(chat_data);
        //$('#chat-history-ul').scrollTop($("#chat-history-ul")[0].scrollHeight);
      },
    });
  }

  function get_history() {
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/get_history",
      //data: {'category':'librarian'},
      success: function (data) {
        console.log("got history");
        var history_data = "";
        for (let i = 1; i <= data.length; i++) {
          if (i == 1) {
            history_data += `
              <li class="chat-contact-list-item active" onclick="historyClick(this, '${data[i - 1]}')">
                  <a class="d-flex align-items-center">
                  <div class="chat-contact-info flex-grow-1 ms-3">
                      <h6 class="chat-contact-name text-truncate m-0">${data[i - 1]}</h6>
                  </div>
                  <small class="text-muted mb-auto">5 Minutes</small>
                  </a>
              </li>
              `;
          } else {
            history_data += `
              <li class="chat-contact-list-item" onclick="historyClick(this, '${data[i - 1]}')">
              <a class="d-flex align-items-center">
                  <div class="chat-contact-info flex-grow-1 ms-3">
                  <h6 class="chat-contact-name text-truncate m-0">${data[i - 1]}</h6>
                  </div>
                  <small class="text-muted mb-auto">5 Minutes</small>
              </a>
              </li>
              `;
          }
        }
        $("#chat-history-div").html(history_data);

        // chat initializer
        if (data.length > 0) {
          var init_history = data[0];
          $("#chat-title").text(init_history);
          console.log("inithistory", init_history);
          // get_chat(init_history);
        }
      },
    });
  }
  get_history();

  $("#clear_history").click(() => {
    const currentFormattedTime = getCurrentFormattedTime();
    var msg_bot = `<li class="chat-message">
                  <div class="d-flex overflow-hidden">
                  <div class="user-avatar flex-shrink-0 me-3">
                      <div class="avatar avatar-sm">
                      <img src="http://127.0.0.1:8000/media/default_images/chatbot_image.png" alt="Avatar" class="rounded-circle chatbot-image">
                      </div>
                  </div>
                  <div class="chat-message-wrapper flex-grow-1">
                      <div class="chat-message-text widget-max-width chatbot-msg-background">
                      <p class="mb-0 chatbot-text-color" id="initial-message">Hi! What can I help with you?</p>
                      </div>
                      <div class="text-muted">
                      <small>${currentFormattedTime}</small>
                      </div>
                  </div>
                  </div>
              </li>`
    $("#chat-history-ul").html(msg_bot)
  });

  $("#send").click(() => {
    var img_url = localStorage.getItem("img_url");
    const currentFormattedTime = getCurrentFormattedTime();
    var bot_animation = `<li class="chat-message" id="bot-animation">
            <div class="d-flex overflow-hidden">
                <div class="user-avatar flex-shrink-0 me-3">
                <div class="avatar avatar-sm">
                    <img src="${img_url}" alt="Avatar" class="rounded-circle" />
                </div>
                </div>
                <div class="chat-message-wrapper flex-grow-1">
                <div class="chat-message-text widget-max-width chatbot-msg-background">
                    <div class="loader">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                    </div>
                </div>
                <div class="text-muted">
                    <small>${currentFormattedTime}</small>
                </div>
                </div>
            </div>
            </li>`;
    var question = $("#message").val();
    $("#message").val("");
    var chatdata_id = $("#chatdata_id").val();

    var history = $("#chat-title").text();
    console.log(history);
    const now = new Date(); // create a new Date object with the current date and time
    const options = { hour12: false, hourCycle: "h23", second: undefined };
    const currentTime = now.toLocaleTimeString([], options);
    var message = `
        <li class="chat-message chat-message-right">
        <div class="d-flex overflow-hidden">
            <div class="chat-message-wrapper flex-grow-1">
            <div class="chat-message-text widget-max-width chatbot-theme user-msg-background user-default-msg-color user-msg-color ">
                <p class="mb-0 user-msg-color">${question}</p>
            </div>
            <div class="text-end text-muted">
                <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" viewBox="0 0 24 24">
                            <path d="M0.41,13.41L6,19L7.41,17.58L1.83,12M22.24,5.58L11.66,16.17L7.5,12L6.07,13.41L11.66,19L23.66,7M18,7L16.59,5.58L10.24,11.93L11.66,13.34L18,7Z" style="fill: #70e043;" />
                        </svg>
                <small>${currentFormattedTime}</small>
            </div>
            </div>

        </div>
        </li>
    `;
    $("#chat-history-ul").append(message);
    $("#chat-history-ul").append(bot_animation);
    scrollToBottom();

    console.log(visitor_id, "------------- Visitor")

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/visitor_chat",
      data: { history: history, question: question, chatdata_id: chatdata_id, visitor_id: visitor_id },
      success: function (data) {
        $("#bot-animation").fadeOut(500);
        const now = new Date(); // create a new Date object with the current date and time
        const currentTime = now.toLocaleTimeString();

        let answer = `
            <li class="chat-message">
            <div class="d-flex overflow-hidden">
                <div class="user-avatar flex-shrink-0 me-3">
                <div class="avatar avatar-sm">
                    <img src=${img_url} alt="Avatar" class="rounded-circle" />
                </div>
                </div>
                <div class="chat-message-wrapper flex-grow-1">
                <div class="chat-message-text widget-max-width chatbot-msg-background">
                    <p class="mb-0 chatbot-text-color" >${data}</p>
                </div>
                <div class="text-muted">
                    <small>${currentFormattedTime}</small>
                </div>
                </div>
            </div>
            </li>
        `;
        setTimeout(function () {
          $("#chat-history-ul").append(answer);
          $("#bot-animation").remove();
          scrollToBottom();
        }, 500);
      },
    });
  });

  // add a chat
  $("#create-history").click(() => {
    var history = $("#chatTitle").val();
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/create_history",
      data: { history: history },
      success: function (data) {
        var history_element = `
            <li class="chat-contact-list-item active" onclick="historyClick('${history}')">
            <a class="d-flex align-items-center">
                <div class="chat-contact-info flex-grow-1 ms-3">
                <h6 class="chat-contact-name text-truncate m-0">${history}</h6>
                </div>
                <small class="text-muted mb-auto">5 Minutes</small>
            </a>
            </li>
        `;
        $("#chat-history-div").prepend(history_element);
        $("#chat-title").text(history);
        // get_chat(history);
        get_history();
      },
    });
  });

  $("#delete-history").click(() => {
    var history = $("#chat-title").text();
    console.log("delete==============", history);
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/delete_history",
      data: { history: history },
      success: function (data) {
        // get_chat(history);
        get_history();
      },
    });
  });

//   Chatbot hide and show toggle
//  $(document).on("click", "#toggleButton", function() {
//    // Get the overlay element using jQuery
//    var overlayElement = $("#overlayElement");
//
//    // Toggle the display of the overlayElement
//    if (overlayElement.css("display") === "none") {
//      overlayElement.css("display", "block");
//      $("#toggleButton").css("display", "none");
//    } else {
//      overlayElement.css("display", "none");
//    }
//  });

//   Chatbot hide and show toggle

$(document).ready(function () {
  // Check if the chatbot state is set in session storage
  var chatbotState = sessionStorage.getItem("chatbotState");

  // Initially check the screen width and hide the toggle button if in mobile view
  checkScreenWidth();

  // Handle toggle button click
  $(document).on("click", "#toggleButton", function () {
    // Get the overlay element using jQuery
    var overlayElement = $("#overlayElement");

    // Toggle the display of the overlayElement
    if (overlayElement.css("display") === "none") {
      overlayElement.css("display", "block");

      // Hide the toggle button in mobile view on click
      if (isMobileView()) {
        $("#toggleButton").css("display", "none");
      }

      // Set the chatbot state to opened
      sessionStorage.setItem("chatbotState", "opened");
    } else {
      overlayElement.css("display", "none");

      // Show the toggle button in mobile view on click
      if (isMobileView()) {
        $("#toggleButton").css("display", "block");
      }

      // Set the chatbot state to closed
      sessionStorage.setItem("chatbotState", "closed");
    }
  });

  // Handle window resize to show/hide the toggle button
  $(window).resize(function () {
    checkScreenWidth();
  });

  // Function to check if in mobile view
  function isMobileView() {
    var screenWidth = $(window).width();
    return screenWidth < 768;
  }
  // Hide the toggle button in mobile view on click
  if (isMobileView()) {
    $("#toggleButton").css("display", "none");
  }

  // Function to check the screen width and hide the toggle button in mobile view
  function checkScreenWidth() {
    var screenWidth = $(window).width();

    // Show/hide the toggle button based on the screen width
    if (isMobileView()) {
      $("#toggleButton").css("display", "block");
    } else {
      $("#toggleButton").css("display", "block");
    }

    // Open the chatbot if it was previously opened and not in mobile view
    if (chatbotState === "opened" && !isMobileView()) {
      $("#overlayElement").css("display", "block");
    }
  }
});

/////////////////////////////////////////////////////////////////////////////////////////////////////////



  // Chatbot hide and show toggle
  $(document).on("click", "#chat-header-actions", function() {
    // Get the overlay element using jQuery
    var overlayElement = $("#overlayElement");

    // Toggle the display of the overlayElement
    if (overlayElement.css("display") === "none") {
      overlayElement.css("display", "block");
    } else {
      overlayElement.css("display", "none");
      $("#toggleButton").css("display", "block");
    }
  });

  // While chatbot feed input its stop form submit
  $("form").on("submit", function (event) {
    event.preventDefault();
  });

  // Enter to submit input value
  $("#message").on("keyup", function (event) {
    if (event.keyCode === 13) {
      const inputValue = $(this).val().trim();
      if (inputValue.match(/[a-zA-Z]/)) {
        $("#send").trigger("click");
        $(this).val("");
      }
    }
  });

  $(".chatbot-trigger").show();
});


