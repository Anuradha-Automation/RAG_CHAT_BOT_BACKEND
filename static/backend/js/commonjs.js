
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

function NotyfMessage(message, type) {
    var notyf = new Notyf();
    if (type === 'success') {
        notyf.success(message);
    } else if (type === 'error') {
        notyf.error(message);
    } else if (type === 'warning') {
        notyf.error(message);
    }
}


let messages = [];
jQuery(".django-message").each(function () {
    messages.push({ text: $(this).data("text"), type: $(this).data("type") });
});

if (messages.length > 0) {
    let messageText = messages.map(m => m.text).join("\n");
    Swal.fire({
        title: "Notifications",
        
        text: messageText,
        icon: messages.some(m => m.type === 'error') ? 'error' :
            messages.some(m => m.type === 'success') ? 'success' :
                messages.some(m => m.type === 'warning') ? 'warning' : 'info',
        confirmButtonText: "OK"
    }).then(() => {
        console.log("Notification displayed.");
    });
}