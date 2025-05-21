$(document).ready(function(){
    // $("#chatbot-form").submit(function(event){
    //     event.preventDefault();  // Default form submit rokna hai
    //     var formData = new FormData(this);
    //     $.ajax({
    //         url: $("#chatbot-form").attr("action"),
    //         type: "POST",
    //         data: formData,
    //         processData: false,
    //         contentType: false,
    //         success: function(response){
    //           console.log(response);
    //             // if(response.success) {
    //             //     $("#responseMessage").text(response.message).css("color", "green");
    //             // } else {
    //             //     $("#responseMessage").text(response.message).css("color", "red");
    //             // }
    //         },
    //         error: function(){
    //             $("#responseMessage").text("Something went wrong!").css("color", "red");
    //         }
    //     });
    // });
});
  $(document).ready(function () {

    // all inputs will work onload
        $(window).on('load', function() {
        $("#chatbot-mode").trigger('input');
        $('input[type="color"]').not('#chatbot-theme-input').trigger('input');
        $('#chatbot-font-style').trigger('input');
        $("#popup-notification").trigger('input');
        $('#chatbot-font-size').trigger('input');
    });

    // Input color inputs
    $(document).on('input', 'input[type="color"]', function () {
      var color_val = $(this).val();
      var connecter = $(this).attr('connecter');
      var input_ele = '#' + connecter
      $(input_ele).val(color_val);
    });

    // Chatbot name
    $(document).on('input', '#display-name', function () {
      var display_raw = $(this).val();
      var display_data = display_raw.trim()
      $("#chat-display-name").html(display_data);
    });

    // Chatbot Footer
    $(document).on('input', '#footer_name', function () {
      var footer_raw = $(this).val();
      var footer_data = footer_raw.trim()
      $("#chat-footer-name").html(footer_data);
    });

    // Chatbot initial messages
    $(document).on('input', '#initial-messages', function () {
      var initial_raw = $(this).val();
      var arrayOfLines = $(this).val().split('\n');

      if ((arrayOfLines.length == 1 ) && (initial_raw.includes("\n") !== -1)){
        var display = initial_raw.trim()
        $("#chatbot-initial-messages").html(display);
      }
    });



    //  Chatbot mode
    $(document).on('input', '#chatbot-mode', function () {
      if (this.checked) {
        $('.chat-history-wrapper').addClass('darkmode')
      } else {
        $('.chat-history-wrapper').removeClass('darkmode')
      }
    });

    //  Chatbot profile input
    $('#chatbot-image').on('input', function (e) {
      // Get the selected file
      var file = e.target.files[0];

      // Create a new FileReader
      var reader = new FileReader();

      // Define the onload event handler
      reader.onload = function (event) {
        // Retrieve the base64 image string
        var base64Image = event.target.result;
        $(".chatbot-image").attr("src", base64Image);
        $(".chatbot-icon").attr("src", base64Image);
      };

      // Read the file as a data URL (base64)
      reader.readAsDataURL(file);
    });

    //  Clicked image src attribute input
    $(document).on('click', '.drag-item', function () {
      var img_attr = $(this).attr("src");
      $('.chatprofile-selected').remove()
      $(this).parent().append(`<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatprofile-selected"></span>`);
      $(".chatbot-image").attr("src", img_attr);
      $(".chatbot-icon").attr("src", img_attr);
      $("#chatbot-image-url").val(img_attr);
    });

    // reset default chatbot image
    $(document).on('click', '#chatbot-image-remove', function () {
      $('.chatprofile-selected').remove()
      var img_attr = "{% static 'backend/img/avatars/1.png' %}"
      $('#default-profile').append(`<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatprofile-selected"></span>`);
      $(".chatbot-image").attr("src", img_attr);
      $(".chatbot-icon").attr("src", img_attr);
      $(".chatbot-launcher-icon").attr("src", img_attr);
      $("#chatbot-image-url").val(img_attr);
    });

    // Chatbot background inputr
    $(document).on('input', '#chatbot-bg-color-input', function () {
      var cl_value = $(this).val();
      $(".chatbot-background").css('background-color', cl_value);
    });

    // Top and right side theme inputr
    $(document).on('input', '#chatbot-theme-input', function () {
      var cl_value = $(this).val();
      $("#chat-header").attr('style', `background: ` + cl_value + ` !important`);
      $("#send-button").attr('style', `background: ` + cl_value + ` !important`);
      $("#chat-display-name").css('color', 'white');
    });

    // Top side only background input
    $(document).on('input', '#top-bar-background-color-input', function () {
      var cl_value = $(this).val();
      $(".theme-header").attr('style', `background: ` + cl_value + ` !important`)
    });
    // Top side only text input
    $(document).on('input', '#top-bar-text-color-input', function () {
      var cl_value = $(this).val();
      $(".theme-header").css('color', cl_value)
      $("#chat-display-name").css('color', cl_value)
    });


    // Chatbot Message background color
    $(document).on('input', '#chatbot-msg-background-color-input', function () {
      var cl_value = $(this).val();
      $(".theme-right").css('background', cl_value)
    });

    // Chatbot Message text color
    $(document).on('input', '#chatbot-msg-text-color-input', function () {
      var cl_value = $(this).val();
      $("#chatbot-initial-messages").attr('style', `color: ` + cl_value + ` !important`);
    });


    // User's background color only input
    $(document).on('input', '#user-msg-background-color-input', function () {
      var cl_value = $(this).val();
      $(".user-msg-background").attr('style', `background-color: ` + cl_value + ` !important`);
    });

    // User's text color only input
    $(document).on('input', '#user-msg-text-color-input', function () {
      var cl_value = $(this).val();
      $(".user-msg-color").attr('style', `color: ` + cl_value + ` !important`);
    });

    // Chatbot bg pattern
    $('#chatbot-bg-pattern').on('input', function (e) {
      var file = e.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        var base64Image = event.target.result;
        $(".chatbot-background").css({
        "background-image": 'url('+ base64Image + ')',
        // "background-size": "contain",
    })
      };
      reader.readAsDataURL(file);
    });

    // Chatbot click each image to input bg pattern
    $(document).on('click', '.chatbot-pattern-img', function () {
      $('.chatpattern-selected').remove()
      $(this).parent().append(`<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatpattern-selected"></span>`);
      var img_attr = $(this).attr("src");
      var img_data = $(this).attr("src_data");
      $("#chatbot-bg-pattern-url").val(img_data);
      $("#chatbot-bg-pattern").val("");
      $(".chatbot-background").css({
        'background-image': 'url(' + img_attr + ')'
      });
      $(".chatbot-pattern").css({
        'background-image': 'url(' + img_attr + ')'
      });
    });

    $(document).on('click', '#chatbot-bg-pattern-remove', function () {
      $('.chatpattern-selected').remove()
      $(".chatbot-pattern").css("background-image", "none");
      $(".chatbot-background").css("background-image","none");
      $(".chatbot-background").css("background-color","#e6e6e6");
      $("#chatbot-bg-pattern-url").val('empty');
    });

    // Popup notification disable and enable
    $(document).on('input', '#popup-notification', function () {
      if (this.checked) {
       $("#popup-notification-delay").removeAttr('disabled');
      } else {
        $("#popup-notification-delay").attr('disabled', true);

      }
    });

    // Initial messages
    $('#initial-messages').keydown(function (event) {
          if (event.keyCode === 13) {
            createNewElement();
          }
        });

    function createNewElement() {
      var arrayOfLines = $('#initial-messages').val().split('\n');
      var last_item = arrayOfLines[arrayOfLines.length - 1]
      if ((arrayOfLines.length >= 2) && (last_item.length != 0)){
      // Create a new paragraph element
      var newElement =` <li class="chat-message">
                        <div class="d-flex overflow-hidden">
                          <div class="user-avatar flex-shrink-0 me-3">
                            <div class="avatar avatar-sm">
                              <img src="{% if cfg.chatbot_image %}{{ cfg.chatbot_image.url }}{% else %}{% static 'backend/image/avatars/1.png' %}{% endif %}" alt="Avatar" class="rounded-circle chatbot-image">
                            </div>
                          </div>
                          <div class="chat-message-wrapper flex-grow-1">
                            <div class="chat-message-text chatbot-text">
                              <p class="mb-0" id="chatbot-initial-messages">`+last_item+`</p>
                            </div>
                          </div>
                        </div>
                      </li>`

      // Append the new element to the container
      $(newElement).insertBefore('.chat-message.chat-message-right');
    }
    };

    //  Suggested messages
    $('#suggested-messages').keydown(function (event) {
          if (event.keyCode === 13) {
            NewElement();
          }
        });

    function NewElement() {
          var arrayOfLines = $('#suggested-messages').val().split('\n');
          var last_item = arrayOfLines[arrayOfLines.length - 1]
          if ((arrayOfLines.length >= 0) && (last_item.length != 0)){
          // Create a new paragraph element
          var newElement =`<li class="nav-item" role="presentation">
                          <div class="ms-3 badge bg-label-success rounded-pill py-3">`+last_item+`</div>
                        </li>`

          // Append the new element to the container
          $(".sticky-suggestion").append(newElement);
        }
        };

    //  Chatbot font input
    $(document).on('input', '#chatbot-font-style', function () {
      var font_value = $(this).val();
      $('.chatbot-font-family').css('font-family', font_value);
    });
    $(document).on('input', '#chatbot-font-size', function () {
      var font_value = $(this).val();
      $('.chatbot-font-size').attr('style', `font-size: ` + font_value +`px !important`);
    });
    //  Chatbot theme clone for both top bar and user message background
    $(document).on('input', '#chatbot-theme-input', function () {
      var color_value = $(this).val();
      $('#top-bar-background-color-input').val(color_value);
      $('#top-bar-background-color').val(color_value);
      //$('#user-msg-background-color-input').val(color_value);
      //$('#user-msg-background-color').val(color_value);
    });

    $(document).on('click', '#theme-reset', function () {
      var top_color = '#8d54a2'
      var msg_color = '#000001'
      var top_bar_text = '#000001'
      var chatbot_bg_color = "#e6e6e6"

      var chatbot_msg_bg_color = "#ffffff"
      var chatbot_msg_text = '#9797a4'

      var user_msg_bg_color = "#ffffff"
      var user_msg_text = '#9797a4'


      $('#send-button').attr('style', `background-color: ` + top_color + ` !important`);
      //$('#user-msg-background-new').attr('style', `background-color: ` + top_color + ` !important`);

      // Theme color
      $('#chatbot-theme-input').val(top_color);
      $('#theme-color').val(top_color);
      $('input[type="color"]').not('#chatbot-theme-input').trigger('input');

      // Top bar background color
      $('#top-bar-background-color-input').val(top_color);
      $('#top-bar-background-color').val(top_color);

      // User's Message background color
      //$('#user-msg-background-color-input').val(msg_color);
      $('#user-msg-background-color').val(top_color);


      $('#top-bar-text-color-input').val(top_bar_text);
      $('#top-bar-text-color').val(top_bar_text);
      $('#top-bar-text-color-input').trigger('input');

      $('#chatbot-bg-color-input').val(chatbot_bg_color);
      $('#chatbot-bg-color').val(chatbot_bg_color);
      $('#chatbot-bg-color-input').trigger('input');

      $('#chatbot-msg-text-color-input').val(chatbot_msg_text);
      $('#chatbot-msg-text-color').val(chatbot_msg_text);
      $('#chatbot-msg-text-color-input').trigger('input');

      $('#chatbot-msg-background-color-input').val(chatbot_msg_bg_color);
      $('#chatbot-msg-background-color').val(chatbot_msg_bg_color);
      $('#chatbot-msg-background-color-input').trigger('input');

      $('#user-msg-background-color-input').val(user_msg_bg_color);
      $('#user-msg-background-color').val(user_msg_bg_color);
      $('#user-msg-background-color-input').trigger('input');

      $('#user-msg-text-color-input').val(user_msg_text);
      $('#user-msg-text-color').val(user_msg_text);
      $('#user-msg-text-color-input').trigger('input');

      $('#user-msg-background-new').val(user_msg_bg_color);
      $('#user-msg-background-new').trigger('input');

    });


  //  Auto select  chatbot profile UI
  var url = "{{ cfg.chatbot_image.url }}";
  var filename = url.split('/').pop();
  var parts = filename.split('_');

  $('#image-list-1 img').each(function() {
    if ($(this).attr('src').includes(parts[1])) {
      var newElementHTML = '<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatprofile-selected"></span>';
      $(this).parent().append(newElementHTML);
    }
  });

    //  Auto select  chatbot bg UI
  var Chat_bg_url = "{% if cfg.chatbot_background_pattern %}{{ cfg.chatbot_background_pattern.url }}{% else %}{% static 'backend/img/avatars/1.png' %}{% endif %}";
  var filename = Chat_bg_url.split('/').pop();
  var parts = filename.split('_');
  console.log(parts[-1]);
  lastElement = parts[parts.length - 1];

  $('#image-list-2 img').each(function() {
    if ($(this).attr('src').includes(lastElement)) {
      var newElementHTML = '<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatpattern-selected"></span>';
      $(this).parent().append(newElementHTML);
    }
  });

  // Chatbot bg pattern
  $('#chatbot-launcher-icon').on('input', function (e) {
    var file = e.target.files[0];
    var reader = new FileReader();
    reader.onload = function (event) {
    var base64Image = event.target.result;
    $(".launcher-icon").attr("src", base64Image);
    };
    reader.readAsDataURL(file);
  });
  // Chatbot click each image to input chatbot-launcher-icon
  $(document).on('click', '.chatbot-launcher-icon', function () {
    $('.chatlauncher-selected').remove()
    $(this).parent().append(`<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatlauncher-selected"></span>`);
    var img_attr = $(this).attr("src");
    var img_data = $(this).attr("src_data");
    $("#chatbot-launcher-icon-url").val(img_data);
    $("#chatbot-launcher-icon").val("");
    $(".launcher-icon").attr("src", img_attr);
  });


  //  Auto select  chatbot launcher icon
  var url = "{{ cfg.chatbot_launcher_icon.url }}";
  var filename = url.split('/').pop();
  var l_icon = filename.split('_');
  lastElement = l_icon[l_icon.length - 1];

  $('#image-list-3 img').each(function() {
    if ($(this).attr('src').includes(lastElement)) {
      var newElementHTML = '<span class="position-absolute top-0 start-100 translate-middle badge badge-dot p-2 border border-2 rounded-pill bg-primary chatlauncher-selected"></span>';
      $(this).parent().append(newElementHTML);
    }
  });

});