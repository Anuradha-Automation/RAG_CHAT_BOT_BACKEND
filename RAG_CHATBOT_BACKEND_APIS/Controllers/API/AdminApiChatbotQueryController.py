import logging
import traceback
from django.http import JsonResponse  # Correct import for JsonResponse
from rest_framework.views import APIView
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, CustomUser
from RAG_CHATBOT_BACKEND_APIS.services.Langchain_Models.LangchainEmbeddingService import LangchainEmbeddingService

logger = logging.getLogger(__name__)

class ChatbotQueryApiController(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to process chatbot queries.
        """
        logger.debug(f"Entering POST request with data: {request.data}, query params: {request.GET}")
        
        query = request.data.get('query')
        chat_id = request.GET.get("chat_id")
        logger.debug(f"Extracted query: {query}, chat_id: {chat_id}")

        if not chat_id:
            logger.error("Missing chat_id or user_id")
            return JsonResponse({"status": "failed", "message": "Missing chat_id or user_id"}, status=400)
        
        if not query:
            logger.error("Query parameter is missing")
            return JsonResponse({"error": "Query parameter is missing"}, status=400)
        
        chatbot = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        logger.debug(f"Queried ChatBotDB for chat_id: {chat_id}, result: {chatbot}")
        if not chatbot:
            logger.error(f"Invalid chat_id: {chat_id}")
            return JsonResponse({"status": "failed", "message": "Invalid chat_id"}, status=404)
        
        try:
            user = CustomUser.objects.get(id=chatbot.user.id)  # type: ignore
            logger.debug(f"Queried CustomUser for user_id: {chatbot.user.id}, result: {user}") # type: ignore
        except CustomUser.DoesNotExist:
            logger.error(f"User not found for user_id: {chatbot.user.id}") # type: ignore
            return JsonResponse({"status": "failed", "message": "User not found"}, status=404)
        
        try:
            logger.info(f"Processing query for chat_id: {chat_id}, query: {query}")
            results = LangchainEmbeddingService.GetResponseFromQuery(chatbot, user, query)
            logger.debug(f"Query processing results: {results}")
            logger.info(f"Successfully processed query for chat_id: {chat_id}")
            return JsonResponse({"results": results}, safe=False, status=200)
        except Exception as e:
            logger.error(f"Error processing query for chat_id: {chat_id}: {str(e)}\n{traceback.format_exc()}")
            return JsonResponse({"error": "Internal server error"}, status=500)