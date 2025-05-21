import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from rest_framework.exceptions import JsonResponse

from RAG_CHATBOT_BACKEND_APIS.services.AdminChatBotService import ChatBotService

logger = logging.getLogger('myapp')

class ChatBotController:
    # Create A Chat BOT Page
    @method_decorator(login_required(login_url='/login/'))
    def chatbot_dashboard_view(self, request, user_uuid):
        user = request.user
        logger.info(f"Rendering chatbot dashboard for user: {user_uuid} (User ID: {user.id})")
        
        openai_key = getattr(settings, "OPENAI_API_KEY", "")
        if not openai_key:
            messages.error(request, "Please fill your OpenAI API key first.")
            logger.warning("OpenAI API key is missing.")
        try:
            logger.debug(f"Fetching chatbots for User ID: {user.id}")
            chatbots = ChatBotService.get_user_chatbots(user.id)
            logger.info(f"Successfully fetched {len(chatbots)} chatbots for user {user.id}.")
        except Exception as e:
            logger.exception("Error fetching chatbots")
            chatbots = []

        context = {"chatbot": chatbots, "data": {"user_chatbots": chatbots}}
        return render(request, 'admin/Pages/ChatBot/CreateChatBotForm.html', context)

    @method_decorator(login_required(login_url='/login/'))
    @csrf_exempt
    def fetch_modal_content(self, request):
        logger.info("Fetching modal content for chatbot modal.")
        user_id = request.POST.get('user_id')
        chat_type = request.POST.get('chat_type')
        chat_id = request.POST.get('chat_id')

        logger.debug(f"Received modal fetch request - User ID: {user_id}, Chat Type: {chat_type}, Chat ID: {chat_id}")

        try:
            if chat_type == 'create':
                data = {}
                header, button_name = "Add Chat Bot", "Create"
                logger.info("Preparing modal for chatbot creation.")
            else:
                data = ChatBotService.get_chatbot_by_id(chat_id)
                header, button_name = "Update Chat Bot", "Update"
                logger.info(f"Preparing modal for chatbot update. Chat ID: {chat_id}")

            context = {"chat_type": chat_type, "user_id": user_id, "data": data, "header": header, "button_name": button_name}
            html_content = render(request, 'admin/Ajax/Chatbot/dynamic_chatbot_modal_content.html', context).content.decode('utf-8')
            logger.info("Rendered chatbot modal content successfully.")
            return JsonResponse({"status": "success", "message": "Rendered the HTML successfully", "html": html_content}, status=200)
        except Exception as e:
            logger.exception("Error fetching modal content")
            return JsonResponse({"status": "error", "message": "Failed to render chatbot modal."}, status=500)

    @method_decorator(login_required(login_url='/login/'))
    def handle_chatbot_action(self, request, user_uuid, curd_type):
        user = request.user
        formdata = request.POST
        chatbot_name = formdata.get('chatbotname')
        chat_id = formdata.get('chat_id')

        logger.info(f"Handling chatbot action '{curd_type}' for user: {user_uuid} (User ID: {user.id})")
        logger.debug(f"Action Type: {curd_type}, Chatbot Name: {chatbot_name}, Chat ID: {chat_id}")

        try:
            if curd_type == 'create':
                response = ChatBotService.create_chatbot(user, chatbot_name)
                if "success" in response:
                    messages.success(request, f"{response['success']}")
                    logger.info(f"Action '{curd_type}' completed successfully: {response['success']}")
                else:
                    messages.error(request, f"{response['error']}")
                    logger.error(f"Action '{curd_type}' failed: {response['error']}")
            elif curd_type == 'edit':
                response = ChatBotService.update_chatbot(user, chatbot_name, chat_id)
                if "success" in response:
                    messages.success(request, f"{response['success']}")
                    logger.info(f"Action '{curd_type}' completed successfully: {response['success']}")
                else:
                    messages.error(request, f"{response['error']}")
                    logger.error(f"Action '{curd_type}' failed: {response['error']}")
            elif curd_type == 'delete':
                response = ChatBotService.delete_chatbot(chat_id)
                if "success" in response:
                    messages.success(request, f"{response['success']}")
                    logger.info(f"Action '{curd_type}' completed successfully: {response['success']}")
                else:
                    messages.error(request, f"{response['error']}")
                    logger.error(f"Action '{curd_type}' failed: {response['error']}")
            else:
                response = {"error": "Invalid action."}
                logger.warning(f"Invalid chatbot action requested: {curd_type}")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/")
        except Exception as e:
            logger.exception(f"Unexpected error in handling chatbot action '{curd_type}'")
            messages.error(request, "An unexpected error occurred. Please try again later.")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/")
