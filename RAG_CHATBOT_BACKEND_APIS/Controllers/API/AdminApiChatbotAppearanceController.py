import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from RAG_CHATBOT_BACKEND_APIS.Serializers.chatbot_document_serializers import ChatbotAppearanceSerializer
from RAG_CHATBOT_BACKEND_APIS.models import ChatbotAppearance
from RAG_CHATBOT_BACKEND_APIS.utils import get_base_url

logger = logging.getLogger(__name__)

class AdminApiChatbotAppearanceController(APIView):
    def get(self, request):
        """
        Handles GET requests to retrieve chatbot appearance data.
        """
        logger.debug(f"Entering GET request with query params: {request.GET}")
        
        chat_id = request.GET.get("chat_id")
        request_type = request.GET.get("type")  # Renamed 'type' to 'request_type' to avoid reserved keyword
        logger.debug(f"Extracted chat_id: {chat_id}, request_type: {request_type}")

        if not chat_id:
            logger.error("Missing chat_id")
            return Response({"status": "failed", "message": "Missing chat_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chatbot_appearance = get_object_or_404(ChatbotAppearance, chatbot_id=chat_id)
            logger.debug(f"Queried ChatbotAppearance for chat_id: {chat_id}, result: {chatbot_appearance}")
            
            serializer = ChatbotAppearanceSerializer(chatbot_appearance)
            logger.debug(f"Serialized data: {serializer.data}")
            
            logger.info(f"Successfully retrieved appearance data for chat_id: {chat_id}")
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving chatbot appearance for chat_id: {chat_id}: {str(e)}\n{traceback.format_exc()}")
            return Response({"status": "error", "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)