from django.urls import path

from RAG_CHATBOT_BACKEND_APIS.Controllers.AdminAuthController import AuthController
from RAG_CHATBOT_BACKEND_APIS.Controllers.AdminChatBotController import ChatBotController
from RAG_CHATBOT_BACKEND_APIS.Controllers.AdminChatbotDashboardController import ChatbotDashboardController
from RAG_CHATBOT_BACKEND_APIS.Controllers.AdminDashboardController import AdminDashboardController
from RAG_CHATBOT_BACKEND_APIS.Middleware.auth_middleware import custom_login_required, redirect_if_authenticated

# Import Controllers

# Define URL patterns
urlpatterns = []

# Authentication URLs
admin_auth_urls = [
    path('register/', redirect_if_authenticated(AuthController().auth_register_page), name='register'),
    path('login/', redirect_if_authenticated(AuthController().auth_login_page), name='login'),
    path('logout/', AuthController().auth_logoutSession, name='logout'),
    path("forget-password/", redirect_if_authenticated(AuthController().forget_password_page), name="forget-password"),
    path('reset-password/<uidb64>/<token>/', redirect_if_authenticated(AuthController().reset_password_page), name='reset_password'),

]

# Admin Dashboard URLs
admin_dashboard_urls = [
    # Dashboard URL
    # path("dashboard/", AdminDashboardController().admin_dashboard_page, name="admin.dashboard"),
    path('dashboard/', custom_login_required(AdminDashboardController().admin_dashboard_page), name='admin_dashboard'),
    
    # Profile Settings
    path('dashboard/profile/<str:user_uuid>/setting-account/', custom_login_required(AdminDashboardController().SettingProfileAccount), name='admin.profile.setting.profile'),
    path("dashboard/profile/<str:user_uuid>/setting-security/", custom_login_required(AdminDashboardController().SettingProfileSercurity), name="admin.profile.setting.security"),
    
    # User Chatbot Management
    path("dashboard/user/<str:user_uuid>/chatbot/", custom_login_required(ChatBotController().chatbot_dashboard_view), name="admin.user.chatbot"),
    path('dashboard/chatbot/fetch-modal-content/', custom_login_required(ChatBotController().fetch_modal_content), name='admin.fetch_modal_content_for_chat_bot'),
    path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/<str:view_type>/", custom_login_required(ChatbotDashboardController().view_chatbot_dashboard), name="admin.user.chatbot.dashboard"),
    path("chatbot/share/public/<str:cc_id>/", ChatbotDashboardController().Share_Links, name="chatbot.share_links"),

    # Upload Documents and Website Data  for Chatbot oN the Source 
    path("dashboard/user/<str:user_uuid>/chatbot/post/<str:curd_type>", custom_login_required(ChatBotController().handle_chatbot_action), name="admin.user.chatbot.manage"),
    path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/upload/<str:upload_type>", custom_login_required(ChatbotDashboardController().upload_and_start_training), name="admin.user.chatbot.upload-document"),
    # Chatbot View COntroller 
    path("dashboard/user/<str:user_uuid>/chatbot/<str:chatbot_id>/action/<str:action_type>", custom_login_required(ChatbotDashboardController().process_chatbot_request), name="admin.user.chatbot.hendle-action"),

]

# Public URLs (if any, add them here)
public_urls = [
    # Chatbot Frontend
     
]

# Combine all URL patterns
urlpatterns += admin_auth_urls + admin_dashboard_urls + public_urls 

# Serve media files in development mode

