from datetime import datetime
import logging
import os
import traceback
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
import openai
from uuid import uuid4
from django.conf import settings
from langchain_community.document_loaders import (
    CSVLoader, Docx2txtLoader, PyPDFLoader, TextLoader
)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAG_CHATBOT_BACKEND_APIS.models import ChatHistory, WebsiteCollectionIds
from RAG_CHATBOT_BACKEND_APIS.services.Langchain_Models.SeleniumScraperServices import SeleniumScraperServices
from RAG_CHATBOT_BACKEND_APIS.utils import format_name

logger = logging.getLogger("myapp")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embed_fun = OpenAIEmbeddings()

class LangchainEmbeddingService:
    @staticmethod
    def GetResponseFromQuery(chatbot, user, query_text):
        """
        Queries the ChromaDB to find relevant documents and generates a response using an LLM.

        Args:
            chatbot: The ChatBotDB instance containing configuration details.
            user: The user object associated with the query.
            query_text (str): The query text to process.

        Returns:
            dict: A dictionary containing the query and response text.
        """
        logger.info(f"Query Received: {query_text}")
        logger.debug(f"Processing query for chatbot: {chatbot.chatbot_name}, user: {user}")

        if not chatbot.openai_key:
            logger.error("Missing OpenAI API key.")
            return {"query": query_text, "response": "OpenAI API key is missing."}

        openai.api_key = chatbot.openai_key
        logger.debug(f"Set OpenAI API key: {chatbot.openai_key[:5]}...")

        if chatbot.vector_database == "chroma":
            try:
                PROMPT = PromptTemplate(
                    template=chatbot.context + """{context} Question: {question} Answer: """,
                    input_variables=["context", "question"],
                )
                ChromaDb_Dir = chatbot.chat_bot_chroma_db_path
                collection_name = f"{format_name(user.username)}_{format_name(chatbot.chatbot_name)}"
                logger.debug(f"Using ChromaDB directory: {ChromaDb_Dir}, collection: {collection_name}")

                vectordb = Chroma(
                    persist_directory=ChromaDb_Dir,
                    embedding_function=embed_fun,
                    collection_name=collection_name
                )
                logger.debug(f"Initialized Chroma vector store: {vectordb}")

                llm = ChatOpenAI(
                    model_name=chatbot.model,  # type: ignore
                    temperature=chatbot.temperature,
                    openai_api_key=chatbot.openai_key  # type: ignore
                )
                logger.debug(f"Initialized ChatOpenAI LLM with model: {chatbot.model}")

                qa = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vectordb.as_retriever(),
                    return_source_documents=True,
                    chain_type_kwargs={"prompt": PROMPT}
                )
                logger.debug("Initialized RetrievalQA chain")

                response_data = qa({"query": query_text})
                response_text = response_data.get("result", "No response generated.")
                logger.debug(f"Generated response: {response_text}")
                logger.info("Successfully retrieved response from LLM.")

                response = str(response_text).replace("\n", '<br>')
                chat_history = ChatHistory(
                    chatbot=chatbot,
                    user=None,
                    question=query_text,
                    question_datetime=datetime.now(),
                    answer=response,
                    answer_datetime=datetime.now()
                )
                chat_history.save()
                logger.debug(f"Saved chat history: {chat_history}")

                return {"query": query_text, "response": response_text}
            except Exception as e:
                error_message = f"Error querying ChromaDB or LLM: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)
                return {"query": query_text, "response": f"An error occurred: {str(e)}"}
        
        logger.warning(f"Unsupported vector database: {chatbot.vector_database}")
        return {"query": query_text, "response": "Vector database not supported."}

    @staticmethod
    def process_urls_for_training(website_instance, chat_data, user_data, ChromaDb_Dir, thread_id):
        """
        Processes website URLs for training and stores them in ChromaDB.

        Args:
            website_instance: The WebsiteDB instance containing the URL.
            chat_data: The ChatBotDB instance with configuration details.
            user_data: The user object associated with the process.
            ChromaDb_Dir (str): The directory path for ChromaDB.
            thread_id (str): The thread ID for logging purposes.

        Returns:
            dict: A dictionary with status, character count, chunk count, and messages.
        """
        logger.info(f"Processing website with ID {website_instance.id} for chatbot: {chat_data.chatbot_name}")
        logger.debug(f"URL: {website_instance.url}, ChromaDb_Dir: {ChromaDb_Dir}, thread_id: {thread_id}")

        openai.api_key = chat_data.openai_key
        vector_database = chat_data.vector_database

        if vector_database == "chroma":
            collection = f"{format_name(user_data.username)}_{format_name(chat_data.chatbot_name)}"
            logger.debug(f"Using collection for training: {collection}")

            response_status, response_messages, extracted_texts = SeleniumScraperServices.get_links_selenium_get_response_data(website_instance.url)
            logger.debug(f"Selenium scraper result - status: {response_status}, messages: {response_messages}, texts length: {len(extracted_texts)}")

            if not response_status:
                error_message = f"Thread {thread_id}: error {response_messages}"
                logger.error(error_message)
                return {
                    "status": "error",
                    "no_of_characters": 0,
                    "no_of_chunks": 0,
                    "status_message": response_messages,
                    "log_messages": error_message
                }

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
            documents = text_splitter.create_documents(extracted_texts)
            ids = [str(uuid4()) for _ in documents]
            full_page_content = "".join([text.page_content for text in documents])
            logger.debug(f"Split documents into {len(documents)} chunks, total characters: {len(full_page_content)}")

            for id_new in ids:
                WebsiteCollectionIds.objects.create(
                    web_id=id_new,
                    web_name=website_instance.url,
                    collection=collection,
                    chroma_dir=ChromaDb_Dir,
                    chatbot=chat_data,
                    user=user_data,
                    website=website_instance
                )
            logger.debug(f"Created {len(ids)} WebsiteCollectionIds entries")

            db = Chroma.from_documents(
                documents,
                embed_fun,
                persist_directory=ChromaDb_Dir,
                collection_name=collection,
                ids=ids
            )
            logger.debug(f"Stored documents in ChromaDB: {db}")

            success_message = "Successfully processed and stored website in ChromaDB."
            logger.info(success_message)
            return {
                "status": "completed",
                "no_of_characters": len(full_page_content),
                "no_of_chunks": len(documents),
                "status_message": success_message,
                "log_messages": f"Thread {thread_id}: Processing completed successfully and {response_messages}"
            }
        else:
            error_message = f"Unsupported vector database: {chat_data.vector_database}"
            logger.error(error_message)
            return {
                "status": "error",
                "no_of_characters": 0,
                "no_of_chunks": 0,
                "status_message": error_message,
                "log_messages": error_message
            }

    @staticmethod
    def uploaded_document_and_train_llm(document, chat_data, user_data, ChromaDb_Dir, thread_id):
        """
        Processes an uploaded document and trains the LLM, storing it in ChromaDB.

        Args:
            document: The Document instance to process.
            chat_data: The ChatBotDB instance with configuration details.
            user_data: The user object associated with the process.
            ChromaDb_Dir (str): The directory path for ChromaDB.
            thread_id (str): The thread ID for logging purposes.

        Returns:
            dict: A dictionary with status, character count, chunk count, and messages.
        """
        logger.info(f"Processing document: {document.name} for chatbot: {chat_data.chatbot_name}")
        file_name = os.path.join(settings.MEDIA_ROOT, str(document.filepath))
        logger.debug(f"File path: {file_name}, ChromaDb_Dir: {ChromaDb_Dir}, thread_id: {thread_id}")

        if not os.path.exists(file_name):
            error_message = f"File not found: {file_name}"
            logger.error(error_message)
            return {
                "status": "error",
                "no_of_characters": 0,
                "no_of_chunks": 0,
                "status_message": "File not found.",
                "log_messages": error_message
            }

        logger.info(f"Training LLM with the uploaded document: {document.name}")
        if chat_data.vector_database == "chroma":
            loaders = {
                '.pdf': PyPDFLoader,
                '.docx': Docx2txtLoader,
                '.csv': CSVLoader,
                '.txt': TextLoader
            }
            ext = os.path.splitext(file_name)[1].lower()
            logger.debug(f"File extension: {ext}")

            if ext in loaders:
                try:
                    loader = loaders[ext](file_name)
                    doc = loader.load()
                    texts = text_splitter.split_documents(doc)
                    ids = [str(uuid4()) for _ in texts]
                    full_page_content = "".join([text.page_content for text in texts])
                    collection = f"{format_name(user_data.username)}_{format_name(chat_data.chatbot_name)}"
                    logger.debug(f"Collection name: {collection}, split into {len(texts)} chunks, total characters: {len(full_page_content)}")

                    db = Chroma.from_documents(
                        texts,
                        embed_fun,
                        persist_directory=ChromaDb_Dir,
                        collection_name=collection,
                        ids=ids
                    )
                    logger.debug(f"Stored document in ChromaDB: {db}")

                    success_message = f"Successfully stored document {document.name} in ChromaDB."
                    logger.info(f"Training LLM with the uploaded document completed successfully. Stored in ChromaDB at: {ChromaDb_Dir}")
                    return {
                        "status": "completed",
                        "no_of_characters": len(full_page_content),
                        "no_of_chunks": len(texts),
                        "status_message": success_message,
                        "log_messages": success_message
                    }
                except Exception as e:
                    error_message = f"Error processing document {document.name}: {str(e)}\n{traceback.format_exc()}"
                    logger.error(error_message)
                    return {
                        "status": "error",
                        "no_of_characters": 0,
                        "no_of_chunks": 0,
                        "status_message": f"Error processing document: {str(e)}",
                        "log_messages": error_message
                    }
            else:
                error_message = f"Unsupported file format: {ext}"
                logger.error(error_message)
                return {
                    "status": "error",
                    "no_of_characters": 0,
                    "no_of_chunks": 0,
                    "status_message": error_message,
                    "log_messages": error_message
                }
        else:
            error_message = f"Unsupported vector database: {chat_data.vector_database}"
            logger.error(error_message)
            return {
                "status": "error",
                "no_of_characters": 0,
                "no_of_chunks": 0,
                "status_message": error_message,
                "log_messages": error_message
            }