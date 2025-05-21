from django.urls import path

from RAG_CHATBOT_BACKEND_APIS.Controllers.API.AdminApiChatbotAppearanceController import AdminApiChatbotAppearanceController
from RAG_CHATBOT_BACKEND_APIS.Controllers.API.AdminApiChatbotQueryController import ChatbotQueryApiController


urlpatterns = [
     path("chatbot/appearances/", AdminApiChatbotAppearanceController.as_view(), name="chatbot-query"),
    path("chatbot/query/", ChatbotQueryApiController.as_view(), name="chatbot-query"),
]