from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB

def chatbot_context(request):
    """Provides chatbot data to all templates."""
    context = {"global_chatbots": None}  # Default structure
    if request.user.is_authenticated:
        chatbots = ChatBotDB.objects.filter(user=request.user)  # Fix filter
        context["global_chatbots"] = {"chatbot": chatbots, "data": {"user_chatbots": chatbots}} # type: ignore
    return context
