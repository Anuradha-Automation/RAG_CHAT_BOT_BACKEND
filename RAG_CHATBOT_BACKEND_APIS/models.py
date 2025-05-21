
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from RAG_CHATBOT_BACKEND_APIS.utils import format_name, get_random_str  # Update if using a custom model
from django.db import models
def user_directory_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Rename the file to avoid name conflicts
    filename = f"profile_pic.{ext}"
    return os.path.join(instance.username, "user_profile", filename)

# CustomUser Model 
class CustomUser(AbstractUser):
    uuid = models.CharField(max_length=255,default=get_random_str,editable=False, unique=True)
    slug = models.SlugField(default="", allow_unicode=True, blank=True, )
    phone_code = models.CharField(max_length=10, default="", blank=True, )
    phone_number = models.CharField(max_length=15, default="", blank=True, )
    profile_pic = models.FileField(upload_to=user_directory_path, blank=True, max_length=250)
    def save(self, *args, **kwargs):
        if self.pk:
            old_profile_pic = CustomUser.objects.get(pk=self.pk).profile_pic
            if self.profile_pic and self.profile_pic != old_profile_pic:
                if old_profile_pic and os.path.exists(old_profile_pic.path):
                    os.remove(old_profile_pic.path)
        super(CustomUser, self).save(*args, **kwargs)
    profile_url = models.TextField(default="", blank=True)
    name = models.CharField(max_length=250, default="", blank=True)
    zip_code = models.CharField(max_length=250, default="", blank=True)
    organization = models.CharField(max_length=250, default="", blank=True)
    address = models.TextField(default="", blank=True)
    state = models.CharField(max_length=250, default="", blank=True)
    country = models.CharField(max_length=250, default="US", blank=True)
    age = models.CharField(max_length=250, default="", blank=True)
    user_chroma_path = models.TextField(default="", blank=True)
    user_upload_path = models.TextField(default="", blank=True)
    language = models.CharField(max_length=250, default="", blank=True)
    status = models.BooleanField(default=True)


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=3, null=True, blank=True)
    numeric_code = models.CharField(max_length=3, null=True, blank=True) 
    iso2 = models.CharField(max_length=2, null=True, blank=True) 
    phonecode = models.CharField(max_length=255, null=True, blank=True)  
    currency_name = models.CharField(max_length=255, null=True, blank=True) 
    currency_symbol = models.CharField(max_length=255, null=True, blank=True) 
    tld = models.CharField(max_length=255, null=True, blank=True) 
    native = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True) 
    subregion = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    timezones = models.TextField(null=True, blank=True)
    translations = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)  # latitude
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)  # longitude
    emoji = models.CharField(max_length=191, null=True, blank=True)
    emojiU = models.CharField(max_length=191, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now=True) 
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)
    wikiDataId = models.CharField(max_length=255, null=True, blank=True, help_text="Rapid API GeoDB Cities")  # wikiDataId

class State(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='states')
    country_code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=255, null=True, blank=True)
    iso2 = models.CharField(max_length=255, null=True, blank=True)
    state_type = models.CharField(max_length=191, null=True, blank=True)
    latitude = models.TextField(null=True, blank=True)
    longitude = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)
    wikiDataId = models.CharField(max_length=255, null=True, blank=True, help_text="Rapid API GeoDB Cities")
    def __str__(self):
        return self.name
class Thread(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class UserThread(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)  # Django auto-creates 'thread_id'
    unique_thread_id = models.CharField(max_length=100, unique=True)  # Avoids conflict
    status = models.CharField(max_length=50, default="Pending")
    log_messages = models.TextField(blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'thread')

PINECONE_INDEX_NAME = str(os.getenv("PINECONE_INDEX_NAME"))
class ChatBotDB(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('restricted', 'Restricted'),
    )
    LOGIN_STATUS = (
        ("anonymous", 'Anonymous'),
        ("login", 'Login')
    )
    LLM_MODEL = (
        ("system openai", 'System OpenAi'),
        ("private openai", 'Private OpenAi'),
        ("gpt4all", 'GPT4ALL'),
        ("huggingface", 'HuggingFace'),
    )
    MODEL = (
        ("gpt-3.5-turbo", 'gpt-3.5-turbo'),
        ("gpt-4", 'gpt-4'),
    )
    VECTOR_DATABASE = (
        ("chroma", 'Chroma'),
        ("pinecone", 'Pinecone'),
    )
    chatbot_name = models.CharField(max_length=200)
    chat_bot_media_path = models.TextField(blank=True)
    chat_bot_chroma_db_path = models.TextField(blank=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    llm_model = models.CharField(choices=LLM_MODEL, default="system openai", max_length=50)
    model = models.CharField(choices=MODEL, default="gpt-3.5-turbo", max_length=50)
    openai_key = models.TextField(default="")
    vector_database = models.CharField(choices=VECTOR_DATABASE, default="chroma", max_length=200)
    pinecone_key = models.CharField(default="", max_length=200)
    pinecone_env = models.TextField(default="")
    pinecone_user_index = models.CharField(default="", max_length=200)
    temperature = models.FloatField(default=0.4)
    context = models.TextField(default="""You are a conversational chatbot and Use the following pieces of context to answer the question at the end. You will try your best to give a logical answer. If you don't know the answer, just say that you don't know, don't try to make up an answer""")
    chatbot_id = models.CharField(max_length=50)
    hits = models.PositiveIntegerField(default=10)
    seconds = models.PositiveIntegerField(default=60)
    visibility = models.CharField(max_length=50, default='private')
    login_status = models.CharField(max_length=20, choices=LOGIN_STATUS, default='login')
    icon_url = models.ImageField(upload_to='chatbot', default='default_images/chatbot_image.png',max_length=255)
    chatbot_appearance = models.OneToOneField(
        "ChatbotAppearance", 
        on_delete=models.CASCADE,
        related_name='chatbot'  # Enables reverse lookup
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatbotAppearance(models.Model):
    chatbot_id = models.CharField(max_length=50)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    chatbot_title = models.CharField(max_length=255, default="Welcome To Chatbot")
    display_name = models.TextField(max_length=2000)
    footer_name = models.TextField(max_length=2000, default="Powered by My AI Solutions.")
    initial_message = models.TextField(blank=True, default="Hi! What can I help with you?")
    chatbot_theme = models.CharField(max_length=10, default="#8d54a2", blank=True)
    chatbot_mode = models.BooleanField(default=False)
    suggested_messages = models.TextField(blank=True)
    destination = models.TextField(blank=True)
    chatbot_image = models.ImageField(upload_to='chatbot_images/', default='default_images/chatbot_image.png', null=True, blank=True,max_length=255)
    chatbot_launcher_icon = models.ImageField(upload_to='launcher_icon/', default='default_images/avatar-1.png', null=True, blank=True,max_length=255)
    top_bar_background = models.CharField(max_length=10, default="#8d54a2")
    top_bar_textcolor = models.CharField(max_length=10, default="#000000")
    bot_message_background = models.CharField(max_length=10, default="#ffffff")
    bot_message_color = models.CharField(max_length=10, default="#46464e")
    user_message_background = models.CharField(max_length=10, default="#ffffff")
    user_message_color = models.CharField(max_length=10, default="#46464e")
    chatbot_background_color = models.CharField(max_length=10, default="#e6e6e6")
    chatbot_background_pattern = models.ImageField(upload_to='chatbot_background_patterns/', blank=True,max_length=255,)
    font_family = models.CharField(max_length=255, default="Arial")
    font_size = models.PositiveIntegerField(blank=True, default=14)
    widget_width = models.PositiveIntegerField(blank=True, default=25)
    widget_height = models.PositiveIntegerField(blank=True, default=450)
    widget_position = models.CharField(max_length=5, default="right")  # Assumes 'right' or 'left, blank=True'
    show_popup_notification = models.BooleanField(default=True)
    delay_showing_popup_notification = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE, blank=True)
    name = models.CharField(default="", max_length=250)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    def upload_path(instance, filename):  # type: ignore
        """Generate the upload path dynamically based on user and chatbot."""
        filename = format_name(os.path.basename(filename)) 
        # Ensure user and chatbot are not None before accessing their attributes
        formatted_username = format_name(getattr(instance.user, "username", "unknown"))
        formatted_chatbot_name = format_name(getattr(instance.chatbot, "chatbot_name", "unknown"))
        return f'{formatted_username}/uploads/{formatted_chatbot_name}/upload_Documents/{filename}'  # type: ignore
    filepath = models.FileField(upload_to=upload_path,default="")  # Use the function here
    size = models.CharField(default="", max_length=250)
    no_of_characters = models.PositiveIntegerField(default=0, blank=True)
    no_of_chunks = models.PositiveIntegerField(default=0, blank=True)
    status = models.CharField(default="pending", max_length=20)      
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)
    status_message = models.TextField(default="The website has been successfully inserted into the database.", max_length=5000)
    def __str__(self):
        return self.name

class DocumentNamespaceIds(models.Model):
    doc_id = models.CharField(default="", max_length=100)
    doc_name = models.CharField(default="", max_length=500)
    namespace = models.CharField(default="", max_length=100)
    index_name = models.CharField(default=PINECONE_INDEX_NAME, max_length=100)
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)

class DocumentCollectionIds(models.Model):
    doc_id = models.CharField(default="", max_length=100)
    doc_name = models.CharField(default="", max_length=500)
    collection = models.CharField(default="", max_length=100)
    chroma_dir = models.TextField(default="")
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    status = models.CharField(default="pending", max_length=50)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)
    

class Chat(models.Model):
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    category = models.CharField(default="", max_length=50)
    history = models.CharField(default="", max_length=50)
    question = models.CharField(default="", max_length=500)
    answer = models.TextField(default="", max_length=5000)
    sent = models.DateTimeField(auto_now_add=True)
    received = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


class VisitorVisits(models.Model):
    visitor_id = models.CharField(max_length=255, default=get_random_str)
    chatbot_id = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    geo_location = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    landing_page = models.CharField(max_length=255, blank=True)
    browser = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=255, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
class ChatHistory(models.Model):
    FEEDBACK_CHOICE = (
        ("thumbsup", 'Thumbs Up'),
        ("thumbsdown", 'Thumbs Down')
    )
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    question = models.CharField(default="", max_length=500)
    answer = models.TextField(default="", max_length=5000)
    question_datetime = models.DateTimeField(auto_now_add=True)
    answer_datetime = models.DateTimeField(auto_now_add=True)
    feedback_flag = models.CharField(choices=FEEDBACK_CHOICE, null=True, max_length=50)
    feedback_datetime = models.DateTimeField(null=True)
    positive_comment = models.TextField(null=True)
    negative_comment = models.TextField(null=True)
    category = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class WebsiteDB(models.Model):
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    url = models.TextField(default="")
    no_of_characters = models.PositiveIntegerField(default=0, blank=True)
    no_of_chunks = models.PositiveIntegerField(default=0, blank=True)
    status = models.CharField(default="pending", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    status_message = models.TextField(default="The website has been successfully inserted into the database.", max_length=5000)
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)

class WebsiteCollectionIds(models.Model):
    web_id = models.CharField(default="", max_length=100)
    web_name = models.CharField(default="", max_length=500)
    collection = models.TextField(default="", max_length=100)
    chroma_dir = models.TextField(default="")
    chatbot = models.ForeignKey("ChatBotDB", on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    website = models.ForeignKey("WebsiteDB", on_delete=models.CASCADE)