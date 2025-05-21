import logging
import os
import random
import shutil
import string
import traceback

from django.core.exceptions import ObjectDoesNotExist  # Correct import for ObjectDoesNotExist
from RAG_Backend import settings
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, ChatbotAppearance, CustomUser
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, create_directories, delete_folder, format_name

logger = logging.getLogger('myapp')

class ChatBotService:

    @staticmethod
    def int_code_generate(c_id: str, base_url: str):
        """
        Generates integration code and share link for a chatbot.

        Args:
            c_id (str): The chatbot ID.
            base_url (str): The base URL of the application.

        Returns:
            dict: A dictionary containing the chatbot integration code and share link.
        """
        logger.debug(f"Generating integration code for chatbot ID: {c_id}, base_url: {base_url}")
        # Use a valid jQuery CDN URL and ensure proper script tag formatting
        chatbot_code = (
            f'<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>'
            f'<script src="{base_url}/static/chat-widget/chat-loader.js" '
            f'chatbot-id="{c_id}" base_url="{base_url}" type="application/javascript"></script>'
        )
        chatbot_share_link = f'{base_url}/chatbot/share/public/{c_id}'
        result = {
            "chatbot_code": chatbot_code,
            "chatbot_share_link": chatbot_share_link
        }
        logger.debug(f"Generated integration code: {result}")
        return result

    @staticmethod
    def ChatbotDetails(c_id: int, user_id: int):
        """
        Fetches chatbot details based on chatbot ID (c_id) and user ID (user_id).

        Args:
            c_id (int): The internal database ID of the chatbot.
            user_id (int): The ID of the user.

        Returns:
            dict or None: A dictionary with chatbot data or None if not found.
        """
        try:
            logger.debug(f"Fetching chatbot details for c_id: {c_id}, user_id: {user_id}")
            CustomUserdata = CustomUser.objects.get(id=user_id)
            logger.debug(f"Fetched CustomUser: {CustomUserdata}")
            
            chatbot_data = ChatBotDB.objects.get(id=c_id, user_id=user_id)
            logger.debug(f"Fetched ChatBotDB: {chatbot_data}")
            
            chatbot_count = ChatBotDB.objects.filter(user_id=user_id).count()
            logger.debug(f"Counted chatbots for user: {chatbot_count}")
            
            user_chatbots = list(ChatBotDB.objects.filter(user_id=user_id))  # Convert QuerySet to list for safety
            logger.debug(f"Fetched user chatbots: {user_chatbots}")
            
            # Constructing the response dictionary
            data = {
                "user_chatbots": user_chatbots,
                "chatbot": chatbot_data,
                "chatbot_count": chatbot_count,
                "chatbot_id": chatbot_data.id,  # type: ignore
                "CustomUserdata_uuld": CustomUserdata.uuid,  # Note: 'uuld' seems to be a typo, should be 'uuid'
                "chat_bot_id": chatbot_data.chatbot_id,
                "chatbot_name": chatbot_data.chatbot_name,
                "llm_model": chatbot_data.llm_model,
                "model": chatbot_data.model,
                "temperature": chatbot_data.temperature,
                "context": chatbot_data.context,
                "openai_key": chatbot_data.openai_key,
                "vector_database": chatbot_data.vector_database,
                "pinecone_key": chatbot_data.pinecone_key,
                "pinecone_env": chatbot_data.pinecone_env,
                "visibility": chatbot_data.visibility,
                "hits": chatbot_data.hits,
                "seconds": chatbot_data.seconds,
                "pinecone_user_index": chatbot_data.pinecone_user_index,
            }
            logger.debug(f"Prepared chatbot details: {data}")
            return data
        except ObjectDoesNotExist:
            logger.warning(f"Chatbot or user not found for c_id: {c_id}, user_id: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching chatbot details for c_id: {c_id}, user_id: {user_id}: {str(e)}\n{traceback.format_exc()}")
            return None

    @staticmethod
    def get_chatbot_by_user_and_id(chat_id, user_id):
        """
        Fetches a chatbot by its chatbot_id and user_id.

        Args:
            chat_id (str): The chatbot ID.
            user_id (int): The ID of the user.

        Returns:
            ChatBotDB or None: The chatbot object if found, otherwise None.
        """
        try:
            logger.debug(f"Fetching chatbot by chat_id: {chat_id}, user_id: {user_id}")
            chatbot = ChatBotDB.objects.get(chatbot_id=chat_id, user_id=user_id)
            logger.debug(f"Fetched chatbot: {chatbot}")
            return chatbot
        except ChatBotDB.DoesNotExist:
            logger.warning(f"Chatbot not found for chat_id: {chat_id}, user_id: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching chatbot for chat_id: {chat_id}, user_id: {user_id}: {str(e)}\n{traceback.format_exc()}")
            return None

    @staticmethod
    def get_user_chatbots(user_id):
        """
        Fetches all chatbots for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            QuerySet: A queryset of chatbots, or an empty list if an error occurs.
        """
        try:
            logger.debug(f"Fetching all chatbots for user_id: {user_id}")
            chatbots = ChatBotDB.objects.filter(user=user_id).only("chatbot_name")
            logger.debug(f"Fetched chatbots: {list(chatbots)}")
            return chatbots
        except Exception as e:
            logger.error(f"Error fetching chatbots for user {user_id}: {str(e)}\n{traceback.format_exc()}")
            return []

    @staticmethod
    def get_chatbot_by_id(chatbot_id):
        """
        Fetches a single chatbot by its chatbot_id.

        Args:
            chatbot_id (str): The chatbot ID.

        Returns:
            ChatBotDB or None: The chatbot object if found, otherwise None.
        """
        try:
            logger.debug(f"Fetching chatbot by chatbot_id: {chatbot_id}")
            chatbot = ChatBotDB.objects.filter(chatbot_id=chatbot_id).first()
            if chatbot:
                logger.info(f"Chatbot found: {chatbot.chatbot_name} (ID: {chatbot_id})")
            else:
                logger.warning(f"No chatbot found with ID: {chatbot_id}")
            logger.debug(f"Fetched chatbot: {chatbot}")
            return chatbot
        except Exception as e:
            logger.error(f"Error fetching chatbot ID {chatbot_id}: {str(e)}\n{traceback.format_exc()}")
            return None

    @staticmethod
    def generate_chatbot_id():
        """
        Generates a random 15-character chatbot ID.

        Returns:
            str: A randomly generated chatbot ID.
        """
        logger.debug("Generating random chatbot ID")
        chatbot_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        logger.info(f"Generated Chatbot ID: {chatbot_id}")
        return chatbot_id

    @staticmethod
    def chat_bot_folder_structure(user_data, chat_bot_name, update_type, chat_bot_data={}):
        """
        Manages the folder structure for a chatbot, either creating or updating it.

        Args:
            user_data: The user object.
            chat_bot_name (str): The name of the chatbot.
            update_type (str): Either 'create' or 'update'.
            chat_bot_data (dict): Existing chatbot data (used for updates).

        Returns:
            list: [success (bool), media_path (str), chroma_db_path (str)]
        """
        logger.debug(f"Managing folder structure for chatbot: {chat_bot_name}, user: {user_data.username}, update_type: {update_type}")
        if update_type == 'create':
            smedia_file, media_bot_ = create_directories(str(user_data.username), str(chat_bot_name))
            copy_path = os.path.join(settings.COPY_ROOT, 'chat_bot')
            logger.debug(f"Creating directories: smedia_file={smedia_file}, media_bot_={media_bot_}, copy_path={copy_path}")
            try:
                copy_directory_contents(copy_path, smedia_file)
                logger.info(f"Successfully created chatbot directories for '{chat_bot_name}' (User: {user_data.username}).")
                return [True, smedia_file, media_bot_]
            except Exception as e:
                logger.error(f"Error creating chatbot directories for '{chat_bot_name}': {str(e)}\n{traceback.format_exc()}")
                return [False, '', '']
        else:
            logger.debug(f"Updating chatbot directories for '{chat_bot_name}' (User: {user_data.username}).")
            old_chatbot_upload_name = chat_bot_data.chat_bot_media_path
            new_chatbot_upload_name, new_chatbot_media_db_name = create_directories(str(user_data.username), str(chat_bot_name), type=True)
            logger.debug(f"Renaming directories: old={old_chatbot_upload_name}, new={new_chatbot_upload_name}, chroma_db_old={chat_bot_data.chat_bot_chroma_db_path}, chroma_db_new={new_chatbot_media_db_name}")
            try:
                shutil.move(old_chatbot_upload_name, new_chatbot_upload_name)
                shutil.move(chat_bot_data.chat_bot_chroma_db_path, new_chatbot_media_db_name)
                logger.info(f"Successfully renamed chatbot folders for '{chat_bot_name}'.")
            except Exception as e:
                logger.error(f"Error updating chatbot directories for '{chat_bot_name}': {str(e)}\n{traceback.format_exc()}")
                return [False, '', '']
            return [True, new_chatbot_upload_name, new_chatbot_media_db_name]

    @staticmethod
    def create_chatbot(user, chatbot_name):
        """
        Creates a new chatbot, including folder structure and database entries.

        Args:
            user: The user object.
            chatbot_name (str): The name of the chatbot to create.

        Returns:
            dict: A dictionary with success or error message.
        """
        logger.debug(f"Creating new chatbot '{chatbot_name}' for user {user.username}")
        chatbot_id = ChatBotService.generate_chatbot_id()
        
        if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
            logger.warning(f"Chatbot with name '{chatbot_name}' already exists for user {user.username}.")
            return {"error": "Chatbot with this name already exists."}

        logger.info(f"Creating new chatbot '{chatbot_name}' for user {user.username} (ID: {chatbot_id}).")

        response = ChatBotService.chat_bot_folder_structure(user, chatbot_name, "create")
        logger.debug(f"Folder structure response: {response}")
        
        if not response[0]:
            logger.error(f"Failed to create folder structure for chatbot '{chatbot_name}'.")
            return {"error": "Something went wrong."}

        chat_bot_media_url = f"{format_name(user.username)}/uploads/{format_name(chatbot_name)}/"
        chat_bot_user_chroma_path = f"{settings.MEDIA_URL}{format_name(user.username)}/chroma_db/{format_name(chatbot_name)}/"
        icon_url = f"{chat_bot_media_url}/default_images/chatbot_image.png"
        chatbot_launcher_icon = f"{chat_bot_media_url}/default_images/avatar-1.png"
        chatbot_background_pattern = ""

        logger.debug(f"Generated paths: media_url={chat_bot_media_url}, chroma_path={chat_bot_user_chroma_path}, icon_url={icon_url}, launcher_icon={chatbot_launcher_icon}")

        logger.info(f"Folder structure created successfully for '{chatbot_name}'.")

        try:
            chatbot_appearance = ChatbotAppearance.objects.create(
                chatbot_id=chatbot_id,
                display_name=chatbot_name,
                chatbot_background_pattern=chatbot_background_pattern,
                chatbot_image=icon_url,
                chatbot_launcher_icon=chatbot_launcher_icon
            )
            logger.debug(f"Created ChatbotAppearance: {chatbot_appearance}")

            chatbot_db_entry = ChatBotDB.objects.create(
                chatbot_name=chatbot_name,
                chatbot_id=chatbot_id,
                openai_key=getattr(settings, "OPENAI_API_KEY", ""),
                icon_url=icon_url,
                chat_bot_media_path=response[1],
                chat_bot_chroma_db_path=response[2],
                user=user,
                chatbot_appearance=chatbot_appearance
            )
            logger.debug(f"Created ChatBotDB entry: {chatbot_db_entry}")

            logger.info(f"Chatbot '{chatbot_name}' (ID: {chatbot_id}) successfully created for user {user.username}.")
            return {"success": "Chatbot added successfully."}
        except Exception as e:
            logger.error(f"Error creating chatbot '{chatbot_name}' (ID: {chatbot_id}): {str(e)}\n{traceback.format_exc()}")
            return {"error": "Something went wrong."}

    @staticmethod
    def update_chatbot(user, chatbot_name, chat_id):
        """
        Updates an existing chatbot, including folder structure and database entries.

        Args:
            user: The user object.
            chatbot_name (str): The new name of the chatbot.
            chat_id (str): The chatbot ID.

        Returns:
            dict: A dictionary with success or error message.
        """
        logger.debug(f"Updating chatbot for user {user.username}, chat_id: {chat_id}, new name: {chatbot_name}")
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            logger.warning(f"Chatbot with ID {chat_id} not found.")
            return {"error": "Chatbot not found."}

        if ChatBotDB.objects.filter(user=user, chatbot_name=chatbot_name).exists():
            logger.warning(f"Chatbot with name '{chatbot_name}' already exists for user {user.username}.")
            return {"error": "Chatbot with this name already exists."}

        logger.info(f"Updating chatbot '{chatbot_data.chatbot_name}' (ID: {chat_id}) for user {user.username}.")

        response = ChatBotService.chat_bot_folder_structure(user, chatbot_name, "update", chat_bot_data=chatbot_data)
        logger.debug(f"Folder structure update response: {response}")
        if not response[0]:
            logger.error(f"Failed to update chatbot folder structure for '{chatbot_name}' (ID: {chat_id}).")
            return {"error": "Something went wrong."}

        chat_bot_media_url = f"{format_name(user.username)}/uploads/{format_name(chatbot_name)}/"
        icon_url = f"{chat_bot_media_url}/default_images/chatbot_image.png"
        chatbot_background_pattern = ""

        logger.debug(f"Generated paths: media_url={chat_bot_media_url}, icon_url={icon_url}")

        try:
            chatbot_data.chatbot_name = chatbot_name
            chatbot_data.icon_url = icon_url  # type: ignore
            chatbot_data.chat_bot_media_path = response[1]
            chatbot_data.chat_bot_chroma_db_path = response[2]
            chatbot_data.save()
            logger.debug(f"Updated ChatBotDB entry: {chatbot_data}")

            logger.info(f"Chatbot '{chatbot_name}' (ID: {chat_id}) successfully updated in the database.")

            chatbot_appearance = ChatbotAppearance.objects.filter(id=chatbot_data.chatbot_appearance.id).first()
            if chatbot_appearance:
                chatbot_appearance.display_name = chatbot_name
                chatbot_appearance.chatbot_background_pattern = chatbot_background_pattern  # type: ignore
                chatbot_appearance.chatbot_image = icon_url  # type: ignore
                chatbot_appearance.save()
                logger.debug(f"Updated ChatbotAppearance: {chatbot_appearance}")

                logger.info(f"Chatbot appearance updated for '{chatbot_name}' (ID: {chat_id}).")
                return {"success": "Chatbot successfully updated."}
            else:
                logger.error(f"Chatbot appearance data not found for chatbot '{chatbot_name}' (ID: {chat_id}).")
                return {"error": "Something went wrong with chatbot appearance data."}
        except Exception as e:
            logger.error(f"Error updating chatbot '{chatbot_name}' (ID: {chat_id}): {str(e)}\n{traceback.format_exc()}")
            return {"error": "Something went wrong."}

    @staticmethod
    def delete_chatbot(chat_id):
        """
        Deletes a chatbot, including its folder structure and database entries.

        Args:
            chat_id (str): The chatbot ID.

        Returns:
            dict: A dictionary with success or error message.
        """
        logger.debug(f"Deleting chatbot with chat_id: {chat_id}")
        chatbot_data = ChatBotDB.objects.filter(chatbot_id=chat_id).first()
        if not chatbot_data:
            logger.warning(f"Chatbot with ID {chat_id} not found.")
            return {"error": "Chatbot not found."}

        try:
            chatbot_data.chatbot_appearance.delete()
            chatbot_data.delete()
            delete_folder(chatbot_data.chat_bot_media_path)
            delete_folder(chatbot_data.chat_bot_chroma_db_path)
            logger.info(f"Chatbot with ID {chat_id} successfully deleted.")
            return {"success": "Chatbot successfully deleted."}
        except Exception as e:
            logger.error(f"Error deleting chatbot with ID {chat_id}: {str(e)}\n{traceback.format_exc()}")
            return {"error": "Failed to delete chatbot."}
