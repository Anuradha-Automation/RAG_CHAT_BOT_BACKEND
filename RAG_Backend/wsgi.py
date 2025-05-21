"""
WSGI config for RAG_Backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path
import sys
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

from RAG_Backend.settings import BASE_DIR
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
path = '/home/ubnatu/Desktop/exotica_projects/RAG_CHAT_BOT_BACKEND'
if path not in sys.path:
    sys.path.append(path)
load_dotenv("/home/ubnatu/Desktop/exotica_projects/RAG_CHAT_BOT_BACKEND/.env")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RAG_Backend.settings')

application = get_wsgi_application()
