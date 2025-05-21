import random
import string
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from django.utils.timezone import now

from RAG_CHATBOT_BACKEND_APIS.models import Thread, UserThread
from RAG_CHATBOT_BACKEND_APIS.services.Langchain_Models.LangchainEmbeddingService import LangchainEmbeddingService

logger = logging.getLogger(__name__)

def generate_thread_id():
    """
    Generates a random 15-character thread ID.

    Returns:
        str: A randomly generated thread ID.
    """
    thread_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    logger.debug(f"Generated thread ID: {thread_id}")
    return thread_id

class ThreadServices:
    @staticmethod
    def process_and_assign_thread_in_the_process_urls(user, website_instance, chatbot):
        """
        Processes website URLs in a background thread and assigns a thread ID.

        Args:
            user: The user object initiating the process.
            website_instance: The WebsiteDB instance to process.
            chatbot: The ChatBotDB instance associated with the process.

        Returns:
            str: The generated thread ID.
        """
        thread_id = generate_thread_id()
        logger.info(f"Started thread {thread_id} for website URLs.")

        # Create or get Thread
        thread, _ = Thread.objects.get_or_create(title=f"Thread {thread_id}")
        logger.debug(f"Created or fetched Thread: {thread}")

        # Create UserThread instance
        user_thread = UserThread.objects.create(
            user=user,
            thread=thread,
            unique_thread_id=thread_id,
            status="Processing",
            assigned_at=now(),
            log_messages="Thread initiated.\n"
        )
        logger.debug(f"Created UserThread: {user_thread}")

        def process_urls():
            try:
                logger.info(f"Thread {thread_id}: Processing started.")
                website_instance.status = "processing"
                website_instance.status_message = "Processing website for training."
                website_instance.save()
                logger.debug(f"Updated website_instance status to processing: {website_instance}")

                bot_path = chatbot.chat_bot_chroma_db_path
                logger.debug(f"Using bot_path: {bot_path}")

                # Process URLs
                website_dist = LangchainEmbeddingService.process_urls_for_training(
                    website_instance, chatbot, user, bot_path, thread_id
                )
                logger.debug(f"Processed URLs result: {website_dist}")

                # Update website & user thread status
                website_instance.status = website_dist.get('status', "Failed")
                website_instance.no_of_characters = website_dist.get('no_of_characters', 0)
                website_instance.no_of_chunks = website_dist.get('no_of_chunks', 0)
                website_instance.status_message = website_dist.get('status_message', "Error processing.")
                user_thread.status = website_instance.status
                user_thread.log_messages = website_dist.get('log_messages', "Processing failed.\n")
                logger.debug(f"Updated statuses - website: {website_instance.status}, user_thread: {user_thread.status}")
            except Exception as e:
                error_message = f"Error processing URLs in thread {thread_id}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)
                website_instance.status = "Failed"
                website_instance.status_message = f"Error: {str(e)}"
                user_thread.status = "Failed"
                user_thread.log_messages = f"Error: {str(e)}\n"
            finally:
                user_thread.save()
                website_instance.save()
                logger.debug(f"Saved updates - website_instance: {website_instance}, user_thread: {user_thread}")

        # Execute the process in the background using ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=5)
        executor.submit(process_urls)
        logger.debug(f"Submitted process_urls to executor for thread {thread_id}")
        return thread_id

    @staticmethod
    def process_and_assign_thread_in_the_process_documents(user_data, document, chatbot):
        """
        Processes uploaded documents in a background thread and assigns a thread ID.

        Args:
            user_data: The user object initiating the process.
            document: The Document instance to process.
            chatbot: The ChatBotDB instance associated with the process.

        Returns:
            str: The generated thread ID.
        """
        thread_id = generate_thread_id()
        logger.info(f"Started thread {thread_id} for document processing.")  # Fixed log message
        thread, _ = Thread.objects.get_or_create(title=f"Thread {thread_id}")
        logger.debug(f"Created or fetched Thread: {thread}")

        # Create UserThread instance
        user_thread = UserThread.objects.create(
            user=user_data,
            thread=thread,
            unique_thread_id=thread_id,
            status="Processing",
            assigned_at=now(),
            log_messages="Thread initiated.\n"
        )
        logger.debug(f"Created UserThread: {user_thread}")

        def process_documents():
            try:
                logger.info(f"Thread {thread_id}: Processing started.")
                document.status = "processing"
                document.status_message = "Processing document for training."  # Fixed message consistency
                document.save()
                logger.debug(f"Updated document status to processing: {document}")

                bot_path = chatbot.chat_bot_chroma_db_path
                logger.debug(f"Using bot_path: {bot_path}")

                document_list = LangchainEmbeddingService.uploaded_document_and_train_llm(
                    document, chatbot, user_data, bot_path, thread_id
                )
                logger.debug(f"Processed document result: {document_list}")

                document.status = document_list.get('status', "Failed")
                document.no_of_characters = document_list.get('no_of_characters', 0)
                document.no_of_chunks = document_list.get('no_of_chunks', 0)
                document.status_message = document_list.get('status_message', "Error processing.")
                user_thread.status = document.status  # Fixed to use document.status instead of status_message
                user_thread.log_messages = document_list.get('log_messages', "Processing failed.\n")
                logger.debug(f"Updated statuses - document: {document.status}, user_thread: {user_thread.status}")
            except Exception as e:
                error_message = f"Error processing document in thread {thread_id}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)
                document.status = "Failed"
                document.status_message = f"Error: {str(e)}"
                user_thread.status = "Failed"
                user_thread.log_messages = f"Error: {str(e)}\n"
            finally:
                user_thread.save()
                document.save()
                logger.debug(f"Saved updates - document: {document}, user_thread: {user_thread}")

        executor = ThreadPoolExecutor(max_workers=5)
        executor.submit(process_documents)
        logger.debug(f"Submitted process_documents to executor for thread {thread_id}")
        return thread_id

    @staticmethod
    def process_and_assign_thread_in_to_genrate_answer(user_data, document, chatbot):
        """
        Placeholder method to process and assign a thread for generating answers.

        Args:
            user_data: The user object initiating the process.
            document: The Document instance to process.
            chatbot: The ChatBotDB instance associated with the process.

        Returns:
            str: The generated thread ID.
        """
        thread_id = generate_thread_id()
        logger.debug(f"Generated thread ID for answer generation: {thread_id}")
        # TODO: Implement answer generation logic
        logger.warning(f"Thread {thread_id}: Answer generation not implemented yet.")
        return thread_id