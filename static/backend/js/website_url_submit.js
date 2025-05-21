  $(document).ready(function(){
    // Page block ui Initiate with custom message
    function block_ui(msg){
      $.blockUI({
            message: `<div class="d-flex justify-content-center"><p class="mb-0">`+msg+`</p> <div class="sk-wave m-0"><div class="sk-rect sk-wave-rect"></div> <div class="sk-rect sk-wave-rect"></div> <div class="sk-rect sk-wave-rect"></div> <div class="sk-rect sk-wave-rect"></div> <div class="sk-rect sk-wave-rect"></div></div> </div>`,
            // timeout: 30e3,
            css: {
                backgroundColor: "transparent",
                color: "#fff",
                border: "0"
            },
            overlayCSS: {
                opacity: .5
            }
        });
    };

    // time sleep
    function timeSleep(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    }
    //  Fetch URLs from Websites
    $(document).on("click", "#fetch_urls", function () {

      $("#fetch-url-form").validate({
        rules: {
          fetch_url: {
            required: true,
            // pattern: /^(?!.*\.xml$).+/i
          },
        },
        messages: {
          fetch_url: {
            required: "Please enter your URL",
            // pattern: "URLs ending with .xml are not allowed"
          },
        },
        errorElement: 'div',
        errorLabelContainer: '.errorTxt',
        submitHandler: function (form) {
          $(".btn-close").trigger('click');
          url = "/beautiful_scrap_cmd/";
          $("#div_for_refresh_url").attr('id', "div_for_refresh_url_disable");
          var url_data = $('#fetch-url').val();
          var url_data = url_data.replace(/\/$/, '');
          var chatbot_id = $('#chatbot_id').val();
          var csrf_token = "{{csrf_token}}"
          $('[data-target="#app-url-view"]').addClass('d-none');
          $('[data-target="#app-scrape-url-view"]').removeClass('d-none');
          $('.progress-horizontal').html(`Crawling ${url_data} please wait...`)
          $('#fetch_urls').addClass('cursor-na').attr('disabled', true);
          $('#delete_multi').addClass('d-none');
          $('.multi-url-delete').text('Delete');
          animateProgressBar(animationDuration);
          // $(".progress").show()
          // $(".progress-horizontal").show()
          // progress()
          $.ajax({
            type: 'POST',
            url: url,
            data: { urldata: url_data, csrfmiddlewaretoken: csrf_token, chatbot_id: chatbot_id },
            success: function (data) {
              var links_count = data['counts']['links_count']
              var total_char = data['counts']['total_char_count']
              showCompleteProgress()
              $('#fetch_urls').removeClass('cursor-na').removeAttr('disabled');
              $('#url-container').removeClass('d-none');
              $('.progress-horizontal').html(`Crawling ${url_data} Completed, Select and Submit to add urls.`)
              if (data['links_data'].length >= 1) {
                var dataItems = "";
                var i=0;
                $.each(data['links_data'], function (key, value) {
                  i++;
                  console.log(key, value['url']);
                  dataItems += `<div class="row list-group-item list-group-item-action d-flex align-items-center cursor-pointer waves-effect">
                                    <div class="d-flex justify-content-center align-items-center">
                                        <div class="form-check mt-1">
                                            <input class="form-check-input" type="hidden" value="`+ value['char'] + `" name="url-characters">
                                            <textarea class="form-check-input d-none" name="url-content"> ${value['text']}</textarea>
                                            <input class="form-check-input childCheckbox" type="checkbox" value="`+ value['url'] + `" name="child_checkbox" id="child-checkbox">
                                            <label class="form-check-label d-none" for="child-checkbox"></label>
                                        </div>
                                        <input type="text" class="form-control url-input" value="`+  value['url'] + `" name='urls' disabled>
                                        <div class="d-flex justify-content-center align-items-center url-delete">
                                            <small class="eye">`+ value['char'].toLocaleString('en-US')+`</small>
                                            <span class="mdi mdi-eye text-secondary ps-2 mx-2 show-content" id="content_${i}" data-bs-toggle="modal" data-bs-target="#ShowContent">

                                            </span>
                                            <span class="mdi mdi-trash-can text-danger ps-2 mx-1" data-bs-toggle="tooltip" data-bs-placement="bottom"
                                                data-bs-custom-class="tooltip-danger" data-bs-original-title="Remove"></span>
                                        </div>
                                    </div>
                                </div>`
                });
                $('#url-container').append(dataItems)
                var temp_button = $('.temp-button')
                if (temp_button) {
                  temp_button.remove()
                }
                var er_message = $('#error-message')
                if (er_message) {
                  er_message.remove()
                }
                $('#url-container').append(`<div class="temp-button"><div class="mt-4"></div>
                <div class="d-flex justify-content-end align-items-center m-4 gap-2">
                  <div class="">
                      <label for="link_count">Links Count:</label> <strong class='font-weight-bold' id="link_count" > `+ links_count.toLocaleString('en-US') +` </strong>
                      </div>
                    <div class="">
                      <label for="char_count">Total Characters Count:</label> <strong class='font-weight-bold' id="character_count"> `+ total_char.toLocaleString('en-US') +` </strong>
                      </div>
                  </div>
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <label for="re_fetch">Choose refresh time:</label>
                    <select name="refetch_time" id="re_fetch" required>
                      <option value="0m">No refresh</option>
                      <option value="2m">2 Minutes</option>
                      <option value="5m">5 Minutes</option>
                      <option value="10m">10 Minutes</option>
                      <option value="1d">1 Day</option>
                      <option value="10d">10 Day</option>
                    </select>
                    <button class="btn btn-primary me-md-2" type="submit" id="submit_urls">Submit</button>
                    <button class="btn btn-danger" type="button" id="back">Back</button>
                    </div>
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <div class="m-3 text-danger font-weight-bold" id="showselecterror"></div>
                </div>
            </div>`)
              }
              else {
                $('#error-message').removeClass('d-none')
                // $('#url-container').append(`<div class="row list-group-item list-group-item-action d-flex align-items-center cursor-pointer waves-effect"><div class="temp-button1 text-danger text-center"> Something Went wrong </div></div>`)
              }
            },
            error: function (data) {
              var error = data
              console.log(error, "----------- err")
              $('#error-message').removeClass('d-none')
              $(".url-progress-bar").addClass("url-progress-error").removeClass("url-progress-bar").html('');
              $('.progress-horizontal').html(`Crawling stopped ${url_data} please try again`)

            }
          })
        }
      });
    });

    //  Get Sitemap xml data
    $(document).on("click", "#get_xml_urls", function () {

      $.validator.addMethod("endsWithXml", function (value, element) {
        return this.optional(element) || value.toLowerCase().endsWith(".xml");
      }, "Please enter a URL ending with .xml");

      $("#xml-url-form").validate({
        rules: {
          xml_url: {
            required: true,
            endsWithXml: true
          },
        },
        messages: {
          xml_url: {
            required: "Please enter your URL",
            endsWithXml: "Please enter a URL ending with .xml"
          },
        },
        errorElement: 'div',
        errorLabelContainer: '.errorTxt',
        submitHandler: function (form) {
          $(".btn-close").trigger('click')
          animateProgressBar(animationDuration);
          url = "/sitemap_crawl/"
          $("#div_for_refresh_url").attr('id', "div_for_refresh_url_disable");
          var url_data = $('#xml-url').val();
          var url_data = url_data.replace(/\/$/, '');
          var chatbot_id = $('#chatbot_id').val();
          var csrf_token = "{{csrf_token}}";
          $('[data-target="#app-url-view"]').addClass('d-none');
          $('[data-target="#app-scrape-url-view"]').removeClass('d-none');
          $('#get_xml_urls').addClass('cursor-na').attr('disabled', true);
          $('.progress-horizontal').html(`${url_data} Sitemap URLS crawling please wait...`);
          $('#delete_multi').addClass('d-none');
          $('.multi-url-delete').text('Delete');
          $.ajax({
            type: 'POST',
            url: url,
            data: { urldata: url_data, csrfmiddlewaretoken: csrf_token, chatbot_id: chatbot_id },
            success: function (data) {
              var dataItems = "";
              $('#fetch_urls').removeClass('cursor-na').removeAttr('disabled')
              $('#url-container').removeClass('d-none')
              $('.progress-horizontal').html(`${url_data} Sitemap URLS crawling Completed.`);
              showCompleteProgress()
              var links_count = data['counts']['links_count']
              var total_char = data['counts']['total_char_count']
              $.each(data['links_data'], function (key, value) {

                dataItems += `<div class="row list-group-item list-group-item-action d-flex align-items-center cursor-pointer waves-effect">
                            <div class="d-flex justify-content-center align-items-center">
                                  <div class="d-flex justify-content-center align-items-center">
                                    <div class="form-check mt-1">
                                      <input class="form-check-input" type="hidden" value="`+ value['char'] + `" name="url-characters">
                                      <input class="form-check-input childCheckbox" type="checkbox" value="`+  value['url'] + `" name="child_checkbox" id="child-checkbox">
                                      <label class="form-check-label d-none" for="child-checkbox"></label>
                                    </div>
                                  </div>

                            <div class="flex-grow-1">
                              <input type="text" class="form-control url-input" value="`+  value['url'] + `" name='urls'>
                            </div>
                            <div class="col-1 d-flex justify-content-center align-items-center url-delete">
                              <small>`+ value['char'].toLocaleString('en-US')+`</small>
                                <span class="mdi mdi-trash-can text-danger ps-2" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-custom-class="tooltip-danger" data-bs-original-title="Remove"></span>
                            </div>
                        </div>
                      </div>`
              });

              var temp_button = $('.temp-button')
              if (temp_button) {
                temp_button.remove()
              }
              var er_message = $('#error-message')
              if (er_message) {
                er_message.remove()
              }
              $('#url-container').append(dataItems);
              $('#url-container').append(`<div class="temp-button"><div class="mt-4"></div>
                            <div class="d-flex justify-content-end align-items-center m-4 gap-2">
                                <div class="">
                                  <label for="link_count">Links Count:</label> <strong class='font-weight-bold' id="link_count" > `+ links_count.toLocaleString('en-US') +` </strong>
                                  </div>
                                <div class="">
                                  <label for="char_count">Total Characters Count:</label> <strong class='font-weight-bold' id="character_count"> `+ total_char.toLocaleString('en-US') +` </strong>
                                  </div>
                                </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <label for="re_fetch">Choose refresh time:</label>
                                <select name="refetch_time" id="re_fetch" required>
                                  <option value="0m">No refresh</option>
                                  <option value="2m">2 Minutes</option>
                                  <option value="5m">5 Minutes</option>
                                  <option value="10m">10 Minutes</option>
                                  <option value="1d">1 Day</option>
                                  <option value="10d">10 Day</option>
                                </select>
                                <button class="btn btn-primary me-md-2 " type="submit" id="submit_urls">Submit</button>
                                <button class="btn btn-danger" type="button" id="back">Back</button>
                                </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <div class="m-3 text-danger font-weight-bold" id="showselecterror"></div>
                            </div>
                        </div>`);
            },
            error: function (data) {
              $('#error-message').removeClass('d-none')
              $(".url-progress-bar").addClass("url-progress-error").removeClass("url-progress-bar").html('');
              $('.progress-horizontal').html(`Crawling stopped ${url_data} please try again`)
            }
          })
        }
      });


    });


    //  Form submit for all websites
    $('#urlForm').submit(async function (event) {
      event.preventDefault(); // Prevent the default form submission

      // Get the form data
      var url_checkbox = document.getElementsByName('child_checkbox');
      var chatbot_id = $('#chatbot_id').val();
      var re_fetch_time = $('#re_fetch').val();
      // var urls = [];

      // for (var checkbox of url_checkbox) {
      //   if (checkbox.checked)
      //     urls.push(checkbox.value);
      // }
      var url = [];
      var char = []
      var content = []
        $('.childCheckbox:checked').each(function() {
            var checkbox = $(this);

            var urlValue = checkbox.val();
            url.push(urlValue);

            var charValue = checkbox.closest('.form-check').find('[name="url-characters"]').val();
            char.push(charValue)

            var contentValue = checkbox.closest('.form-check').find('[name="url-content"]').html();
            console.log(contentValue);
            content.push(contentValue.trim());
        });

      if (Object.keys(url).length === 0) {
        document.getElementById("showselecterror").innerHTML = "Please Select Any Value Before Submit!";
        return
      }

        // block btns
        var submitt_btn = document.getElementById("submit_urls");
        submitt_btn.setAttribute('disabled', true);
        var back_btn = document.getElementById("back");
        back_btn.setAttribute('disabled', true);

        // scroll to top
        var scrollableDiv = document.getElementById("email-list-scroll");
        scrollableDiv.scrollTop = 0;

        $('.progress-horizontal').html(`Training, please wait...`)

        var progressBarElements = document.getElementsByClassName('url-progress-bar-stop');
        if (progressBarElements.length > 0) {
            progressBarElements[0].style.removeProperty("width");
        }
        var progressTextElements = document.getElementsByClassName('url-progress-text-stop');
        if (progressTextElements.length > 0) {
            progressTextElements[0].innerHTML = '0%';
        }

        await timeSleep(1000);

       // Function to update the progress bar
        function updateProgressBar(progressBar, progressText, percentage) {
            if (progressBar) {
                progressBar.style.width = percentage + '%';
            }

            if (progressText) {
                progressText.innerHTML = percentage + '%';
            }
        }

        // Assuming you have an array of progress bar elements and text elements
        var progressBarElements = document.getElementsByClassName('url-progress-bar-stop');
        var progressTextElements = document.getElementsByClassName('url-progress-text-stop');

        // Define the total duration for the animation in milliseconds
        var animationDuration = 10000; // For example, 10 seconds

        // Loop to update the progress every second
        for (var i = 0; i <= 99; i++) {

            setTimeout(function (percentage) {
                return async function () {
                    if (percentage > 60) {
                      await timeSleep(3000);
                      updateProgressBar(progressBarElements[0], progressTextElements[0], percentage);
                    }
                    else {
                      updateProgressBar(progressBarElements[0], progressTextElements[0], percentage);
                    }
                };
            }(i), i * (animationDuration / 10));
        }


      // Make the AJAX request
      $.ajax({
        url: '/urls_saver/{{ data.chatbot_id }}',  // Replace with your actual backend URL
        type: 'POST',
        data: { chatbot_id: chatbot_id, urls: url,characters:char, content:content, re_fetch_time: re_fetch_time },  // Pass chatbot_id and urls as an object
        headers: {
          'X-CSRFToken': "{{csrf_token}}"  // Get the CSRF token value
        },
        success: async function (response) {
          showCompleteProgress()
          await timeSleep(700);
          // Handle the success response from the server
          window.location.reload()
        },
        error: function (xhr, errmsg, err) {
          // Handle any errors
          window.location.reload()
          console.log(xhr.status + ": " + xhr.responseText);
        }
      });
    });


    // Attach a click event to the parent checkbox
    $('#parent_checkbox').click(function () {
        var isChecked = $(this).prop('checked');
        $('.childCheckbox').prop('checked', isChecked);
    });

    $('.childCheckbox').click(function () {
        var allChecked = $('.childCheckbox:checked').length === $('.childCheckbox').length;
        $('#parent_checkbox').prop('checked', allChecked);
    });

    //  remove added ajax urls
    $(document).on("click", ".mdi-trash-can", function () {
        $(this).closest('.row').hide().delay(2000).remove();
        $(this).closest('.row').remove();
    });
  });
