import logging
import random
import string
import os
import shutil
from django.conf import settings




# Create a logger instance
logger = logging.getLogger(__name__)


def get_base_url(request):
    """Returns the base URL dynamically"""
    return request.build_absolute_uri('/').rstrip('/')


def get_random_str():
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    return random_str

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    
def create_directories(username, chat_bot_name, type = False):
    """
    Creates necessary directories for storing chatbot media and Chroma DB data.
    
    :param username: The username of the user.
    :param chat_bot_name: The chatbot name.
    :return: Paths of the created directories.
    """
    def format_name(name):
        return name.replace(" ", "_").lower()
    chat_bot_media_path = os.path.join(settings.MEDIA_ROOT, format_name(username), "uploads", format_name(chat_bot_name))
    chat_bot_chroma_db_path = os.path.join(settings.MEDIA_ROOT, format_name(username), "chroma_db", format_name(chat_bot_name))
    if not type:
        os.makedirs(os.path.join(chat_bot_media_path, "upload_Documents"), exist_ok=True)
        os.makedirs(chat_bot_chroma_db_path, exist_ok=True)    
    return chat_bot_media_path, chat_bot_chroma_db_path

def delete_folder(folder_path):
    """
    Deletes the folder at the given path and all its contents.
    
    :param folder_path: Path of the folder to be deleted.
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder {folder_path} and its contents have been deleted.")
        except Exception as e:
            print(f"Error occurred while deleting the folder: {e}")
    else:
        print(f"The folder {folder_path} does not exist.")
def copy_directory_contents(source_dir, destination_dir):
    """
    Copies all files and subdirectories from source_dir to destination_dir.
    
    Args:
        source_dir (str): Path to the source directory.
        destination_dir (str): Path to the destination directory.
    
    Returns:
        bool: True if the operation succeeds, False otherwise.
    """
    try:
        # Ensure the destination directory exists
        os.makedirs(destination_dir, exist_ok=True)
        # Copy all files and directories
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            destination_item = os.path.join(destination_dir, item)
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item, dirs_exist_ok=True)  # Copy directories
            else:
                shutil.copy2(source_item, destination_item)  # Copy files with metadata
        print(f"✅ Successfully copied from {source_dir} to {destination_dir}")
        return True
    except Exception as e:
        print(f"❌ Error copying files: {e}")
        return False

def format_name(name):
    """Format names by converting to lowercase and replacing spaces with underscores."""
    return name.strip().lower().replace(" ", "_")


# Global variable declaration
def ensure_directory_exists(directory_path):
    """
    Ensure that the given directory exists. If not, create it.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Creates all intermediate directories if necessary
        print(f"✅ Created directory: {directory_path}")
    else:
        print(f"✅ Directory already exists: {directory_path}")
