import logging
import os
import uuid
import traceback
from RAG_CHATBOT_BACKEND_APIS.models import Document, WebsiteDB
from RAG_CHATBOT_BACKEND_APIS.services.ThreadServices import ThreadServices
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories, format_name

# Logger setup
logger = logging.getLogger("myapp")

class ChatbotContentManagementService:
    """
    Manages chatbot training content (documents and website URLs).
    Handles uploading, processing, and triggering LLM training.
    """

    @staticmethod
    def upload_and_process_chatbot_website_urls(user, chatbot, urls):
        """
        Uploads website URLs and starts training.

        Args:
            user: The user object associated with the chatbot.
            chatbot: The chatbot object to associate the URLs with.
            urls (str): The website URLs to process.

        Returns:
            tuple: (bool, str, list) - (success status, message, uploaded documents)
        """
        logger.info(f"Uploading website URLs for chatbot: {chatbot.chatbot_name}")
        logger.debug(f"Processing URLs: {urls} for user: {user}, chatbot: {chatbot}")
        try:
            website_instance = WebsiteDB(
                user=user,
                url=urls,
                chatbot=chatbot,
                no_of_characters=0,
                no_of_chunks=0,
                status="pending"
            )
            website_instance.save()
            logger.debug(f"Saved WebsiteDB instance: {website_instance}")
            
            logger.info(f"Started LLM training thread for website URLs")
            ThreadServices.process_and_assign_thread_in_the_process_urls(user, website_instance, chatbot)
            return True, "Website URLs uploaded successfully.", []
        except Exception as e:
            error_message = f"Error saving Website URL {urls}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return False, error_message, []

    @staticmethod
    def upload_and_process_chatbot_documents(user, chatbot, files):
        """
        Uploads and processes chatbot documents.

        Args:
            user: The user object associated with the chatbot.
            chatbot: The chatbot object to associate the documents with.
            files: A dictionary of uploaded files from the request.

        Returns:
            tuple: (bool, str, list) - (success status, message, uploaded documents)
        """
        if not files:
            logger.warning("No files uploaded!")
            return False, "No files uploaded.", []

        logger.debug(f"Processing files: {files} for user: {user}, chatbot: {chatbot}")
        uploaded_docs = []
        _, bot_path = create_directories(user.username, chatbot.chatbot_name)
        logger.debug(f"Created directories, bot_path: {bot_path}")

        for file in files.values():
            original_name, ext = os.path.splitext(file.name)  # Extract filename and extension
            formatted_name = format_name(original_name)  # Format filename
            unique_id = uuid.uuid4().hex[:8]  # Generate short random ID
            upload_file_name = f"{formatted_name}_{unique_id}{ext}"  # Unique filename

            logger.info(f"Processing file: {file.name} -> {upload_file_name}")
            logger.debug(f"File details - name: {file.name}, size: {file.size}")

            try:
                # Save document entry in the database
                document = Document(
                    user=user,
                    chatbot=chatbot,
                    name=upload_file_name,
                    size=file.size,
                )
                document.filepath.save(upload_file_name, file, save=True)
                logger.debug(f"Saved Document instance: {document}")

                logger.info(f"File successfully saved at: {document.filepath}")
                logger.info(f"Started LLM training thread for: {file.name}")
                ThreadServices.process_and_assign_thread_in_the_process_documents(user, document, chatbot)
                uploaded_docs.append(
                    {
                        "document_id": document.id,  # type: ignore
                        "name": document.name,
                        "size": document.size,
                        "filepath": str(document.filepath),
                    }
                )
                logger.debug(f"Added to uploaded_docs: {uploaded_docs[-1]}")

            except Exception as e:
                error_message = f"Error saving file {file.name}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)

        if not uploaded_docs:
            logger.warning("No files were uploaded successfully.")
            return False, "No files were uploaded successfully.", []

        logger.info(f"Upload completed successfully with {len(uploaded_docs)} documents.")
        return True, "Upload completed.", uploaded_docs