import logging
import traceback
from urllib.parse import urlparse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Sum
from RAG_CHATBOT_BACKEND_APIS.models import Chat, ChatBotDB, ChatHistory, ChatbotAppearance, Document, WebsiteDB
from RAG_CHATBOT_BACKEND_APIS.services.AdminAuthServices import AuthServices
from RAG_CHATBOT_BACKEND_APIS.services.AdminChatBotService import ChatBotService
from RAG_CHATBOT_BACKEND_APIS.services.AdminChatbotContentServices import ChatbotContentManagementService
from RAG_CHATBOT_BACKEND_APIS.utils import get_base_url

# Configure logger
logger = logging.getLogger('myapp')

class ChatbotDashboardController:
    """
    Controller for handling chatbot dashboard functionalities, including viewing chatbot details, 
    uploading training documents, and handling website URL uploads.
    """
    def Share_Links(self, request, cc_id):
        logger.debug(f"Entering Share_Links with cc_id: {cc_id}")
        base_url = get_base_url(request)
        context = {"cc_id": cc_id, "base_url": base_url}
        logger.debug(f"Rendering integration_public_chatbot.html with context: {context}")
        return render(request, 'admin/Pages/ChatBot/integration_public_cahtbot.html', context)

    @method_decorator(login_required(login_url='/login/'))
    def view_chatbot_dashboard(self, request, user_uuid, chatbot_id, view_type):
        """
        Renders the chatbot dashboard based on the provided view type.
        Retrieves chatbot details, chat history, and associated documents/websites.
        """
        try:
            base_url = get_base_url(request)
            user_id = request.user.id

            logger.info(f"Loading chatbot dashboard for User: {user_id}, Chatbot ID: {chatbot_id}, View: {view_type}")

            chatbot_instance = ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
            logger.debug(f"Queried ChatBotDB for chatbot_id: {chatbot_id}, result: {chatbot_instance}")
            if not chatbot_instance:
                logger.error(f"Chatbot with ID {chatbot_id} not found!")
                return JsonResponse({"status": "error", "message": "Chatbot not found"}, status=404)
            chatbot_data = ChatBotService.ChatbotDetails(chatbot_instance.id, user_id)  # type: ignore        
            chats = Chat.objects.filter(user=user_id, chatbot_id=chatbot_instance.id)  # type: ignore
            chat_history = ChatHistory.objects.filter(user=user_id, chatbot_id=chatbot_instance.id)  # type: ignore
            cfg = ChatbotAppearance.objects.filter(chatbot_id=chatbot_id).first()
            documents = Document.objects.filter(chatbot=chatbot_instance, user=user_id)
            websites = WebsiteDB.objects.filter(chatbot=chatbot_instance, user=user_id)
            icode = ChatBotService.int_code_generate(chatbot_id, base_url)
            website_char_sum = WebsiteDB.objects.filter(chatbot=chatbot_instance.id, user=user_id).aggregate(Sum('no_of_characters'))[ # type: ignore
        "no_of_characters__sum"]
            print('website_char_sum', website_char_sum)
            context = {
                "data": {
                    "user_chatbots": chatbot_data,
                    "chats": chats,
                    "chat_history": chat_history,
                    "cfg": cfg,
                    "documents_data": {"documents": documents, "doc_count": documents.count()},
                    "websites_data": {"websites": websites, "web_count": websites.count(), "website_char_sum" : website_char_sum},
                    "int_code": icode
                }
            }
            logger.debug(f"Prepared context: {context}")
            logger.info("Dashboard data prepared successfully.")
            # Mapping view types to respective template pages
            view_map = {
                'document-list': 'admin/Pages/ChatBot/admin_create_chatbot.html',
                'website-list': 'admin/Pages/ChatBot/add-website-list.html',
                'chat-page-preview': 'admin/Pages/ChatBot/ChatBotPreview.html',
                'chat-history': 'admin/Pages/ChatBot/chat_History.html',
                'settings-training': 'admin/Pages/ChatBot/ChatBotSetting/chat_setting.html',
                'settings-chatbot-appearance': 'admin/Pages/ChatBot/ChatBotSetting/chat_setting_apperence.html',
                'settings-chatbot-delete': 'admin/Pages/ChatBot/ChatBotSetting/delete_chatbot_data.html',
                'integration': 'admin/Pages/ChatBot/share_chat_bot.html',
            }
    
            template = view_map.get(view_type, 'error_page.html')
            logger.debug(f"Rendering template: {template}")
            return render(request, template, context)
        except Exception as e:
            logger.error(f"Unexpected error in dashboard: {str(e)}\n{traceback.format_exc()}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    @method_decorator(login_required(login_url='/login/'))
    def process_chatbot_request(self, request, user_uuid, chatbot_id, action_type):
        logger.debug(f"Entering process_chatbot_request with action_type: {action_type}, chatbot_id: {chatbot_id}")
        if action_type == 'setting-training':
            chatbot_instance = ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
            logger.debug(f"Queried ChatBotDB for chatbot_id: {chatbot_id}, result: {chatbot_instance}")
            if not chatbot_instance:
                logger.error(f"Chatbot with ID {chatbot_id} not found!")
                messages.error(request, f"Chatbot with ID {chatbot_id} not found!")
                return redirect(f"/dashboard/user/{user_uuid}/chatbot/{chatbot_id}/settings-training/")
            chatbot_context = request.POST.get('chatbot_context', '')
            logger.debug(f"Updating chatbot context to: {chatbot_context}")
            chatbot_instance.context = chatbot_context  # type: ignore
            chatbot_instance.save()  # type: ignore
            logger.debug(f"Chatbot instance saved: {chatbot_instance}")
            messages.success(request, "Chatbot prompt updated successfully.")
            logger.info(f"Chatbot prompt updated for chatbot_id: {chatbot_id}")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/{chatbot_id}/settings-training/")
        elif action_type == 'chatbot-appearance':
            user_id = request.user.id
            chatbot_instance = ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
            bot_count = ChatbotAppearance.objects.filter(chatbot_id=chatbot_id).count()
            print('bot_count', bot_count)
            print('user_id', user_id)
            if request.method == "POST":
                data = request.POST
                cb_config = ChatbotAppearance.objects.get(chatbot_id=chatbot_id)
                data = request.POST
                fileData = request.FILES
                display_name = data.get("display-name")
                initial_messsage = data.get("initial-messsage")
                chatbot_mode = data.get("chatbot-mode")
                suggested_messages = data.get("suggested-messages")
                footer_name = data.get("footer_name")
                chatbot_theme_input = data.get("chatbot-theme-input")
                chatbot_bg_color_input = data.get("chatbot-bg-color-input")
                top_bar_bg_color_input = data.get("top-bar-background-color-input")
                top_bar_text_color_input = data.get("top-bar-text-color-input")
                chatbot_msg_bg_color_input = data.get("chatbot-msg-background-color-input")
                chatbot_msg_text_color_input = data.get("chatbot-msg-text-color-input")
                user_msg_background_color_input = data.get("user-msg-background-color-input")
                user_msg_text_color_input = data.get("user-msg-text-color-input")

                widget_width = data.get("widget-width")
                widget_height = data.get("widget-height")
                widget_position = data.get("widget-position")
                chatbot_font_style = data.get("chatbot-font-style")
                chatbot_font_size = data.get("chatbot-font-size")
                # popup_notification_delay = data.get("popup-notification-delay")

                # popup notification on / off control
                if data.get("popup-notification") == 'on':
                    popup_notification = True
                else:
                    popup_notification = False

                # Chatbot mode
                if chatbot_mode == 'on':
                    chatbot_mode = True
                else:
                    chatbot_mode = False
                   # if user clicks the profile chabnot profile  images manual upload
                chatbot_image = cb_config.chatbot_image if fileData.get("chatbot-image") == None else fileData.get(
            "chatbot-image") 
                print('chatbot_image', chatbot_image)  
                if len(str(data.get("chatbot-image-url")).strip()) != 0:
                    print('hhjhjhjhjhjhjhj')
                    chatbot_image = data.get("chatbot-image-url").lstrip('/')
                else:
                    chatbot_media_path = chatbot_instance.chat_bot_media_path # type: ignore
                    print('NOOOOOOOOOOOOOOOOOOOOOOOOOO', chatbot_media_path)
                    chatbot_image = 'xzcxzcxz'  
                cb_config.chatbot_mode = chatbot_mode
                cb_config.display_name = display_name
                cb_config.footer_name = footer_name
                cb_config.chatbot_theme = chatbot_theme_input
                cb_config.initial_message = initial_messsage
                cb_config.top_bar_textcolor = top_bar_text_color_input
                cb_config.bot_message_background = chatbot_msg_bg_color_input
                cb_config.bot_message_color = chatbot_msg_text_color_input
                cb_config.user_message_background = user_msg_background_color_input
                cb_config.user_message_color = user_msg_text_color_input
                cb_config.chatbot_background_color = chatbot_bg_color_input
                cb_config.font_family = chatbot_font_style
                cb_config.font_size = chatbot_font_size
                cb_config.show_popup_notification = popup_notification
                cb_config.save()
                ChatBotDB.objects.filter(chatbot_id=chatbot_id).update(chatbot_appearance=cb_config.id) # type: ignore
                messages.success(request, 'Chatbot Appearance Configuration Successfully Saved.')
            else:
                messages.error(request, 'Chatbot Appearance Configuration already exist')
                # return redirect("chatbot-appearance", c_id=c_id)
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/{chatbot_id}/settings-chatbot-appearance/")
        else:
            logger.error(f"Invalid action_type: {action_type}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=200)

    @method_decorator(login_required(login_url='/login/'))
    def upload_and_start_training(self, request, user_uuid, chatbot_id, upload_type):
        """
        Handles the upload process for chatbot training data.
        Supports both document file uploads and website URL submissions.
        """
        try:
            logger.info(f"Uploading training data. Type: {upload_type}, User: {request.user.id}, Chatbot ID: {chatbot_id}")
            logger.debug(f"Request method: {request.method}, POST data: {request.POST}, FILES: {request.FILES}")
            if upload_type == 'file':
                result = self._handle_training_logic_for_uploading_documents(request, user_uuid, chatbot_id)
            elif upload_type == 'upload-website':
                result = self._handle_training_logic_for_website_urls(request, user_uuid, chatbot_id)
            else:
                logger.error(f"Invalid upload type: {upload_type}")
                return JsonResponse({"status": "error", "message": "Invalid upload type"}, status=400)

            logger.debug(f"Upload result: {result}")
            if result["status"] == "error":
                messages.error(request, result["message"])
                return JsonResponse(result, status=400)
            messages.success(request, "Training started successfully!")
            logger.info(f"Training started successfully for chatbot_id: {chatbot_id}")
            return redirect(f"/dashboard/user/{user_uuid}/chatbot/{chatbot_id}/website-list/")
        except Exception as e:
            logger.error(f"Unexpected error in training upload: {str(e)}\n{traceback.format_exc()}")
            return JsonResponse({"status": "error", "message": "An unexpected error occurred"}, status=500)

    def _handle_training_logic_for_website_urls(self, request, user_uuid, chatbot_id):
        """
        Processes and validates website URL uploads for chatbot training.
        """
        try:
            website_url = request.POST.get('url')
            logger.info(f"Processing website URL upload: {website_url} for Chatbot {chatbot_id}")
            logger.debug(f"Validating URL: {website_url}")
            if not website_url or not urlparse(website_url).scheme or not urlparse(website_url).netloc:
                logger.error("Invalid or empty URL!")
                return {"status": "error", "message": "Invalid URL format"}
            user_id = request.user.id
            chatbot = ChatBotService.get_chatbot_by_user_and_id(chatbot_id, user_id)
            logger.debug(f"Queried chatbot: {chatbot}")
            if not chatbot:
                return {"status": "error", "message": "Chatbot not found"}

            user = AuthServices.fetch_user_data('uuid', user_uuid)
            logger.debug(f"Queried user by UUID {user_uuid}: {user}")
            if not user:
                return {"status": "error", "message": "User not found"}

            logger.info(f"Processing website URL upload: {website_url} for Chatbot {chatbot_id}")
            response, message, uploaded_documents = ChatbotContentManagementService.upload_and_process_chatbot_website_urls(user, chatbot, website_url)
            logger.debug(f"Website processing response: {response}, message: {message}, uploaded_documents: {uploaded_documents}")
            print('Response: ', response)  # Consider replacing print with logger for production
            uploaded_documents = {}  # This line might be redundant depending on service behavior
            return {"status": "success", "uploaded_documents": uploaded_documents}
        except Exception as e:
            logger.error(f"Error processing website URLs: {str(e)}\n{traceback.format_exc()}")
            return {"status": "error", "message": "An error occurred"}

    def _handle_training_logic_for_uploading_documents(self, request, user_uuid, chatbot_id):
        """
        Processes document uploads for chatbot training.
        """
        try:
            user_id = request.user.id
            chatbot = ChatBotService.get_chatbot_by_user_and_id(chatbot_id, user_id)
            logger.debug(f"Queried chatbot: {chatbot}")
            if not chatbot:
                return {"status": "error", "message": "Chatbot not found"}

            user = AuthServices.fetch_user_data('uuid', user_uuid)
            logger.debug(f"Queried user by UUID {user_uuid}: {user}")
            if not user:
                return {"status": "error", "message": "User not found"}

            logger.info(f"Processing document upload for Chatbot ID {chatbot_id}")
            logger.debug(f"Files in request: {request.FILES}")
            response, message, uploaded_documents = ChatbotContentManagementService.upload_and_process_chatbot_documents(user, chatbot, request.FILES)
            logger.debug(f"Document processing response: {response}, message: {message}, uploaded_documents: {uploaded_documents}")
            return {"status": "success", "uploaded_documents": uploaded_documents}
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}\n{traceback.format_exc()}")
            return {"status": "error", "message": "An error occurred"}