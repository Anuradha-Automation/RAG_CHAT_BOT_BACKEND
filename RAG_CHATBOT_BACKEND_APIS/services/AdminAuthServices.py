import logging
import os
import traceback
from django.db import DatabaseError
from django_filters.exceptions import FieldError
from RAG_Backend import settings
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from RAG_CHATBOT_BACKEND_APIS.utils import copy_directory_contents, format_name

logger = logging.getLogger('myapp')

class AuthServices:
    @staticmethod
    def fetch_user_data(key, value):
        """
        Fetches user data from the database based on a key-value pair.

        Args:
            key (str): The field name to query (e.g., 'uuid', 'email').
            value: The value to match against the field.

        Returns:
            CustomUser or None: The user object if found, otherwise None.
        """
        try:
            logger.debug(f"Fetching user data with {key}={value}")
            if not hasattr(CustomUser, key):
                logger.error(f"Invalid field '{key}' for CustomUser model.")
                return None

            user = CustomUser.objects.get(**{key: value})
            logger.info(f"User found for {key}={value}: {user}")
            return user
        except CustomUser.DoesNotExist:
            logger.warning(f"User with {key}={value} does not exist.")
            return None
        except CustomUser.MultipleObjectsReturned:
            logger.error(f"Multiple users found for {key}={value}. Expected a single record.")
            return None
        except FieldError:
            logger.error(f"Invalid field '{key}' provided. Check your database model.")
            return None
        except DatabaseError as db_err:
            logger.error(f"Database error while fetching user with {key}={value}: {db_err}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching user with {key}={value}: {str(e)}\n{traceback.format_exc()}")
            return None

    @staticmethod
    def check_user_existence(key, value):
        """
        Checks if a user exists in the database based on a key-value pair.

        Args:
            key (str): The field name to query (e.g., 'uuid', 'email').
            value: The value to match against the field.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        try:
            logger.debug(f"Checking existence for {key}={value}")
            exists = CustomUser.objects.filter(**{key: value}).exists()
            logger.debug(f"Checked existence for {key}={value}: {exists}")
            return exists
        except FieldError:
            logger.error(f"Invalid field '{key}' provided. Check your database model.")
            return False
        except DatabaseError as db_err:
            logger.error(f"Database error while checking user existence with {key}={value}: {db_err}")
            return False
        except Exception as e:
            logger.error(f"Error checking user existence with {key}={value}: {str(e)}\n{traceback.format_exc()}")
            return False

    @staticmethod
    def RegisterUser(username, email, password, base_url):
        """
        Registers a new user, creating necessary directories and saving user data.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str): The password for the new user.
            base_url (str): The base URL for constructing profile URLs.

        Returns:
            tuple: (bool, str) - (success status, message)
        """
        try:
            user_slug = format_name(username)
            logger.debug(f"Creating user directories for user_slug: {user_slug}")

            main_user_folder = os.path.join(settings.MEDIA_ROOT, user_slug)
            user_upload_dir = os.path.join(main_user_folder, "uploads")
            user_chroma_db_dir = os.path.join(main_user_folder, "chroma_db")
            user_profile_dir = os.path.join(main_user_folder, "user_profile")
            profile_pic_path = os.path.join(user_profile_dir, "user_profile_pic.jpg")

            logger.debug(f"Creating directories: {main_user_folder}, {user_upload_dir}, {user_chroma_db_dir}, {user_profile_dir}")
            os.makedirs(user_upload_dir, exist_ok=True)
            os.makedirs(user_chroma_db_dir, exist_ok=True)
            os.makedirs(user_profile_dir, exist_ok=True)

            user_upload_url = f"{settings.MEDIA_URL}{user_slug}/uploads/"
            user_chroma_db_url = f"{settings.MEDIA_URL}{user_slug}/chroma_db/"

            original_path = os.path.join(settings.COPY_ROOT, "user_profile")
            logger.debug(f"Copying user profile from {original_path} to {user_profile_dir}")

            if not copy_directory_contents(original_path, user_profile_dir):
                logger.error("Failed to copy user profile directory.")
                return False, "Failed to copy user profile directory."

            profile_url = f"{base_url}{settings.MEDIA_URL}{user_slug}/user_profile/user_profile_pic.jpg"
            logger.debug(f"Generated profile URL: {profile_url}")

            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            logger.debug(f"Created user: {user}")
            user.user_upload_path = user_upload_url
            user.user_chroma_path = user_chroma_db_url
            user.profile_pic = profile_pic_path  # type: ignore
            user.profile_url = profile_url
            user.save()
            logger.debug(f"Saved user with additional fields: {user}")

            logger.info(f"User successfully registered: {username}")
            return True, "User successfully registered."
        except Exception as e:
            logger.error(f"Error registering user {username}: {str(e)}\n{traceback.format_exc()}")
            return False, "Something went wrong"

    @staticmethod
    def UpdateUser_Details(login_user_uuid, user_data, user_profile_data):
        """
        Updates user details, including profile picture and other fields.

        Args:
            login_user_uuid (str): The UUID of the user to update.
            user_data (dict): A dictionary of user fields to update.
            user_profile_data (dict): A dictionary of profile data (e.g., profile picture).

        Returns:
            tuple: (bool, str) - (success status, message)
        """
        logger.debug(f"Updating user details for UUID: {login_user_uuid}, user_data: {user_data}, user_profile_data: {user_profile_data}")
        user = AuthServices.fetch_user_data('uuid', login_user_uuid)
        if not user:
            logger.warning(f"User with UUID {login_user_uuid} not found for update.")
            return False, "User not found."

        profile_updated = False
        if 'profile_pic' in user_profile_data:
            logger.debug(f"Profile picture update detected: {user_profile_data['profile_pic']}")
            if user.profile_pic != user_profile_data['profile_pic']:
                user.profile_pic = user_profile_data['profile_pic']
                user.profile_url = ""
                profile_updated = True

        for field, value in user_data.items():
            if field == 'profile_pic' and not value:
                logger.debug(f"Skipping empty profile_pic field")
                continue
            if hasattr(user, field):
                logger.debug(f"Updating field {field} to {value}")
                setattr(user, field, value)
                profile_updated = True

        if profile_updated:
            user.save()
            logger.info(f"User {user.username} successfully updated.")
            return True, "User successfully updated."
        
        logger.debug(f"No updates made for user {user.username}.")
        return True, "No changes detected."