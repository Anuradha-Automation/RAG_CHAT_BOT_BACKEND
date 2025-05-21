// chatbot-loader.js
function loadChatbot() {
  var botId = document.currentScript.getAttribute('data-bot-id');
  // Append the HTML to the body of the page
  var chatbotHTML = `
    <!-- Your provided HTML code -->
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <!-- CSS and external dependencies -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha256-pvPw+upLPUjgMXY0G+8O0xUf+/Im1MZjXxxgOcBQBXU=" crossorigin="anonymous" referrerpolicy="no-referrer">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <script src="https://code.jquery.com/jquery-3.6.3.min.js" integrity="sha256-pvPw+upLPUjgMXY0G+8O0xUf+/Im1MZjXxxgOcBQBXU=" crossorigin="anonymous"></script>
 
        <link rel="stylesheet" href="http://127.0.0.1:8000/static/assets/vendor/css/pages/assistant.css">
        <style>
          /* Customize the chatbox appearance here */
          /* Add your own styles or use the existing ones */
          #chat-circle {
              bottom: 20px;
              right: 20px;
              z-index: 9999;
              float: right;
              padding:10px;
          }
          .chat-box{
            bottom: 90px;
          }
          #chat-input{
            width:81%;
          }
          /* Add any additional custom styles here */
        </style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
      </head>
      <body>
        <!-- Your provided HTML content -->
        <div id="chat-container">
          <div id="chat-circle" class="btn btn-raised">
            <div id="chat-overlay"></div>
            <i class="bi bi-question-circle"></i><span style="padding-left:6px"><i class="fa fa-commenting fa-2x"></i></span>
          </div>
          <div class="chat-box">
            <div class="chat-box-header">
              ChatBot
              <span class="chat-box-toggle"><i class="fa fa-close "></i></span>
            </div>
            <div class="chat-box-body">
              <div class="chat-box-overlay"></div>
              <div class="chat-logs"></div>
            </div>
            <div class="chat-input">
              <form id="chat-form">
                <input type="text" id="chat-input" placeholder="Send a message..." />
                <button type="submit" class="chat-submit" id="chat-submit">
                  <i class="fa fa-send fa-2x"></i>
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Your provided JavaScript code -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        
      </body>
    </html>
  `;
  document.body.innerHTML += chatbotHTML;
  // Your JavaScript logic can continue here
}

// Call the loadChatbot function with the desired botId to start loading the chatbot
loadChatbot();
$(document).ready(function () {
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var scriptTag = document.querySelector('script[data-bot-id]'); // Capture the botId provided as a parameter
    var botId = scriptTag.getAttribute('data-bot-id');
    var ipAddress = null;

  // Your JavaScript logic goes here
  var INDEX = 0;

  // Handle form submission
  $("#chat-form").submit(function (e) {
    e.preventDefault();
    const msg = $("#chat-input").val().trim();
    if (msg === '') {
      return false;
    }
    generate_message(msg, 'self');
    // Replace 'YOUR_CHAT_ENDPOINT_URL' with the actual URL for your chat endpoint
    $.ajax({
      type: "POST",
      // url: "http://localhost:8000/chat",
      url: "http://127.0.0.1:8000/chat",
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: {
        history: "first chat",
        botId: botId, // Pass the botId as part of the request payload
        question: msg,
        ipAddress: ipAddress
      },
      success: function (res) {
        generate_message(res, 'user');
      }
    });
  });

  function generate_message(msg, type) {
    INDEX++;
    var str = "";
    str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + "\">";
    str += "<span class=\"msg-avatar\">";
    if (type == 'self') {
      str += "<img src=\"http://127.0.0.1:8000/static/assets/img/avatars/1.png\" alt=\"twbs\" width=\"32\" height=\"32\" class=\"rounded-circle flex-shrink-0\">";
    } else {
      str += "<img src=\"http://127.0.0.1:8000/static/assets/img/avatars/bot.jfif\" alt=\"twbs\" width=\"32\" height=\"32\" class=\"rounded-circle flex-shrink-0\">";
    }
    str += "</span>";
    str += "<div class=\"cm-msg-text\" style=\"font-size:14px\">";
    str += msg;
    str += "</div>";
    str += "</div>";
    $(".chat-logs").append(str);
    $("#cm-msg-" + INDEX).hide().fadeIn(300);
    if (type == 'self') {
      $("#chat-input").val('');
    }
    $(".chat-logs").stop().animate({
      scrollTop: $(".chat-logs")[0].scrollHeight
    }, 1000);
  }

  function track_info() {
    //     AJAX CALL to track user info
    var url = window.location.href;
    // Fetch user's IP address
    var scriptTag = document.querySelector('script[data-bot-id]');
    var botId = scriptTag.getAttribute('data-bot-id');
    $.getJSON("https://api.ipify.org?format=json", function (data) {
      ipAddress = data.ip;
      // Fetch location information using IP address
      $.getJSON("http://ipapi.co/" + ipAddress+"/json", function (locationData) {
        var location = locationData.city + ", " + locationData.regionName + ", " + locationData.country;

        // Rest of your code
        $.ajax({
          type: "POST",
          url: "http://127.0.0.1:8000/track/",
          // url: "http://localhost:8000/track/",
          headers: {
            'X-CSRFToken': csrftoken
          },
          data: {
            url: url,
            location: location,
            ipAddress: ipAddress,
            botId: botId,
          },
          success: function (res) {
            console.log("success", res);
          },
          error: function (res) {
            console.log("error", res);
          }
        });
      });
    });
  }


  function error() {
    console.log("Geolocation error occurred");
  }

  $("#chat-circle").click(function () {
    // $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
    track_info();
  });

  $(".chat-box-toggle").click(function () {
    // $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  });


});