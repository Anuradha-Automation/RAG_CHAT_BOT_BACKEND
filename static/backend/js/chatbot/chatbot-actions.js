// Chat Bot Modal Open
$(document).on('click', '#chat_bot_modal_box', async function(event) {
    let url = $(this).data("url");
    let fullUrl = window.location.origin + url;
    let ajax_value_list = {
        user_id: $(this).data("login-user-id"),
        chat_type: $(this).data("model-type"),
        chat_id: $(this).data("chat_id")
    };

    console.log("Opening chat bot modal with URL: ", fullUrl);
    const [resPose] = await Promise.all([Ajax_response(fullUrl, "POST", ajax_value_list, '')]);
    
    if (resPose.status === 'success') {
        $("#modal_content").html(resPose.html);
        $("#modalCenter").modal("show");
        console.log("Modal displayed with content.");
    }
});

// Chat Bot Delete Action
$(document).on('click', '#chat_bot_delete', async function(event) {
    const form = document.createElement("form");
    let url = $(this).data("url");
    form.method = "POST";
    form.id = "chat_bot_modal_form";
    form.action = url;

    const csrfToken = document.createElement("input");
    csrfToken.type = "hidden";
    csrfToken.name = "csrfmiddlewaretoken";
    csrfToken.value = getCSRFToken(); 
    form.appendChild(csrfToken);

    const userIdInput = document.createElement("input");
    userIdInput.type = "hidden";
    userIdInput.name = "user_id";
    userIdInput.value = $(this).data("login-user-id");
    form.appendChild(userIdInput);

    const chatTypeInput = document.createElement("input");
    chatTypeInput.type = "hidden";
    chatTypeInput.name = "curd_type";
    chatTypeInput.value = $(this).data("model-type");
    form.appendChild(chatTypeInput);

    document.body.appendChild(form);
    
    const botIdInput = document.createElement("input");
    botIdInput.type = "hidden";
    botIdInput.name = "chat_id";
    botIdInput.value = $(this).data("chat_id");
    form.appendChild(botIdInput);

    Swal.fire({
        title: "Do you want to delete the bot?",
        showDenyButton: false,
        showCancelButton: true,
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel"
    }).then(async (result) => {
        if (result.isConfirmed) {
            console.log("Bot deletion confirmed.");
            form.submit();
        } else {
            console.log("Bot deletion canceled.");
        }
    });
});
